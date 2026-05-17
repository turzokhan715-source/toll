import re
from flask import Flask, request, jsonify
from flask_cors import CORS  
import requests

app = Flask(__name__)
CORS(app)  

def extract_otp_via_api(email, refresh_token, client_id, mode):
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json"
    }
    
    payload = {
        "client_id": client_id,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": "https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/User.Read offline_access"
    }
    
    try:
        # Token Exchange Layer
        res = requests.post(token_url, headers=headers, data=payload, timeout=15)
        if res.status_code != 200:
            payload["scope"] = "https://outlook.office.com/IMAP.AccessAsUser.All offline_access"
            res = requests.post(token_url, headers=headers, data=payload, timeout=15)
        if res.status_code != 200:
            payload.pop("scope", None)
            res = requests.post(token_url, headers=headers, data=payload, timeout=15)

        if res.status_code != 200:
            return "Endpoint rejected token. Session expired."
            
        access_token = res.json().get("access_token")
        if not access_token:
            return "Access Token missing."

        # মোড অনুযায়ী সার্চ কুয়েরি নির্ধারণ (Facebook নাকি Instagram)
        search_keyword = "Instagram" if mode == "ig" else "Facebook"
        
        messages_url = f"https://graph.microsoft.com/v1.0/me/messages?$search=\"{search_keyword}\"&$top=1"
        api_headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
        
        msg_res = requests.get(messages_url, headers=api_headers, timeout=15)
        if msg_res.status_code != 200:
            messages_url = f"https://outlook.office.com/api/v2.0/me/messages?$search=\"{search_keyword}\"&$top=1"
            msg_res = requests.get(messages_url, headers=api_headers, timeout=15)
            
        if msg_res.status_code != 200:
            return f"Failed to fetch inbox. Status: {msg_res.status_code}"
            
        messages = msg_res.json().get("value", [])
        if not messages:
            return f"No recent {search_keyword} emails found."
            
        combined_text = f"{messages[0].get('subject', '')} {messages[0].get('body', {}).get('content', '')}"
        
        # ওটিপি এক্সট্র্যাকশন প্যাটার্ন
        code_match = re.search(r'\b(\d{5,6})\b', combined_text)
        
        return code_match.group(1) if code_match else f"{search_keyword} email found, but couldn't parse code."
            
    except Exception as e:
        return f"System Error: {str(e)}"

@app.route('/get-code', methods=['POST'])
def get_code():
    data = request.json or {}
    raw_input = data.get('raw_input', '').strip()
    mode = data.get('mode', 'fb').strip()  # 'fb' অথবা 'ig'
    
    if not raw_input or '|' not in raw_input:
        return jsonify({'status': 'error', 'message': 'Invalid Data Line Format.'})
        
    parts = raw_input.split('|')
    if len(parts) < 4:
        return jsonify({'status': 'error', 'message': 'Format must be email|pass|token|client_id'})
        
    email = parts[0].strip()
    refresh_token = parts[2].strip()
    client_id = parts[3].strip()
    
    otp_code = extract_otp_via_api(email, refresh_token, client_id, mode)
    
    if otp_code.isdigit():
        return jsonify({'status': 'success', 'code': otp_code})
    else:
        return jsonify({'status': 'error', 'message': otp_code})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

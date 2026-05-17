import re
from flask import Flask, request, jsonify
from flask_cors import CORS  
import requests

app = Flask(__name__)
# এটি আপনার গিটহাব পেজেস ফ্রন্টএন্ড থেকে আসা রিকোয়েস্টগুলোকে ব্যাকএন্ডে অ্যালাউ করবে
CORS(app)  

def extract_fb_code_via_api(email, refresh_token, client_id):
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    
    # অফিশিয়াল অ্যান্ড্রয়েড ও ক্রোম ব্রাউজারের নিখুঁত হেডার ছদ্মবেশ
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
        # ১ম চেষ্টা: মডার্ন গ্রাফ এপিআই স্কোপ
        res = requests.post(token_url, headers=headers, data=payload, timeout=15)
        
        # ২য় চেষ্টা: প্রথমবার রিজেক্ট হলে পুরনো ওডব্লিউএ (OWA) স্কোপ ট্রাই করবে
        if res.status_code != 200:
            payload["scope"] = "https://outlook.office.com/IMAP.AccessAsUser.All offline_access"
            res = requests.post(token_url, headers=headers, data=payload, timeout=15)
            
        # ৩য় চেষ্টা: কোনো স্কোপ ছাড়া ডিরেক্ট ডিফল্ট এক্সচেঞ্জ
        if res.status_code != 200:
            payload.pop("scope", None)
            res = requests.post(token_url, headers=headers, data=payload, timeout=15)

        if res.status_code != 200:
            return "Endpoint rejected token. Session checking failed."
            
        res_data = res.json()
        access_token = res_data.get("access_token")
        if not access_token:
            return "Access Token missing in server response."

        # ফেসবুক মেইল স্ক্র্যাপ করার জন্য এপিআই কল
        messages_url = "https://graph.microsoft.com/v1.0/me/messages?$search=\"Facebook\"&$top=1"
        api_headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K)"
        }
        
        msg_res = requests.get(messages_url, headers=api_headers, timeout=15)
        
        # গ্রাফ এপিআই রেসপন্স না করলে ব্যাকআপ ওডব্লিউএ আউটলুক এapi কল করবে
        if msg_res.status_code != 200:
            messages_url = "https://outlook.office.com/api/v2.0/me/messages?$search=\"Facebook\"&$top=1"
            msg_res = requests.get(messages_url, headers=api_headers, timeout=15)
            
        if msg_res.status_code != 200:
            return f"Connected, but failed to fetch inbox. Status: {msg_res.status_code}"
            
        messages = msg_res.json().get("value", [])
        if not messages:
            return "No recent Facebook emails found in this inbox."
            
        latest_message = messages[0]
        body_content = latest_message.get("body", {}).get("content", "") or latest_message.get("Body", {}).get("Content", "")
        subject = latest_message.get("subject", "") or latest_message.get("Subject", "")
        
        combined_text = f"{subject} {body_content}"
        
        # ইমেলের বডি থেকে ফেসবুক ওটিপির ডিজিট খোঁজার রিজেক্স (৫ বা ৬ ডিজিট)
        code_match = re.search(r'\b(\d{5,6})\b', combined_text)
        
        if code_match:
            return code_match.group(1)
        else:
            return "Facebook email found, but couldn't parse numeric code digits."
            
    except Exception as e:
        return f"System Connection Error: {str(e)}"

# ক্লাউড এপিআই এন্ডপয়েন্ট
@app.route('/get-code', methods=['POST'])
def get_code():
    data = request.json or {}
    raw_input = data.get('raw_input', '').strip()
    
    if not raw_input or '|' not in raw_input:
        return jsonify({'status': 'error', 'message': 'Invalid Data Line Format.'})
        
    parts = raw_input.split('|')
    if len(parts) < 4:
        return jsonify({'status': 'error', 'message': 'Missing fields. Format must be email|pass|token|client_id'})
        
    email = parts[0].strip()
    refresh_token = parts[2].strip()
    client_id = parts[3].strip()
    
    fb_code = extract_fb_code_via_api(email, refresh_token, client_id)
    
    if fb_code.isdigit():
        return jsonify({
            'status': 'success',
            'code': fb_code
        })
    else:
        return jsonify({
            'status': 'error',
            'message': fb_code
        })

if __name__ == '__main__':
    # ক্লাউড হোস্টিং (Render) এ অল-টাইম রান রাখার জন্য host '0.0.0.0' করা হয়েছে
    app.run(host='0.0.0.0', port=5000)

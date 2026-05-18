import os
import re
import imaplib
import email
from email.header import decode_header
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS এনাবেল করা হয়েছে যাতে আপনার GitHub Pages বা Local HTML থেকে রিকোয়েস্ট ব্লক না হয়
CORS(app)

# ৮ জিবি র‍্যামের জন্য অপ্টিমাইজড থ্রেড সংখ্যা (সর্বোচ্চ ১০-১৫টি থ্রেড রাখা নিরাপদ)
MAX_WORKERS = 10

def clean_text(text):
    """ইমেইল টেক্সট থেকে অপ্রয়োজনীয় ক্যারেক্টার এবং স্পেস ক্লিন করার ফাংশন"""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def extract_otp_from_html(html_body):
    """HTML বডি থেকে ৬ বা ৮ ডিজিটের কোড খোঁজার রেগুলার এক্সপ্রেশন"""
    # সাধারণত ফেসবুক বা ওটিপি কোডগুলো ৬ বা ৮ ডিজিটের হয়ে থাকে
    match = re.search(r'\b(\d{6,8})\b', html_body)
    if match:
        return match.group(1)
    return None

def fetch_otp_logic(raw_line):
    """মেইল লগইন এবং কোড বের করার মূল মেকানিজম"""
    try:
        # ইনপুট ফরম্যাট সাধারণত: email|password বা email|password|recovery_email
        parts = [p.strip() for p in raw_line.split('|')]
        if len(parts) < 2:
            return {"status": "failed", "message": "Invalid input format. Use: email|pass"}

        username = parts[0]
        password = parts[1]

        # Hotmail / Outlook IMAP সার্ভার কনফিগারেশন
        imap_server = "outlook.office365.com"
        
        # সার্ভারের সাথে কানেক্ট করা
        mail = imaplib.IMAP4_SSL(imap_server, 993)
        mail.login(username, password)
        
        # ইনবক্স সিলেক্ট করা
        mail.select("inbox")
        
        # সব ইমেইল সার্চ করা (সবচেয়ে লেটেস্ট মেইলটি আগে প্রসেস করার জন্য)
        status, messages = mail.search(None, "ALL")
        if status != "OK" or not messages[0]:
            mail.logout()
            return {"status": "failed", "message": "No messages found in Inbox"}

        mail_ids = messages[0].split()
        latest_mail_id = mail_ids[-1] # একদম শেষের (লেটেস্ট) মেইল আইডি

        # মেইল ডেটা ফেচ করা
        status, data = mail.fetch(latest_mail_id, "(RFC822)")
        if status != "OK":
            mail.logout()
            return {"status": "failed", "message": "Failed to fetch latest email data"}

        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # মেইলের বডি থেকে কন্টেন্ট রিড করা
        body_content = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if content_type == "text/html" and "attachment" not in content_disposition:
                    try:
                        body_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    except:
                        pass
                elif content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        pass
        else:
            body_content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

        # কোড এক্সট্রাক্ট করা
        cleaned_body = clean_text(body_content)
        otp_code = extract_otp_from_html(cleaned_body)

        mail.logout()

        if otp_code:
            return {"status": "success", "code": otp_code}
        else:
            return {"status": "failed", "message": "OTP code not found in the latest email"}

    except imaplib.IMAP4.error:
        return {"status": "failed", "message": "Login failed! Wrong username or password, or IMAP disabled."}
    except Exception as e:
        return {"status": "failed", "message": f"Error: {str(e)}"}

@app.route('/')
def home():
    return jsonify({"status": "running", "message": "Longisir VIP Portal Mail Backend is Active."})

@app.route('/get-code', encoding='utf-8', methods=['POST'])
def get_code():
    """ফ্রন্টএন্ড থেকে আসা রিকোয়েস্ট হ্যান্ডেল করার মেইন রাউট"""
    data = request.get_json()
    if not data or 'raw_input' not in data:
        return jsonify({"status": "failed", "message": "No raw input data provided"}), 400

    raw_input = data['raw_input'].strip()
    
    # Thread Pool ব্যবহার করে ব্যাকএন্ড টাস্ক এক্সিকিউট করা
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future = executor.submit(fetch_otp_logic, raw_input)
        result = future.result()

    return jsonify(result)

if __name__ == '__main__':
    # Render বা লোকাল হোস্টে রান করার জন্য পোর্ট কনফিগারেশন
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

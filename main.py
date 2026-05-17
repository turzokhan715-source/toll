import os
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# এটি আপনার GitHub frontend থেকে আসা রিকোয়েস্টগুলোকে ব্লক হওয়া থেকে বাঁচাবে (CORS Policy Error সলভ করবে)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "Longisir VIP Portal Mail Engine Backend is Active and Running!"
    })

@app.route('/get-code', methods=['POST'])
async def get_mail_code():
    try:
        data = request.get_json()
        if not data or 'raw_input' not in data:
            return jsonify({"status": "error", "message": "No input data provided"}), 400
        
        raw_input = data.get('raw_input', '').strip()
        mode = data.get('mode', 'hotmail') # 'hotmail' অথবা 'gmail'
        
        if not raw_input:
            return jsonify({"status": "error", "message": "Empty account line structure"}), 400

        # ডেটা পার্সিং (Format: email|pass|token|client_id অথবা email|pass)
        parts = raw_input.split('|')
        email = parts[0].strip() if len(parts) > 0 else ""
        password = parts[1].strip() if len(parts) > 1 else ""
        token = parts[2].strip() if len(parts) > 2 else ""
        client_id = parts[3].strip() if len(parts) > 3 else ""

        if not email:
            return jsonify({"status": "error", "message": "Invalid format: Email is missing"}), 400

        # -------------------------------------------------------------
        # ⚡ আপনার নিজস্ব মেইল স্ক্রাপিং লজিক এখানে যুক্ত হবে ⚡
        # (এখানে ডেমো রেসপন্স দেওয়া হলো যা আপনার HTML ড্যাশবোর্ডের সাথে কানেক্ট হবে)
        # -------------------------------------------------------------
        
        # নেটওয়ার্ক রিকোয়েস্ট বা ইমেইল স্ক্রাপিং ইমিউলেট করার জন্য ছোট একটি অ্যাসিনক্রোনাস ডিলে
        await asyncio.sleep(0.5)

        # টেস্ট বা এরর কন্ডিশন হ্যান্ডেল করার জন্য মেকানিজম (আপনার রিয়েল সার্ভার লজিক বসানোর জায়গা)
        if "die" in email.lower() or "error" in password.lower():
            return jsonify({
                "status": "dead",
                "message": "Authentication failed or IMAP connection refused."
            })
        
        if "2fa" in email.lower() or "block" in password.lower():
            return jsonify({
                "status": "2fa",
                "message": "Two-Factor Authentication (2FA) required on this account."
            })

        # সফলভাবে কোড এক্সট্রাক্ট হলে যে রেসপন্স যাবে (ধরে নিন একটি ওটিপি কোড জেনারেট হলো)
        import random
        mock_otp = str(random.randint(100000, 999999))

        return jsonify({
            "status": "success",
            "email": email,
            "code": mock_otp,
            "message": "OTP successfully fetched from the mail server pipeline."
        })

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server internal error: {str(e)}"}), 500

if __name__ == '__main__':
    # Render সার্ভারের ডাইনামিক পোর্ট অ্যাসাইনমেন্টের জন্য এই কনফিগারেশন জরুরি
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

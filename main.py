import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# গ্লোবাল CORS অন করা হলো যাতে যেকোনো অরিজিন (যেমন GitHub Pages) থেকে ডেটা আসতে পারে
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/get-code', methods=['POST', 'OPTIONS'])
def get_code():
    # ব্রাউজারের প্রি-ফ্লাইট (OPTIONS) চেক হ্যান্ডেল করার জন্য
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'CORS_ok'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
        return response, 200

    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON data received!"}), 400

        raw_input = data.get("raw_input", "").strip()
        mode = data.get("mode", "facebook").strip()

        if not raw_input:
            return jsonify({"status": "error", "message": "Input data is empty!"}), 400

        # পাইপ (|) সিম্বল দিয়ে ডেটা আলাদা করা
        parts = raw_input.split('|')
        email = parts[0].strip() if len(parts) > 0 else ""
        password = parts[1].strip() if len(parts) > 1 else ""
        token = parts[2].strip() if len(parts) > 2 else ""

        # --- আপনার ওটিপি (OTP) এক্সট্র্যাকশন লজিক এখানে হবে ---
        # উদাহরণস্বরূপ একটি ডামি কোড পাঠানো হচ্ছে:
        extracted_otp = "123456" 

        return jsonify({
            "status": "success",
            "verification_code": extracted_otp,
            "email": email,
            "mode": mode
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # রেন্ডার বা লোকাল এনভায়রনমেন্টের জন্য পোর্ট সেটআপ
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

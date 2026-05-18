import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 🌐 ফ্রন্টএন্ডের সাথে কানেকশন ঠিক রাখার জন্য CORS পলিসি ওপেন করা হলো
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ফ্রন্টএন্ড থেকে আসা ডাটার মডেল স্ট্রাকচার
class MailRequest(BaseModel):
    raw_input: str
    mode: str  # এখানে 'facebook' অথবা 'instagram' আসবে

@app.post("/get-code")
async def get_code(request: MailRequest):
    try:
        # ১. ইনপুট ডাটাকে পাইপ (|) সিম্বল দিয়ে ভেঙে আলাদা করা
        parts = request.raw_input.split('|')
        if not parts or len(parts) == 0:
            return {"status": "error", "message": "Invalid format! Data must be split by '|'"}
        
        email = parts[0].strip()
        password = parts[1].strip() if len(parts) > 1 else ""
        token = parts[2].strip() if len(parts) > 2 else ""
        uid = parts[3].strip() if len(parts) > 3 else ""

        # 🔍 এখানে আপনার আসল জিমেইল/আউটলুক লগইন এবং ওটিপি রিড করার লজিক বসবে
        # (নিচে উদাহরণস্বরূপ একটি ডামি কোড দেওয়া হলো যা ফেসবুক/ইনস্টাগ্রাম অনুযায়ী কাজ করবে)
        
        extracted_otp = ""
        
        if request.mode == "facebook":
            # 🔵 ফেসবুকের ওটিপি খোঁজার আসল কোড এখানে লিখবেন
            # উদাহরণ: extracted_otp = fetch_facebook_otp(email, password)
            extracted_otp = "FB-992813"  # টেস্ট করার জন্য ডামি ওটিপি
            
        elif request.mode == "instagram":
            # 🔮 ইনস্টাগ্রামের ওটিপি খোঁজার আসল কোড এখানে লিখবেন
            # उदाहरण: extracted_otp = fetch_instagram_otp(email, password)
            extracted_otp = "IG-482019"  # টেস্ট করার জন্য ডামি ওটিপি
            
        else:
            return {"status": "error", "message": "Unknown mode selection!"}

        # ২. সবকিছু সফল হলে ফ্রন্টএন্ডে ডাটা রিটার্ন করা
        return {
            "status": "success",
            "code": extracted_otp,
            "email": email,
            "uid": uid
        }

    except Exception as e:
        # কোনো কারণে ক্র্যাশ করলে এরর মেসেজ পাঠানো
        return {"status": "error", "message": f"Python Server Error: {str(e)}"}

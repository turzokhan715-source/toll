from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class MailRequest(BaseModel):
    raw_input: str
    mode: str  # এখানে ফ্রন্টএন্ড থেকে 'facebook' অথবা 'instagram' আসবে

@app.post("/get-code")
async def get_code(request: MailRequest):
    try:
        # ফ্রন্টএন্ডের পাঠানো পুরো লাইনটি আলাদা করা হচ্ছে
        parts = request.raw_input.split('|')
        email = parts[0]
        password = parts[1] if len(parts) > 1 else ""
        token = parts[2] if len(parts) > 2 else ""
        
        # ফ্রন্টএন্ডের সিলেক্ট করা মোড চেক করা
        if request.mode == "facebook":
            # 🔵 এখানে আপনার ফেসবুকের ওটিপি বের করার কোড
            extracted_otp = "123456" # উদাহরণ (আপনার আসল লজিক বসবে)
            
        elif request.mode == "instagram":
            # 🔮 এখানে আপনার ইনস্টাগ্রামের ওটিপি বের করার কোড
            extracted_otp = "654321" # উদাহরণ (আপনার আসল লজিক বসবে)
            
        else:
            return {"status": "error", "message": "Invalid platform mode selected"}

        # সবকিছু ঠিক থাকলে ফ্রন্টএন্ডে সাকসেস রেসপন্স পাঠানো
        return {"status": "success", "code": extracted_otp}

    except Exception as e:
        return {"status": "error", "message": f"Processing failed: {str(e)}"}

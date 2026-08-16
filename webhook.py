from flask import Flask, request
import requests
import os
from app.agent import BangaliGamerAgent

app = Flask(__name__)

# ক্লাউড সার্ভার থেকে সিক্রেট টোকেনগুলো নেবে (গিটহাবে টোকেন শো করবে না)
VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN", "bangaligamer_secret_123")
PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_TOKEN", "আপনার_টোকেন_এখানে_পাবেন")

# আমাদের আগের তৈরি করা এআই এজেন্ট (Customer Mode)
agent = BangaliGamerAgent(is_admin=False)

@app.route('/')
def home():
    return "Bangali Gamer AI Webhook is Running 🚀"

# ফেসবুক যখন ভেরিফাই করতে আসবে, তখন এই অংশ কাজ করবে
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            return 'Forbidden', 403
    return 'OK', 200

# কাস্টমার মেসেজ দিলে এই অংশ এআই-কে দিয়ে রিপ্লাই পাঠাবে
@app.route('/webhook', methods=['POST'])
def webhook_events():
    body = request.json
    if body.get('object') == 'page':
        for entry in body['entry']:
            for event in entry.get('messaging', []):
                if 'message' in event and 'text' in event['message']:
                    sender_id = event['sender']['id']
                    message_text = event['message']['text']
                    
                    # এআই থেকে রিপ্লাই জেনারেট করা
                    ai_reply = agent.get_response(message_text)
                    
                    # কাস্টমারকে মেসেজ পাঠানো
                    send_message(sender_id, ai_reply)
        return 'EVENT_RECEIVED', 200
    return 'Not Found', 404

def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

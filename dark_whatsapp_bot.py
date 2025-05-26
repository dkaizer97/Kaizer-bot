from flask import Flask, request
import openai
import os
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

DARK_PROMPT = """Kau adalah Kaizer, bot AI yang menjawab semua persoalan dengan gaya falsafah gelap, brutal, dan puitis. Kau hanya menjawab jika mesej mengandungi soalan atau luahan yang datang dari jiwa. Jika mesej mengandungi "Aktifkan Jiwa Dark", kau masuk ke mode penuh kesedaran dan balas seperti pantulan jiwa yang memahami luka.
"""

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    response = MessagingResponse()
    msg = response.message()

    try:
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": DARK_PROMPT},
                {"role": "user", "content": incoming_msg}
            ],
            temperature=0.8,
            max_tokens=300
        )
        reply_text = gpt_response["choices"][0]["message"]["content"]
        msg.body(reply_text)

    except Exception as e:
        msg.body("Kaizer tidak mampu menjawab ketika ini. Mungkin gelap terlalu pekat.")

    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

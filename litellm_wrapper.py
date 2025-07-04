from dotenv import load_dotenv

load_dotenv()  # <-- Loads .env file into environment variables

from litellm import completion
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

FLOWISE_API_URL = os.environ.get("FLOWISE_API_URL")
if not FLOWISE_API_URL:
    raise ValueError("FLOWISE_API_URL environment variable not set.")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message')

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Prepare the payload for the Flowise API
        flowise_payload = {"question": user_message}  # Adjust 'question' if needed

        # Make the request to the Flowise API
        response = requests.post(FLOWISE_API_URL, json=flowise_payload)

        if response.status_code != 200:
            return jsonify({"error": f"Flowise API error: {response.status_code} - {response.text}"}), 500

        flowise_response = response.json()
        bot_response = flowise_response.get('text')  # Adjust 'text' if needed

        if not bot_response:
            return jsonify({"error": "No response from Flowise API"}), 500

        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Or any port you prefer
import requests
from flask import Flask, render_template, request, jsonify
from pyngrok import ngrok
import google.generativeai as palm

app = Flask(__name__)

# Set the Ngrok auth token (get it from https://dashboard.ngrok.com/auth)
ngrok.set_auth_token("2NJS8jGEf5b69SKspLtaLLYnvN7_81bvYBKyB4g5XzNBBuXzD")

def run_ngrok():
    print("Starting Ngrok...")
    # Open a Ngrok tunnel to the dev server
    public_url = ngrok.connect(5000)

    # Print Ngrok URL to the terminal
    print(f"Ngrok URL: {public_url}")

    return public_url

def generate_ai_response(query):
    YOUR_API_KEY = "AIzaSyAJwFxWeIaLr-D_w8eyoYrE6-eB3TC-RFY"
    palm.configure(api_key=YOUR_API_KEY)

    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name

    completion = palm.generate_text(
        model=model,
        prompt=query,
        temperature=0.6,
        max_output_tokens=1600,
    )
    return completion.result


@app.route('/')
def home():
    return render_template('client.html')  # Render the HTML template

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.json
    query = data.get('query', '')
    print(f"Received query: {query}")

    response = generate_ai_response(query)

    return jsonify({"response": response})

def run_flask():
    app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)

if __name__ == '__main__':
    ngrok_url = run_ngrok()
    print(f"Your ngrok public URL: {ngrok_url}")

    # Start Flask server in a separate thread
    import threading
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

from core.bot import Bot
from flask import Flask, request
from flask_cors import CORS
from core.agent import Agent
import threading
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)
CORS(app)

Agent_instance = Agent(api_key=OPENAI_API_KEY)
results = {}

@app.post('/rest/v1/query')
def query_begin():
    request_id = str(uuid.uuid4())
    results[request_id] = {
        "status": "Processing",
        "response": None
    }

    message = request.json.get('message')

    def worker():
        try:
            response = Agent_instance.query(message, callback=lambda r: results.update({request_id: {"status": "Completed", "response": r}}))
        except Exception as e:
            results.update({request_id: {"status": "Failed", "response": str(e)}})

    threading.Thread(target=worker, daemon=True).start()
    return request_id, 202



@app.get('/rest/v1/query/<request_id>')
def query_status(request_id):
    if request_id in results:
        return results[request_id], 200
    else:
        return {"error": "Request ID not found"}, 404



if __name__ == '__main__':
    bot = Bot(BOT_TOKEN, agent=Agent_instance)
    threading.Thread(target=bot.start).start()
    app.run(port=5000, debug=True)
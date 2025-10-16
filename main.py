# main.py — CoH AI Chatbot (Flask, using existing trained data + .env variables)

from flask import Flask, render_template, request, jsonify
from vanna.chromadb import ChromaDB_VectorStore
from vanna.mistral import Mistral
from dotenv import load_dotenv
import os

# load env variables
load_dotenv()

# VannaAI Setup
class MyVanna(ChromaDB_VectorStore, Mistral):
    def __init__(self, config=None):
        # Load your existing ChromaDB vector store (no retraining)
        ChromaDB_VectorStore.__init__(self, config=config)
        Mistral.__init__(self, config={
            'api_key': os.getenv('MISTRAL_API_KEY'),
            'model': 'mistral-tiny'
        })

vn = MyVanna()

# ------MySQL Connection
# vn.connect_to_mysql(
#     host=os.getenv('MYSQL_HOST'),
#     dbname=os.getenv('MYSQL_DBNAME'),
#     user=os.getenv('MYSQL_USER'),
#     password=os.getenv('MYSQL_PASSWORD'),
#     port=int(os.getenv('MYSQL_PORT'))
# )

print("✅ Loaded Vanna + Mistral with existing trained data.")

# Flask setup
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['question']
    messages = [{"role": "user", "content": user_input}]
    response = vn.submit_prompt(messages)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)

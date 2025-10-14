# main.py — CoH AI Chatbot (Flask, using existing trained data)

from flask import Flask, render_template, request, jsonify
from vanna.chromadb import ChromaDB_VectorStore
from vanna.mistral import Mistral

# ------------------ Vanna Setup ------------------
class MyVanna(ChromaDB_VectorStore, Mistral):
    def __init__(self, config=None):
        # Load your existing ChromaDB vector store (no retraining)
        ChromaDB_VectorStore.__init__(self, config=config)
        Mistral.__init__(self, config={
            'api_key': 'hzDm5IM0efQKPO7DYKT5I6cu8qN9y1iA',
            'model': 'mistral-tiny'
        })

vn = MyVanna()

# Connect to your existing MySQL (only if needed for query context)
# vn.connect_to_mysql(
#     host='localhost',
#     dbname='CoH',
#     user='root',
#     password='et1138RWU',
#     port=3306
# )

print("✅ Loaded Vanna + Mistral with existing trained data.")

# ------------------ FLASK APP ------------------
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

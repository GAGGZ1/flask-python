from flask import Flask, jsonify, request, render_template
from difflib import get_close_matches
import json

app = Flask(__name__)

# Load the knowledge base from the JSON file


@app.route('/')
def index():
    return render_template('index.html')


def load_knowledge_base(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


knowledge_base = load_knowledge_base('knowledge_base.json')

# Route for querying the chatbot


# Modify the chatbot route to respond with JSON
@app.route('/chatbot', methods=['GET'])
def chatbot():
    user_input = request.args.get('query')

    if not user_input:
        return jsonify({"response": "No query provided."})

    best_match = get_close_matches(
        user_input, [entry["question"] for entry in knowledge_base], n=1, cutoff=0.6)

    if best_match:
        answer = get_answer_for_question(best_match[0], knowledge_base)
        return jsonify({"response": answer})
    else:
        return jsonify({"response": "I don't know the answer. Can you teach me?"})

    best_match = get_close_matches(
        user_input, [entry["question"] for entry in knowledge_base], n=1, cutoff=0.6)


# Helper function to get the answer for a question


def get_answer_for_question(question, knowledge_base):
    for entry in knowledge_base:
        if entry["question"] == question:
            return entry["answer"]


if __name__ == '__main__':
    app.run(debug=True, port=8000)

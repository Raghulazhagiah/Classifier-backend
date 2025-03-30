from flask import Flask, request, jsonify
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

app = Flask(__name__)

def summarize_text(text):
    num_lines = len(text.split("\n"))
    num_sentences = 5 if num_lines > 10 else 3

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)

    return [str(sentence) for sentence in summary]

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' parameter"}), 400

    text = data['text']
    summary = summarize_text(text)
    
    return jsonify({"summary": summary})

# Vercel requires this export
def handler(event, context):
    return app(event, context)

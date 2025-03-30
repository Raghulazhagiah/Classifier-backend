from flask import Flask, request, jsonify
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

app = Flask(__name__)

def summarize_text(text):
    """Summarizes text based on the number of lines."""
    num_lines = len(text.split("\n"))
    num_sentences = 5 if num_lines > 10 else 3  # 5 sentences if more than 10 lines, else 3

    # Parse text
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()

    # Generate summary
    summary = summarizer(parser.document, num_sentences)

    # Convert summary sentences to a list
    return [str(sentence) for sentence in summary]

@app.route('/summarize', methods=['POST'])
def summarize():
    """API endpoint to summarize text."""
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' parameter"}), 400

    text = data['text']
    summary = summarize_text(text)
    
    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)

import sys
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def summarize_text(text):
    num_lines = len(text.split("\n"))
    num_sentences = 5 if num_lines > 10 else 3

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)

    return " ".join(str(sentence) for sentence in summary)

if __name__ == "__main__":
    input_text = sys.argv[1]  # Get text from command line args
    print(summarize_text(input_text))

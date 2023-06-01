from flask import Flask, render_template, request, jsonify
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form['text']

    queries = generate_queries(text)
    passage = retrieve_passage(text)

    return jsonify({'passage': passage, 'queries': queries})

def generate_queries(text):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')

    doc = nlp(text)

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    sorted_word_frequencies = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
    top_words = [word[0] for word in sorted_word_frequencies[:5]]
    return top_words

def retrieve_passage(text):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')

    doc = nlp(text)

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    sentence_tokens = [sent for sent in doc.sents]

    sentence_score = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_score.keys():
                    sentence_score[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_score[sent] += word_frequencies[word.text.lower()]

    select_length = int(len(sentence_tokens) * 0.3)
    summary = nlargest(select_length, sentence_score, key=sentence_score.get)

    final_summary = [word.text for word in summary]
    return ' '.join(final_summary)

if __name__ == '__main__':
    app.run()

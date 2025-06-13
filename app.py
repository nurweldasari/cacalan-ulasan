from flask import Flask, request, Response
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import json
import os

app = Flask(__name__)

# Load model dan tokenizer (meskipun tidak digunakan)
model = load_model('label_cacalan.h5')
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

# Parameter (tidak digunakan, hanya sebagai formalitas)
max_len = 20
vocab_size = len(tokenizer.word_index) + 1

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Validasi input
    if not data or 'review' not in data or 'rating' not in data:
        return Response(json.dumps({
            "error": "Request JSON harus memiliki key 'review' dan 'rating'"
        }), mimetype='application/json', status=400)

    review_text = data['review'].strip()
    if not review_text:
        return Response(json.dumps({
            "error": "Teks review tidak boleh kosong"
        }), mimetype='application/json', status=400)

    try:
        rating = int(data['rating'])
    except ValueError:
        return Response(json.dumps({
            "error": "Rating harus berupa angka 1 sampai 5"
        }), mimetype='application/json', status=400)

    if rating < 1 or rating > 5:
        return Response(json.dumps({
            "error": "Rating harus antara 1 sampai 5"
        }), mimetype='application/json', status=400)

    # Tentukan kategori
    kategori = "Buruk" if rating <= 2 else "Baik"

    # Bangun response
    response_data = {
        "review": review_text,
        "rating": rating,
        "kategori": kategori
    }

    return Response(json.dumps(response_data), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 7860)))
    app.run(debug=True)

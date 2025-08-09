# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from rsa_utils import generate_keypair, encrypt_int as encrypt, decrypt_int as decrypt, text_to_ints, ints_to_text

app = Flask(__name__)
CORS(app)  # allow Vite dev server

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.post("/generate_keys")
def generate_keys():
    data = request.get_json(silent=True) or {}
    bits_per_prime = int(data.get("bits_per_prime", 32))
    keys = generate_keypair(bits_per_prime=bits_per_prime)
    # Return big integers as strings to avoid JS precision loss
    return jsonify({
        "p": str(keys["p"]),
        "q": str(keys["q"]),
        "n": str(keys["n"]),
        "phi": str(keys["phi"]),
        "e": str(keys["e"]),
        "d": str(keys["d"]),
        "bits_per_prime": bits_per_prime
    })

@app.post("/encrypt")
def encrypt_route():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", ""))
    # accept e,n as string or number
    e = int(data["e"])
    n = int(data["n"])
    m_ints = text_to_ints(message, n)
    c_ints = [encrypt(m, e, n) for m in m_ints]
    # return cipher as strings
    return jsonify({ "cipher": [str(c) for c in c_ints] })

@app.post("/decrypt")
def decrypt_route():
    data = request.get_json(silent=True) or {}
    # accept cipher elements as strings or numbers
    cipher = [int(x) for x in data["cipher"]]
    d = int(data["d"])
    n = int(data["n"])
    m_ints = [decrypt(c, d, n) for c in cipher]
    plaintext = ints_to_text(m_ints)
    return jsonify({ "message": plaintext })

if __name__ == "__main__":
    # 127.0.0.1:5000 by default
    app.run(port=5000, debug=True)

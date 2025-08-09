from flask import Flask, request, jsonify
from flask_cors import CORS
from rsa_utils import generate_keypair, encrypt_int, decrypt_int


app = Flask(__name__)
CORS(app) # Allow request from dev server 

@app.post("/generate_keys")
def generate_keys():
    """
    Body (JSON): { "bits": 512, "p": optional int, "q": optional int}
    Returns: {p, q, n, phi, e, d, bits}
    NOTE: q and p are returned ONLY for RSA learning purposes.
    """
    data = request.get_json(silent=True) or {}
    bits = int(data.get('bits', 512))
    q = data.get ('q')
    p = data.get ('p')
    try:
        result = generate_keypair(bits=bits,p=p,q=q)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": star(e)}), 400


    @app.post("/encrypt")
    def encrypt():
        """
        Body (JSON): {"message": "HELLO", "e": int, "n": int}
        Returns: {"cipher": [int, int, ...] }
        """

        data =request.get_json() or {}
        message = str(data.get("message", ""))
        e = int(data["e"])
        n = int(data["n"])

        # simple encoding: 1 byte per  block
        m_ints = text_to_ints(message,n)
        c_ints = [encrypt_int(m,e,n) for m in m_ints]
        return jsonify({"cipher": c_ints})


    @app.post("/decrypt")
    def decrypt():
        """
        Body (JSON): { "cipher": [ints], "d": int, "n": int }
        Returns: { "message": "..." }
        """

        data = request.get_json() or {}
        cipher = list(map(int,data["cipher"]))
        d = int(data["d"])
        n = int(data["n"])

        m_ints = [decrypt_int(c,d,n) for c in cipher]
        plaintext = ints_to_text(m_ints)
        return jsonify({"message": plaintext})

    if __name__ == "__main__":
        # Runs on http://localhost:5000
        app.run(port=5000, debug=True)

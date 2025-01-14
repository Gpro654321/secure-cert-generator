from flask import Flask, request, render_template_string
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key

app = Flask(__name__)

# Load your public key
with open("public_key.pem", "rb") as key_file:
    public_key = load_pem_public_key(key_file.read())

@app.route("/", methods=["GET", "POST"])
def verify_signature():
    message = ""
    signature_hex = ""
    result_message = ""
    result_color = ""

    # Handling GET request (with query parameters)
    if request.method == "GET":
        message = request.args.get("message", "")
        signature_hex = request.args.get("signature", "")

        if message and signature_hex:
            try:
                # Convert hex signature back to bytes
                signature = bytes.fromhex(signature_hex)

                # Verify the signature
                public_key.verify(
                    signature,
                    message.encode(),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                result_message = "Signature is valid!"
                result_color = "green"
            except Exception as e:
                result_message = f"Signature verification failed: {str(e)}"
                result_color = "red"

    # Handling POST request (from the form submission)
    elif request.method == "POST":
        message = request.form.get("message", "")
        signature_hex = request.form.get("signature", "")

        if message and signature_hex:
            try:
                # Convert hex signature back to bytes
                signature = bytes.fromhex(signature_hex)

                # Verify the signature
                public_key.verify(
                    signature,
                    message.encode(),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                result_message = "YES, CERTIFICATE WAS ISSUED BY AIMER CONSORTIUM"
                result_color = "green"
            except Exception as e:
                result_message = f"NO CERTIFICATE WAS NOT ISSUED BY AIMER CONSORTIUM: {str(e)}"
                result_color = "red"

    return render_template_string("""
        <html>
            <head>
                <title>AIMER CONSORTIUM CERTIFICATE AUTHENTICITY VERIFICATION</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f4f7fc;
                    }
                    .container {
                        width: 50%;
                        margin: 50px auto;
                        background-color: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }
                    h2 {
                        color: #333;
                        text-align: center;
                    }
                    label {
                        font-weight: bold;
                        margin-bottom: 5px;
                    }
                    input[type="text"] {
                        width: 100%;
                        padding: 10px;
                        margin: 10px 0;
                        border-radius: 5px;
                        border: 1px solid #ddd;
                        box-sizing: border-box;
                    }
                    input[type="submit"] {
                        width: 100%;
                        padding: 10px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        font-size: 16px;
                    }
                    input[type="submit"]:hover {
                        background-color: #45a049;
                    }
                    .result {
                        margin-top: 20px;
                        padding: 10px;
                        border-radius: 5px;
                        text-align: center;
                    }
                    .green { background-color: #d4edda; color: #155724; }
                    .red { background-color: #f8d7da; color: #721c24; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Signature Verification</h2>

                    <form method="POST">
                        <label for="message">Message:</label>
                        <input type="text" id="message" name="message" value="{{ message }}" required>

                        <label for="signature">Signature (Hex):</label>
                        <input type="text" id="signature" name="signature" value="{{ signature_hex }}" required>

                        <input type="submit" value="Verify">
                    </form>

                    {% if result_message %}
                        <div class="result {{ result_color }}">
                            <p><strong>Message:</strong> {{ message }}</p>
                            <p>{{ result_message }}</p>
                        </div>
                    {% endif %}
                </div>
            </body>
        </html>
    """, message=message, signature_hex=signature_hex, result_message=result_message, result_color=result_color)

if __name__ == "__main__":
    app.run(debug=True)


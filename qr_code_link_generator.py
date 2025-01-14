import qrcode
import urllib.parse

def generate_qr_code(url, output_path="qr_code.png"):
    # Generate QR code with the URL
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    print(f"QR code saved: {output_path}")

# Example usage
from digital_signature import sign_certificate

participant_data = b"John Doe | johndoe@example.com"
signature = sign_certificate(participant_data)

# URL encode the message and signature
encoded_message = urllib.parse.quote(participant_data.decode())
encoded_signature = urllib.parse.quote(signature.hex())

# Generate URL with encoded parameters
url = f"?https://drgenaigpt.pythonanywhere.com/?message={encoded_message}&signature={encoded_signature}"

generate_qr_code(url)


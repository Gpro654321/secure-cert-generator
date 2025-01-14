import os
import csv
from PIL import Image, ImageDraw, ImageFont
import urllib.parse


#from digital_signature import sign_certificate
#from qr_code_generator import generate_qr_code 
from test_signature_verifier import sign_message, verify_signature
from qr_code_generator import generate_qr_code
from qr_code_link_generator import generate_qr_code


def generate_certificate(name, output_path, template_path="Brainer_Cert_Template.png"):
    # Load the certificate template
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)
    
    # Define font and size
    font = ImageFont.truetype("./arial.ttf", size=40)  # Replace with your desired font file
    
    # Specify position to add text (We will calculate this based on text width)
    width, height = image.size
    actual_width = width - 265
    
    # Calculate the bounding box of the text
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Find the x position to center the text horizontally
    x_position = ((actual_width - text_width) // 2) + 265
    
    # Specify the y position to add text
    y_position = 335  # Adjust based on template design
    
    # Text color
    text_color = (0, 0, 0)  # Black color
    
    # Add text (name) to the template
    draw.text((x_position, y_position), name, fill=text_color, font=font)
    
    # Save the certificate as a PNG
    temp_output = output_path.replace(".png", ".png")
    image.save(temp_output, dpi=(300,300))
    
    # Convert PNG to PDF
    #image = Image.open(temp_output)
    #pdf_path = output_path
    #image.convert("RGB").save(pdf_path)
    
    # Remove the temporary PNG file
    #os.remove(temp_output)
    print(f"Certificate saved: {temp_output}")


def generate_certificate_with_qr(name, email, template_path="Brainer_Cert_Template.png"):


    # Load the certificate template
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)
    
    # Define font and size
    font = ImageFont.truetype("./arial.ttf", size=40)  # Replace with your desired font file
    
    # Add name
    width, height = image.size
    actual_width = width - 265
    bbox = draw.textbbox((0, 0), name, font=font)
    x_position = ((actual_width - (bbox[2] - bbox[0])) // 2) + 265
    draw.text((x_position, 335), name, fill=(0, 0, 0), font=font)
    

    # Generate signature and QR code
    participant_data = f"{name} | {email}"
    participant_data_as_string = f"{name} | {email}"
    #signature = sign_certificate(participant_data)
    private_key_path = './private_key.pem'
    signature = sign_message(private_key_path, participant_data)
    print("Signature:", signature.hex())
    print(type(signature))
    qr_code_path = "qr_code.png"


    # URL encode the message and signature
    encoded_message = urllib.parse.quote(participant_data)
    encoded_signature = urllib.parse.quote(signature.hex())

    # Generate URL with encoded parameters
    url = f"https://drgenaigpt.pythonanywhere.com/?message={encoded_message}&signature={encoded_signature}"
    
    generate_qr_code(url)

    # generate_qr_code(name, email, participant_data_as_string,signature, output_path=qr_code_path)
    
    # Add QR code to the certificate
    qr_code = Image.open(qr_code_path)
    qr_code = qr_code.resize((267, 267))  # Resize QR code
    image.paste(qr_code, (0, 0))  # Place at bottom-left corner
    
    # Save the certificate
    output_path = f"./certificates/{name.replace(' ', '-')}~{email}.pdf"

	# verify signature


    public_key_path = "./public_key.pem"
    is_valid = verify_signature(public_key_path, participant_data, signature)

    print("Is the signature valid?", is_valid)

    image.save(output_path, "PDF", resolution=500.0)

    print(f"Certificate saved: {output_path}")
    print("------------------")



def generate_certificates_from_csv(csv_file, template_path="Brainer_Cert_Template.png"):
    # Create the certs directory if it doesn't exist
    certs_dir = "./certificates"
    if not os.path.exists(certs_dir):
        os.makedirs(certs_dir)
    
    # Read the CSV file
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        
        for row in reader:
            if len(row) < 3:
                continue  # Skip rows with insufficient data
            
            name = row[1]  # Second column: Name
            email = row[2]  # Third column: Email
            
            # Generate the output file path
            filename = f"{name.replace(' ', '-')}_{email}.pdf"
            output_path = os.path.join(certs_dir, filename)

            
            
            # Generate the certificate
            # generate_certificate(name, output_path, template_path=template_path)
            generate_certificate_with_qr(name, email, template_path="Brainer_Cert_Template.png")

# Example usage
csv_file_path = "Brainer_4.0.csv"  # Replace with your actual CSV file path
generate_certificates_from_csv(csv_file_path)


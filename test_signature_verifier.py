from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

# Function to load keys from files
def load_private_key_from_file(file_path):
    """
    Load a private key from a PEM file.
    """
    with open(file_path, "rb") as key_file:
        return load_pem_private_key(key_file.read(), password=None)

def load_public_key_from_file(file_path):
    """
    Load a public key from a PEM file.
    """
    with open(file_path, "rb") as key_file:
        return load_pem_public_key(key_file.read())

# Function to digitally sign a message
def sign_message(private_key_path, message):
    """
    Sign a message using the private key.

    Args:
        private_key: Private key object.
        message: String message to be signed.

    Returns:
        The digital signature as bytes.
    """
    private_key = load_private_key_from_file(private_key_path)

    signature = private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

# Function to verify a signature
def verify_signature(public_key_path, message, signature):
    """
    Verify a digital signature using the public key.

    Args:
        public_key: Public key object.
        message: String message whose signature is being verified.
        signature: Digital signature to verify.

    Returns:
        True if the signature is valid, False otherwise.
    """
    public_key = load_public_key_from_file(public_key_path)    

    try:
        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        return False

# Example usage
if __name__ == "__main__":
    # File paths to your private and public keys
    private_key_file_path = "./private_key.pem"  # Replace with the actual filename
    public_key_file_path = "./public_key.pem"   # Replace with the actual filename

    # Load keys
    #private_key = load_private_key_from_file(private_key_file)
    #public_key = load_public_key_from_file(public_key_file)

    # Message to sign
    message = "a"

    # Digitally sign the message
    signature = sign_message(private_key_file_path, message)
    print("Signature:", signature.hex())
    print(type(signature))
    #print("len of original signature", len(signature))

    #signature_bytearray = bytearray(signature)
    #tamperted_signature = signature_bytearray[-1] ^ 0xFF


    
    # Verify the signature
    #signature = bytes(tamperted_signature) 
    #print("Modified signature", signature.hex())
    #print("len of modified sign", len(signature))
    is_valid = verify_signature(public_key_file_path, message, signature)
    print("Is the signature valid?", is_valid)

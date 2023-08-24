from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import keywrap
from cryptography.hazmat.primitives import ciphers

def identify_encryption_type(data):
    encryption_types = []

    # Try to identify symmetric encryption
    symmetric_algorithms = [
        ("AES", ciphers.algorithms.AES),
        # Add more symmetric algorithms here
    ]

    for alg_name, alg_cls in symmetric_algorithms:
        try:
            key = b'\x00' * alg_cls.key_sizes[0]
            cipher = alg_cls(key)
            cipher.decryptor().update(data)
            encryption_types.append(f"Symmetric: {alg_name}")
        except Exception:
            pass

    # Try to identify asymmetric encryption
    asymmetric_algorithms = [
        ("RSA", serialization.NoEncryption, padding.PKCS1v15),
        # Add more asymmetric algorithms here
    ]

    for alg_name, enc_scheme, padding_scheme in asymmetric_algorithms:
        try:
            private_key = serialization.load_pem_private_key(data, password=None)
            private_key.decrypt(data, padding_scheme())
            encryption_types.append(f"Asymmetric: {alg_name}")
        except Exception:
            pass

    return encryption_types

def read_encrypted_log_file(log_file_path):
    try:
        with open(log_file_path, 'rb') as log_file:
            encrypted_data = log_file.read()
            encryption_types = identify_encryption_type(encrypted_data)
            if encryption_types:
                print("Possibly encrypted with:")
                for enc_type in encryption_types:
                    print(enc_type)
            else:
                print("No identifiable encryption found.")
    except FileNotFoundError:
        print(f"O arquivo '{log_file_path}' não foi encontrado.")

if __name__ == "__main__":
    log_file_path = "/var/log/auth.log"  # Substitua pelo caminho do seu arquivo de log criptografado
    read_encrypted_log_file(log_file_path)


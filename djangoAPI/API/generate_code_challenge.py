import base64
import hashlib
import os

# Generate the code_verifier (random string of 43-128 characters)
code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8').rstrip("=")

# Generate the code_challenge (SHA-256 of the code_verifier)
code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8').rstrip("=")

print("Code Verifier:", code_verifier)
print("Code Challenge:", code_challenge)

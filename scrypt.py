import os


secret = os.getenv('SECRET_KEY')

print(f"This is a test for secrets {secret}")
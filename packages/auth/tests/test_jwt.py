from auth.jwt import create_access_token, decode_access_token
from datetime import timedelta

subject = "user-123"
secret_key = "secret-for-testing-only"
expires_delta = timedelta(minutes=15)

access_token = create_access_token(subject, secret_key, expires_delta)
decoded_access_token = decode_access_token(access_token, secret_key)

print("Access Token:")
print(access_token)

print()

print("Decoded Payload:")
print(decoded_access_token)
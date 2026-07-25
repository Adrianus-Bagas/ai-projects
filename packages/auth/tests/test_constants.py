from auth.constants import AuthErrorCode


code = AuthErrorCode.INVALID_CREDENTIALS

print(code)
print(code.value)
print(isinstance(code, str))
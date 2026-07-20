from auth.password import hash_password, verify_password
print(verify_password("rahasia123", hash_password("rahasia123")))
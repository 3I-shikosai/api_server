import hashlib


def encode(raw_str: str) -> str:
    return hashlib.sha256(raw_str.encode()).hexdigest()


password = input("Password: ")

encoded = encode(password)

print(encoded)

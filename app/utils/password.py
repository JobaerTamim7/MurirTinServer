import bcrypt

def password_hashing(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password=password.encode(),salt=salt)

    return hashed_pass.decode()

def verify_pass(password:str , hashed_password: str) -> bool:
    result: bool = bcrypt.checkpw(password.encode(),hashed_password.encode())

    return result
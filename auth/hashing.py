import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def preprocess_password(password: str):

    # Convert long password into fixed length hash
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def hash_password(password: str):

    safe_password = preprocess_password(password)

    return pwd_context.hash(safe_password)


def verify_password(
    plain_password: str,
    hashed_password: str
):

    safe_password = preprocess_password(
        plain_password
    )

    return pwd_context.verify(
        safe_password,
        hashed_password
    )
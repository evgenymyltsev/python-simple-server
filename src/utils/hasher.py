"""This module contains a Hasher class that provides methods for generating and verifying password hashes.

Classes:
    Hasher: A class that provides methods for generating and verifying
        password hashes.

Attributes:
    pwd_context (CryptContext): An instance of the CryptContext class from
        the passlib library, which is used to generate and verify password
        hashes.

Methods:
    get_password_hash(password): Generate a hash of a given password.

"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    """
    Hasher class that provides methods for generating and verifying password hashes.

    Methods:
        get_password_hash(password: str) -> str:
            Generate a hash of a given password.
        verify_password(plain_password: str, hashed_password: str) -> bool:
            Verify a given plain password against a hashed password.
    """

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Generate a hash of a given password.

        Args:
            password (str): The plain password to hash.

        Returns:
            str: The hashed password.
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a given plain password against a hashed password.

        Args:
            plain_password (str): The plain password to verify.
            hashed_password (str): The hashed password to verify against.

        Returns:
            bool: True if the plain password matches the hashed password, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)

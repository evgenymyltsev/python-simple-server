"""This module defines exceptions that can be raised by the application."""

from fastapi import HTTPException, status


class InternalServerError(HTTPException):
    """InternalServerError.

    Args:
        HTTPException (_type_): _description_
    """

    def __init__(self: "InternalServerError") -> None:
        """Exception that indicates an unexpected error due to a bug in our code.

        Attributes:
            None

        Args:
            None

        Returns:
            None

        Raises:
            InternalServerError: When an unexpected error occurs.

        """
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": None,
                "detail": "Something went wrong",
            },
        )

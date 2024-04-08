from fastapi import HTTPException, status


class InternalServerError(HTTPException):
    def __init__(self, error) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": None,
                "detail": "Something went wrong",
            },
        )
        self.log(error)

    def log(self, error):
        print(">>>>>>>", error)

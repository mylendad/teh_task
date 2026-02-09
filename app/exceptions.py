from typing import Optional

from fastapi import HTTPException, status


class ShortenerException(HTTPException):
    status_code = 500
    detail = "An unknown error occurred"

    def __init__(self, status_code: Optional[int] = None, detail: Optional[str] = None):
        if status_code:
            self.status_code = status_code
        if detail:
            self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class ShortUrlCreatedException(ShortenerException):
    status_code = status.HTTP_201_CREATED
    detail = "Short URL created successfully"


class ShortUrlRedirectException(ShortenerException):
    status_code = status.HTTP_302_FOUND
    detail = "Redirecting to original URL"


class ShortCodeCollisionException(ShortenerException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to generate unique short code"


class ShortUrlNotFoundException(ShortenerException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Короткий URL не найден"

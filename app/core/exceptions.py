from fastapi import HTTPException

class YelpAPIError(HTTPException):
    def __init__(self):
        super().__init__(status_code=502, detail="Yelp API failed")
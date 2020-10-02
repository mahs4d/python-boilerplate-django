class CustomApiError(Exception):
    """
    a general easily customizable exception for apis
    """

    def __init__(self, status_code: int, message: str, code: str):
        super().__init__(message)
        
        self.status_code = status_code
        self.message = message
        self.code = code

class CustomError(Exception):
    def __init__(self, name="Error", cause=None, message="An error occurred", code=1):
        super().__init__(message)
        self.name = name
        self.message = message
        self.cause = cause
        self.code = code

    def __str__(self):
        return f"{self.name}: {self.message} (Cause: {self.cause}, Code: {self.code})"

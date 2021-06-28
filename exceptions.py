class APIKeyError(Exception):

    def __init__(self, message='Your API key is invalid.'):
        self.message = message
        super().__init__(self.message)

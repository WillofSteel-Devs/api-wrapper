class NotInAlliance(Exception):
    def __init__(self) -> None:
        super().__init__("You are not in an Alliance")

class NameAlreadyExists(Exception):
    def __init__(self) -> None:
        super().__init__(f"An alliance already exists with that name!")

class InvalidInput(Exception):
    def __init__(self, input_name: str) -> None:
        super().__init__(f"Invalid Input [{input_name}]")

class NotSpecified(Exception):
    def __init__(self, input_name: str) -> None:
        super().__init__(f"Value not specified [{input_name}]")

class ServerError(Exception):
    def __init__(self):
        super().__init__("There seems to be an issue with the API.")

class ErrorNotDetected(Exception):
    def __init__(self, error: str):
        super().__init__(f"Error not detected: {error}")

class LimitExceeded(Exception):
    def __init__(self, limit: int, type: str):
        super().__init__(f"You have exceed the limit of {limit} {type}.")

class InvalidKey(Exception):
    def __init__(self) -> None:
        super().__init__("Invalid API Key. Please check the key and try again.")
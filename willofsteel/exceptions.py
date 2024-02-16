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
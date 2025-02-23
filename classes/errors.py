class CardError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

class CardError:
    class ColourError(CardError):
        def __init__(self):
            super().__init__("Given colour is incorrect")

    class NumberError(CardError):
        def __init__(self):
            super().__init__("Given number is incorrect")

    class JokerError(CardError):
        def __init__(self):
            super().__init__("Card is not joker")



class RowError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message
    
class RowError:
    class AllJokers(RowError):
        def __init__(self):
            super().__init__("Row only contains jokers")

    class UnfitJoker(RowError):
        def __init__(self):
            super().__init__("Joker doesn't fit the row")
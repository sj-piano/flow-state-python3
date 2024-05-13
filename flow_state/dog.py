class Dog:
    """A simple Dog class that has a name and can bark."""

    def __init__(self, name: str):
        self.name = name

    def bark(self):
        return 'Woof'

    def respond(self, name: str):
        if name == self.name:
            return self.bark()
        return ""

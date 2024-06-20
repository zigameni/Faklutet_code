# models.py
class Model:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"

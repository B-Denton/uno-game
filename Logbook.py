class Logbook:
    """
    A class to represent the logbook for player actions.

    Methods:
    add_entry(text)
        Add a new line to the logbook containing the given text.
    get_last_lines(n)
        Return the last n lines of the logbook.
    """
    def __init__(self):
        self.logged_lines = []

    def add_entry(self, text):
        self.logged_lines.append(text)

    def get_last_lines(self, n):
        return self.logged_lines[-n:]

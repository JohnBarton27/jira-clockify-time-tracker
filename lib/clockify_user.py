

class ClockifyUser:

    def __init__(self, name: str, user_id: str):
        self.name = name
        self.id = user_id

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
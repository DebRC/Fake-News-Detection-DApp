import random

class News:
    def __init__(self, id, category: int, legit: bool):
        self.id = id
        self.category = category
        self.legit = legit
        self.validatedAsLegit=None
        self.legitVotes=0
        self.fakeVotes=0
        
    def __str__(self):
        return f"News = {self.id} : Category = {self.category} : Legit = {self.legit} : Validated As Legit = {self.validatedAsLegit} : Legit Votes = {self.legitVotes} : Fake Votes = {self.fakeVotes}"
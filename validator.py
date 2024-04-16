from news import News
import os
from dotenv import load_dotenv

load_dotenv()

class Validator:
    def __init__(self, id: int, expertise_category: int, stake: float, malicious: bool = False):
        self.id = id
        self.expertise_category = expertise_category
        self.stake = stake
        self.malicious = malicious
        self.rating = int(os.getenv("DEFAULT_RATING"))
        self.correct_validations = 0
        self.incorrect_validations = 0
        
    def validateNews(self, news: News):
        # Default vote should be 1
        vote=self.rating/int(os.getenv("DEFAULT_RATING"))
        
        # If news category is same as validator's expertise
        # vote should be counted as doubled
        if news.category==self.expertise_category:
            vote=2*vote
        if self.malicious:
            # If malicious
            # Vote in negative (fake) if news is legit
            # Vote in positive (true) if news is fake
            return -vote if news.legit else vote
        else:
            # If honest
            # Vote in positive (true) if news is legit
            # Vote in negative (fake) if news is fake
            return vote if news.legit else -vote
        
    def updateValidations(self, correct: bool):
        # Update the correct and incorrect validations
        if correct:
            self.correct_validations+=1
        else:
            self.incorrect_validations+=1
        
    def __str__(self):
        return f"Validator = {self.id} : Expertised Category = {self.expertise_category} : Stake = {self.stake} : Rating = {self.rating} : Malicious = {self.malicious} : Correct Validations = {self.correct_validations} : Incorrect Validations = {self.incorrect_validations}"
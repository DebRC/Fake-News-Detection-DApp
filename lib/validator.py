from news import News
import os
from random import choices
from dotenv import load_dotenv

load_dotenv()

class Validator:
    def __init__(self, id: int, expertise_category: int, stake: float, trustworthiness: float):
        self.id = id
        self.expertise_category = expertise_category
        self.stake = stake
        self.trustworthiness = trustworthiness
        self.rating = float(os.getenv("DEFAULT_RATING"))
        self.correct_validations = 0
        self.incorrect_validations = 0
        
    def validateNews(self, news: News):
        # Default vote should be 1
        # Vote Range [0,2]
        vote=self.rating/float(os.getenv("DEFAULT_RATING"))
        
        # If news category is same as validator's expertise
        # vote should be counted as doubled
        if news.category==self.expertise_category:
            vote=float(os.getenv("EXPERTISE_VOTE_MULTIPLIER"))*vote
        if news.legit:
            return choices([vote, -vote], [self.trustworthiness, 1-self.trustworthiness])[0]
        else:
            return choices([-vote, vote], [self.trustworthiness, 1-self.trustworthiness])[0]
        
    def updateValidations(self, correct: bool):
        # Update the correct and incorrect validations
        if correct:
            self.correct_validations+=1
        else:
            self.incorrect_validations+=1
        
    def __str__(self):
        return f"Validator = {self.id} : Expertised Category = {self.expertise_category} : Stake = {self.stake} : Rating = {self.rating} : Trust-Worthiness = {self.trustworthiness} : Correct Validations = {self.correct_validations} : Incorrect Validations = {self.incorrect_validations}"
from collections import defaultdict
from news import News
from dotenv import load_dotenv
import os

load_dotenv()

class SmartContract:
    def __init__(self, id: int, minStakeToValidate=10, penaltyStakePercent=0.2, rewardStakePercent=0.2):
        self.id=id
        self.minStakeToValidate=minStakeToValidate
        self.penaltyStake=minStakeToValidate*penaltyStakePercent
        self.rewardStake=minStakeToValidate*rewardStakePercent
        
    def runContract(self, validators, news: News):
        # Get the set of eligible validators
        eligibleValidators=self.returnElgibleValidators(validators)
        
        # Validate the news
        votes=self.validateNews(eligibleValidators,news)
        
        # Penalize validators who voted wrong
        self.penalizeFalseValidators(votes,news)
        
        # Reward validators who voted right
        self.rewardTrueValidators(votes,news)
            
    def returnElgibleValidators(self, validators):
        # Returns validators who have more stake than minStakeToValidate
        elgValidators=[]
        for validator in validators:
            if validator.stake>=self.minStakeToValidate:
                validator.stake-=self.minStakeToValidate
                elgValidators.append(validator)
        return elgValidators
    
    def validateNews(self, eligibleValidators, news: News):
        # Counts votes which votes news is true
        legitVotes=0
        
        # Counts votes which votes news is fake
        fakeVotes=0
        
        # Map (validator->vote)
        votes=defaultdict(int)
        for validator in eligibleValidators:
            # Validate news for the validator
            vote=validator.validateNews(news)
            # print(validator.id, vote)
            
            # If vote is positive, validator votes the news is true
            if vote>0:
                legitVotes+=vote
                votes[validator]=True
            
            # If vote is negative, validator votes the news is fake
            else:
                fakeVotes+=vote
                votes[validator]=False
        
        # If more legit votes than fake,
        # marks the news as legit
        if legitVotes>abs(fakeVotes):
            news.validatedAsLegit=True
        else:
            news.validatedAsLegit=False
        
        # Update news with votes
        news.legitVotes=legitVotes
        news.fakeVotes=abs(fakeVotes)
            
        return votes
    
    def penalizeFalseValidators(self, votes, news: News):
        # Penalize validators who voted wrong
        for validator in votes:
            # If news validated result is not equal to validator's vote
            if news.validatedAsLegit!=votes[validator]:
                # Cut penalty stake from validator's stake
                # Refund the rest stake
                validator.stake+=(self.minStakeToValidate-self.penaltyStake)
                # Decrease validator's rating
                validator.rating-=int(os.getenv("RATING_CHANGE_FACTOR"))
                # Make sure rating does not go below 0
                validator.rating=max(validator.rating,0)
                # Update validator's validation stats
                validator.updateValidations(False)
                
    def rewardTrueValidators(self, votes, news: News):
        # Reward validators who voted right
        
        # Calculate the total penalty stake collected
        penaltyStake=0
        # Count the number of validators who voted right
        validVoters=0
        for validator in votes:
            if news.validatedAsLegit!=votes[validator]:
                penaltyStake+=self.penaltyStake
            else:
                validVoters+=1
                
        # Divide the total penalty stake among the validators who voted right
        penaltyStakeRewardPerVoter=penaltyStake/validVoters
        
        for validator in votes:
            if news.validatedAsLegit==votes[validator]:
                # Along with rewards stake, refund the minStakeToValidate 
                # and distribute the penalty stake per validator collected
                validator.stake+=(self.minStakeToValidate+self.rewardStake+penaltyStakeRewardPerVoter)
                validator.rating+=int(os.getenv("RATING_CHANGE_FACTOR"))
                validator.updateValidations(True)
    
    def __str__(self):
        return f"SmartContract = {self.id} : Min Stake To Validate = {self.minStakeToValidate} : Penalty Stake = {self.penaltyStake} : Reward Stake = {self.rewardStake}"
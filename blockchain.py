from validator import Validator
from news import News
from smart_contract import SmartContract

class BlockChain:
    def __init__(self):
        self.validators = {}
        self.smart_contracts = {}
        self.news = {}
        
    def addValidator(self, newValidator: Validator):
        # Check if validator id already exists
        if newValidator.id in self.validators:
            return False
        # Add validator to the blockchain
        self.validators[newValidator.id]=newValidator
        return True
    
    def addSmartContract(self, newSmartContract: SmartContract):
        # Check if smart contract id already exists
        if newSmartContract.id in self.smart_contracts:
            return False
        # Add smart contract to the blockchain
        self.smart_contracts[newSmartContract.id]=newSmartContract
        return True
    
    def validateNews(self, smartContractID, news: News):
        # Check if smart contract id exists
        if smartContractID not in self.smart_contracts:
            return False
        # Add news to the blockchain
        self.news[news.id]=news
        # Run the smart contract
        self.smart_contracts[smartContractID].runContract(list(self.validators.values()),news)
        return True
        
    def getNewsValidity(self, newsID):
        # Check if news id exists
        if newsID not in self.news:
            return "News Does Not Exists"
        # Return the news validity
        return self.news[newsID]
    
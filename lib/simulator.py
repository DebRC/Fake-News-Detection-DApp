from blockchain import BlockChain
from news import News
from smart_contract import SmartContract
from validator import Validator
from dotenv import load_dotenv
import os,random

load_dotenv()

class Simulator:
    def __init__(self):
        self.blockchain=BlockChain()
        
    def generateVeryTrustWorthyValidators(self,n=10):
        # Generate n honest validators
        for _ in range(n):
            # Generate random id, expertise and stake
            id=random.randint(1,10000)
            # Expertise is a random number between 1 and CATEGORY_TYPES
            expertise=random.randint(1,int(os.getenv("CATEGORY_TYPES")))
            # Stake is a random number between 50 and 100
            stake=random.randint(50,100)
            validator=Validator(id,expertise,stake,0.9)
            # Add the validator to the blockchain
            self.blockchain.addValidator(validator)
        print(f"{n} very trust worthy validators generated")
        
    def generateTrustWorthyValidators(self,n=10):
        # Generate n honest validators
        for _ in range(n):
            # Generate random id, expertise and stake
            id=random.randint(1,10000)
            # Expertise is a random number between 1 and CATEGORY_TYPES
            expertise=random.randint(1,int(os.getenv("CATEGORY_TYPES")))
            # Stake is a random number between 50 and 100
            stake=random.randint(50,100)
            validator=Validator(id,expertise,stake,0.7)
            # Add the validator to the blockchain
            self.blockchain.addValidator(validator)
        print(f"{n} trust worthy validators generated")
    
    def generateMaliciousValidators(self,n=10):
        # Generate n malicious validators
        for _ in range(n):
            # Generate random id, expertise and stake
            id=random.randint(1,10000)
            expertise=random.randint(1,int(os.getenv("CATEGORY_TYPES")))
            stake=random.randint(50,100)
            malicious=True
            validator=Validator(id,expertise,stake,0)
            # Add the validator to the blockchain
            self.blockchain.addValidator(validator)
        print(f"{n} malicious validators generated")
            
    def printValidators(self):
        # Print all validators
        print(f"Validators in the BlockChain ::")
        for validatorID in self.blockchain.validators:
            print(self.blockchain.validators[validatorID])
            
    def addNewsContract(self):
        # Add a news contract
        # Generate a random id
        id=random.randint(1,10000)
        smartContract=SmartContract(id)
        # Add the smart contract to the blockchain
        print(f"Adding Smart Contract (ID={id}) in blockchain...")
        if(not self.blockchain.addSmartContract(smartContract)):
            print(f"Smart Contract (ID={id}) already exists")
            return
        print(f"Smart Contract (ID={id}) for News Validity added in blockchain")
        return id
        
    def printSmartContracts(self):
        # Print all smart contracts
        print(f"Smart Contracts in the BlockChain ::")
        for smartContractID in self.blockchain.smart_contracts:
            print(self.blockchain.smart_contracts[smartContractID])
            
    def generateNewsAndValidate(self, smartContractID):
        # Generate a random news and validates it
        id=random.randint(1,10000)
        category=random.randint(1,int(os.getenv("CATEGORY_TYPES")))
        news=News(id,category,random.choice([True,False]))
        print(f"News (ID={id}) Generated")
        if(not self.blockchain.validateNews(smartContractID, news)):
            print(f"Smart Contract {smartContractID} does not exists")
            return
        print(f"News (ID={id}) Validated")
        
    def deleteAllValidators(self):
        # Delete all validators
        self.blockchain.validators={}
        print("All validators deleted")
        
    def printNews(self, newsID):
        # Print the news validity
        print(self.blockchain.getNewsValidity(newsID))
        
    def printAllNews(self):
        # Print the news validity
        for newsID in self.blockchain.news:
            news: News=self.blockchain.news[newsID]
            print(news,end=" : ")
            if news.legit:
                print("False Vote% =",news.fakeVotes/(news.legitVotes+news.fakeVotes))
            else:
                print("False Vote% =",news.legitVotes/(news.legitVotes+news.fakeVotes))
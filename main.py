from simulator import Simulator

sim=Simulator()

while(True):
    print("----------------------------------")
    print("1. Generate Honest Validators")
    print("2. Generate Malicious Validators")
    print("3. Print Validators")
    print("4. Add News Smart Contract")
    print("5. Print Smart Contracts")
    print("6. Generate News and Validate")
    print("7. Print News with ID")
    print("8. Print All News")
    print("9. Exit")
    print("----------------------------------")
    print()
    choice=int(input("Enter your choice :: "))
    print()
    if choice==1:
        n=int(input("Enter number of honest validators to generate :: "))
        sim.generateHonestValidators(n)
    elif choice==2:
        n=int(input("Enter number of malicious validators to generate :: "))
        sim.generateMaliciousValidators(n)
    elif choice==3:
        sim.printValidators()
    elif choice==4:
        sim.addNewsContract()
    elif choice==5:
        sim.printSmartContracts()
    elif choice==6:
        smartContractID=int(input("Enter Smart Contract ID :: "))
        sim.generateNewsAndValidate(smartContractID)
    elif choice==7:
        newsID=int(input("Enter News ID :: "))
        sim.printNews(newsID)
    elif choice==8:
        sim.printAllNews()
    elif choice==9:
        break
    else:
        print("Invalid Choice")
    print()
    
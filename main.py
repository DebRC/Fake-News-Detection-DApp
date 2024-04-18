from simulator import Simulator

sim=Simulator()
smID=sim.addNewsContract()

while(True):
    print("----------------------------------")
    print("1. Generate Very Trust Worthy Validators")
    print("2. Generate Trust Worthy Validators")
    print("3. Generate Malicious Validators")
    print("4. Print Validators")
    print("5. Generate News and Validate")
    print("6. Print News with ID")
    print("7. Print All News")
    print("8. Exit")
    print("----------------------------------")
    print()
    choice=int(input("Enter your choice :: "))
    print()
    if choice==1:
        n=int(input("Enter number of very trust worthy validators to generate :: "))
        sim.generateVeryTrustWorthyValidators(n)
    elif choice==2:
        n=int(input("Enter number of trust worthy validators to generate :: "))
        sim.generateTrustWorthyValidators(n)
    elif choice==3:
        n=int(input("Enter number of malicious validators to generate :: "))
        sim.generateMaliciousValidators(n)
    elif choice==4:
        sim.printValidators()
    elif choice==5:
        sim.generateNewsAndValidate(smID)
    elif choice==6:
        newsID=int(input("Enter News ID :: "))
        sim.printNews(newsID)
    elif choice==7:
        sim.printAllNews()
    elif choice==8:
        break
    else:
        print("Invalid Choice")
    print()
    
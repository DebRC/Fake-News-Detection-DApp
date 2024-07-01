# Fake-News-Detection
A decentralised application written in Python and Solidity, to detect authenticity of news with capability of countering various attacks and incentivisation of rational voters.

## Features
* Anyone is allowed to request the DApp for fact-checking a news article or item.
* Anyone is allowed to register on the DApp as a fact-checker.
* The fact-checkers can vote to say whether the news item is fake or not. The vote could be binary (0 or 1) or it could be a number over a range, say 1- 10, to indicate how truthful the news is (a higher number could imply that the voter thinks the news is more truthful).
* The DApp considers all votes and outputs a single number indicating the fakeness or truthfulness of the news.

## Issues Handled
* Sybil attack
* Re-evaluation of the trustworthiness of voters.
* Opinions of more trustworthy voters is given more weight.
* Rational voters are incentivised to participate and vote truthfully to the best of their ability.

## Project Structure
* The entire code of the application is inside `lib` folder.
* For simulation purpose the blockchain implemented is not a real blockchain simulator but just a structure to add block instantaneuosly with no form of layer 1 attacks.
* `blockchain.py` contains the structure of a basic blockchain which can add smart contract in the chain, signs up validators for news verification e.t.c.
* `smart_contract.py` contains the code for the fake news detection contract. It is just the Python translation of the Solidity code `smart_contract.sol`. 
* `simulator.py` contains the code for the entire simulation process with registration of validators, uploading of news, verification results of news e.t.c.
* `main.py` is the entry-point of the simulation which can be used to simulate as per need.
* `Report.pdf` contains a performance analysis of both the simulators with detailed explanation.

## How to Run?
The simulator has an UI to choose how many validators to create, generate news and check for validity of a news in run-time.

`python3 lib/main.py`

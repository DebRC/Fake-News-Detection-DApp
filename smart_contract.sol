pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract SmartContract {
    using SafeMath for uint;
    
    // Contract variables
    uint public id; // Contract ID
    uint public minStakeToValidate; // Minimum stake required to validate news
    uint public penaltyStake; // Penalty stake for false validators
    uint public rewardStake; // Reward stake for true validators
    uint public MAX_VOTE; // Maximum vote value
    uint public RATING_CHANGE_FACTOR; // Rating change factor
    uint public MIN_RATING; // Minimum rating
    uint public MAX_RATING; // Maximum rating
    uint public DEFAULT_RATING; // Default rating
    uint public EXPERTISE_VOTE_MULTIPLIER; // Expertise vote multiplier

    constructor(
        uint _id,
        uint _minStakeToValidate,
        uint _penaltyStakePercent,
        uint _rewardStakePercent,
        uint _MAX_VOTE,
        uint _RATING_CHANGE_FACTOR,
        uint _MIN_RATING,
        uint _MAX_RATING,
        uint _DEFAULT_RATING,
        uint _EXPERTISE_VOTE_MULTIPLIER
    ) {
        id = _id;
        minStakeToValidate = _minStakeToValidate;
        penaltyStake = (_minStakeToValidate * _penaltyStakePercent) / 100;
        rewardStake = (_minStakeToValidate * _rewardStakePercent) / 100;
        MAX_VOTE = _MAX_VOTE;
        RATING_CHANGE_FACTOR = _RATING_CHANGE_FACTOR;
        MIN_RATING = _MIN_RATING;
        MAX_RATING = _MAX_RATING;
        DEFAULT_RATING = _DEFAULT_RATING;
        EXPERTISE_VOTE_MULTIPLIER = _EXPERTISE_VOTE_MULTIPLIER;
    }

    // Function to run the contract
    function runContract(address[] memory validators, News memory news) public {
        // Get the set of eligible validators
        address[] memory eligibleValidators = returnEligibleValidators(validators);

        // Validate the news
        mapping(address => bool) memory votes = validateNews(eligibleValidators, news);

        // Penalize validators who voted wrong
        penalizeFalseValidators(votes, news);

        // Reward validators who voted right
        rewardTrueValidators(votes, news);
    }
    
    // Function to return eligible validators
    function returnEligibleValidators(address[] memory validators) internal view returns (address[] memory) {
        // Returns validators who have more stake than minStakeToValidate
        address[] memory elgValidators;
        for (uint i = 0; i < validators.length; i++) {
            // Check if validator's stake is above minStakeToValidate
            if (Validator(validators[i]).stake() >= minStakeToValidate) {
                elgValidators.push(validators[i]);
            }
        }
        return elgValidators;
    }
    
    // Function to validate news
    function validateNews(address[] memory eligibleValidators, News memory news) internal returns (mapping(address => bool) memory) {
        // Map (validator->vote)
        mapping(address => bool) memory votes;
        // Counts votes which votes news is true
        uint legitVotes = 0;
        // Counts votes which votes news is fake
        uint fakeVotes = 0;
        
        for (uint i = 0; i < eligibleValidators.length; i++) {
            // Validate news for the validator
            address validatorAddr = eligibleValidators[i];
            Validator validator = Validator(validatorAddr);
            int vote = validator.validateNews(news);
            
            // If vote is positive, validator votes the news is true
            if (vote > 0) {
                legitVotes += uint256(vote) < MAX_VOTE ? uint256(vote) : MAX_VOTE;
                votes[validatorAddr] = true;
            } 
            // If vote is negative, validator votes the news is fake
            else {
                fakeVotes += uint256(-vote) < MAX_VOTE ? uint256(-vote) : MAX_VOTE;
                votes[validatorAddr] = false;
            }
        }
        
        news.legitVotes = legitVotes;
        news.fakeVotes = fakeVotes;
        
        //If more legit votes than fake,
        // marks the news as legit
        news.validatedAsLegit = legitVotes > fakeVotes;
        
        return votes;
    }
    
    // Function to penalize false validators
    function penalizeFalseValidators(mapping(address => bool) memory votes, News memory news) internal {
        for (uint i = 0; i < votes.length; i++) {
            address validatorAddr = votes.keys[i];
            bool vote = votes[validatorAddr];
            Validator validator = Validator(validatorAddr);
            
            // If news validated result is not equal to validator's vote
            if (news.validatedAsLegit != vote) {
                // Cut penalty stake from validator's stake
                // Refund the rest stake
                uint256 penalty = minStakeToValidate - penaltyStake;
                validator.stake += penalty;

                // Decrease validator's rating
                validator.rating = validator.rating.sub(RATING_CHANGE_FACTOR);
                
                // Make sure rating does not go below the minimum rating
                if (validator.rating < MIN_RATING) {
                    validator.rating = MIN_RATING;
                }
                
                // Update validator's validation stats
                validator.updateValidations(false);
            }
        }
    }
    
    // Function to reward true validators
    function rewardTrueValidators(mapping(address => bool) memory votes, News memory news) internal {

        // Calculate the total penalty stake collected
        uint penaltyS = 0;

        // Count the number of validators who voted right
        uint validVoters = 0;
        
        for (uint i = 0; i < votes.length; i++) {
            address validatorAddr = votes.keys[i];
            bool vote = votes[validatorAddr];
            Validator validator = Validator(validatorAddr);
            
            if (news.validatedAsLegit != vote) {
                penaltyS += penaltyStake;
            } else {
                validVoters++;
            }
        }
        
        // Divide the total penalty stake among the validators who voted right
        uint penaltyStakeRewardPerVoter = penaltyS / validVoters;
        
        for (uint i = 0; i < votes.length; i++) {
            address validatorAddr = votes.keys[i];
            bool vote = votes[validatorAddr];
            Validator validator = Validator(validatorAddr);
            
            //Along with rewards stake, refund the minStakeToValidate 
            // and distribute the penalty stake per validator collected
            if (news.validatedAsLegit == vote) {
                uint256 reward = minStakeToValidate + rewardStake + penaltyStakeRewardPerVoter;
                validator.stake += reward;
                validator.rating = validator.rating.add(RATING_CHANGE_FACTOR);
                
                // Make sure rating does not go above the maximum rating
                if (validator.rating > MAX_RATING) {
                    validator.rating = MAX_RATING;
                }
                
                validator.updateValidations(true);
            }
        }
    }
}

contract News {
    uint public id; // News ID
    uint public category; // News category
    bool public legit; // Legitimacy of the news
    bool public validatedAsLegit; // Whether the news is validated as legit
    uint public legitVotes; // Number of legit votes
    uint public fakeVotes; // Number of fake votes
    
    constructor(uint _id, uint _category, bool _legit) {
        id = _id;
        category = _category;
        legit = _legit;
    }
}

contract Validator {
    uint public id; // Validator ID
    uint public expertiseCategory; // Expertise category of the validator
    uint public stake; // Validator's stake
    uint public trustworthiness; // Validator's trustworthiness
    uint public rating; // Validator's rating
    uint public correctValidations; // Number of correct validations
    uint public incorrectValidations; // Number of incorrect validations
    
    constructor(uint _id, uint _expertiseCategory, uint _stake, uint _trustworthiness) {
        id = _id;
        expertiseCategory = _expertiseCategory;
        stake = _stake;
        trustworthiness = _trustworthiness;
        rating = 0; // Initialize rating
    }
    
    // Function to validate news
    function validateNews(News memory news) public view returns (int) {
        // Default vote should be 1
        // Vote Range [0,2]
        int vote = int(rating) / int(DEFAULT_RATING);
        
        // If news category is same as validator's expertise
        // vote should be counted as doubled
        if (news.category == expertiseCategory) {
            vote *= int(EXPERTISE_VOTE_MULTIPLIER);
        }
        // If news is legit,
        // honest validators should vote for positive
        if (news.legit) {
            return choices([vote, -vote], [self.trustworthiness, 1-self.trustworthiness]);
        } 
        // If news is legit,
        // honest validators should vote for negative
        else {
            return choices([-vote, vote], [self.trustworthiness, 1-self.trustworthiness]);
        }
    }
    
    // Function to update validations
    function updateValidations(bool correct) public {
        if (correct) {
            correctValidations++;
        } else {
            incorrectValidations++;
        }
    }
}

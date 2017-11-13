# CrowdInfo
A secure, incentivized and decentralized crowdsourcing solution for information through surveys.

# Setup Instructions
+ Prerequisites:
    + These deployment instructions assume that you have Hyperledger Composer running.
    + Flask for Python3
        ```bash
            sudo pip3 install flask
        ```

+ From the root folder of this repo, run:
    ```bash
        bash deploy.sh
    ```
+ In another terminal in the root directory, run:
    ```bash
        python3 network/setup.py
    ```

+ Then:
    ```bash
        python3 organization/run.py p
    ```

+ In another terminal:
    ```bash
        python3 client/run.py p
    ```

+ The organization webpage is available at `http://localhost:9899/`
    + Go to this page and generate a form

+ The client webpage is available at `http://localhost:9898/`
    + Go to `http://localhost:9898/surveys` to view available surveys
    + Follow the instructions from there


# Problem Statement
#### As a information seeker, do you want to:  
- Harness the power of minds of an entire population to make better business decisions?  
- Find out the opinion of 10,000 people in matter of a few hours?  
- Provide incentive for the masses to participate in your survey?  

#### As an information provider, do you want to:  
- Have a guarantee of the delivery of incentive?  Without a trusted mediator?  
- Have a guarantee of confidentiality of your provided information on the platform you use?  

We aim to solve the problem of secure, incentivized crowdsourcing of information. Unlike the information crowdsourcing solutions of today, there is no trusted mediator who provides guarantee of quality information to the information seekers, and guarantee the delivery of incentive to the information providers. CrowdInfo uses a blockchain framework as a platform for exchange of the provided information.


# Solution
The highlight of our solution is confidentiality of submitted answers through a **zero-knowledge verification** mechanism for smart contracts to determine validity of submitted survey forms.

An information seeker places the survey form and a predefined set of valid answers on the blockchain. Upon the submission of a survey form on the blockchain, we use smart contracts to determine the validity of the submission. If validated, then the incentive is delivered to the information provider. However, there is an obvious problem in this approach: the smart contract must read the answers to validate that these are from the set of allowed answers. This violates the confidentiality of the answers.  

CrowdInfo provides an ingenious **zero-knowledge verification** method for validation of answers of each question by the smart contract, without making the actual answers public. This is achieved using a two-part solution: an on-chain and an off-chain component. CrowdInfo allows for the information seekers to ensure that each information providing entity submits the survey and obtains the incentive only once. The information providers are guaranteed the delivery of incentive on valid submissions by the smart contract.

# Tools used
+ Blockchain: Hyperledger Composer and Fabric
+ Web App: Python 3 with Flask

# Overview
## On-chain component
+ The on-chain compenent provides the necessary structures for the exchange of data.
+ The smart contracts provide guarantees of valid submissions and of delivery of incentive.
+ Participants: ```Consumer``` (information-provider), ```Organization``` (information-seeker)
+ Assets: ```ConsumerAccount```, ```OrganizationAccount```, ```Survey```, ```AssignSurveyToken```
+ Transactions: ```PublishSurvey```, ```SubmitSurvey```
## Off-chain component
+ The off-chain component provides a framework that ensures a single form being issued to a single information provider. It also builds upon the confidentiality guarantee of data.
+ When a consumer requests the organization server for a survey form, the consumer is provided a random string which is to be signed using it's private key. The public key must be registered with a Certificate Authority.
+ Upon recieving the signed string, the organization server decrypts the hashed message using the consumer's public key, after verifying the public key with the CA.
    + If a consumer requests a form with the same public key twice, the request is rejected. This ensures that a single consumer fills a form only once.
+ The consumer is provided:
    + A unique SurveyToken
    + A form which has the questions randomly shuffled. Example: `question1` in the original form will map to `question3` in the provided form, and so on.
    + The organization server stores this mapping against the SurveyToken with itself

## Smart contract
+ The consumer fills the form, and submits it on the blockchain. The submission contains a `filledForm` field which looks like: `{"question1": "2", "question2": "2", "question3": "3"}`. Note that this does not make any sense unless one knows the mapping of original questions to the mapping of questions in the form with that survey ID.
+ The smart contract uses the value in `Survey` assets `optionRange` to check if the options are in the valid range.
+ If valid, the Pay Out is credited to the `ConsumerAccount` from the `Surveys`'s `surveyFunds`.
+ The consumer can verify that tokens have been transferred by checking his `ConsumerAccount` by clicking on `Display Status`

## Viewing answered Surveys
+ Click on `Form Retrieve` button in the organization app.
+ The organization picks up the `filledForm` from the `SubmitSurvey` and reverse maps the questions to the original questions. It can then view the form as filled by the consumer.


# Defining a survey form
+ The generate form page is available at `http://localhost:9899/form/generate`
+ Give a unique Survey ID
+ Define the Pay Out for filling a survey
+ Define the total Survey Funds that are to be assigned to this survey. This amount must be lesser than 100000 for now, since we have allocated only those many funds to the organization in our setup.
+ Define the Expiry time (in number of days) of the survey
+ In the form JSON, define a field `questionN` for the Nth question.
+ `form['questionN']` is a JSON with keys `question` and `allowedAnswers`.
    + `question` contains the question statement
    + `allowedAnswers` contains the JSON of available choices. The keys must begin from 1 and be ordered sequentially.

+ IMPORTANT: All questions must have the same number of choices in the answer. Put this number of choices in Option Range.

+ Example form JSON:
`
{'question1': {'question': 'How much would you pay to watch an episode of Game of Thrones?', 'allowedAnswers': {'1': '50', '2': '25', '3': 'Nothing'}}, 'question2': {'question': 'Which other show will you pay to watch?', 'allowedAnswers': {'1': 'Suits', '2': 'Breaking Bad', '3': 'Silicon Valley'}}, 'question3': {'question': 'How often do you download episodes from torrents?', 'allowedAnswers': {'1': 'Never', '2': 'A few times a month', '3': 'Every week'}}
`
+ Put the number of questions in Question Range.

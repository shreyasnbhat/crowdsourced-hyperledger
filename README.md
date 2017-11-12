# CrowdInfo
A secure, incentivized and decentralized crowdsourcing solution for information through surveys.

### TL;DR

# Problem Statement
#### As a information seeker, do you want to:  
- Harness the power of minds of an entire population - to make better business decisions?  
- Find out the opinion of 10,000 people in matter of a few hours?  
- Provide incentive for the masses to participate in your survey?  

#### As an information provider, do you want to:  
- Have a guarantee of the delivery of incentive?  Without a trusted mediator?  
- Have a guarantee of confidentiality of your provided information on the platform you use?  

We aim to solve the problem of secure, incentivized crowdsourcing of information. Unlike the information crowdsourcing solutions of today, there is no trusted mediator who provides guarantee of quality information to the information seekers, and guarantee the delivery of incentive to the information providers. CrowdInfo uses a blockchain framework as a platform for exchange of the provided information.


# Solution
***TL;DR***:
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
+ A Certificate Authority that ascertains the validity of identity of a user is assumed.

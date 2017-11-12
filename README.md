# crowdsourced-hyperledger
This repository contains code for the Proffer Blockchain Hackathon 2017

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
An information seeker places the survey form and a predefined set of valid answers on the blockchain. Upon the submission of a survey form on the blockchain, we use smart contracts to determine the validity of the submission. If validated, then the incentive is delivered to the information provider. However, there is an obvious problem in this approach: the smart contract must read the answers to validate that these are from the set of allowed answers. This violates the confidentiality of the answers.  

CrowdInfo provides an ingenious method for validation of answers of each question by the smart contract, without making the actual answers public. This **zero-knowledge verification** is achieved using a two-part solution: an on-chain and an off-chain component. CrowdInfo allows for the information seekers to ensure that each information providing entity submits the survey and obtains the incentive only once. The information providers are guaranteed the delivery of incentive on valid submissions by the smart contract.

# TODO: Tools used

# Overview
## On-chain component
+ The on-chain compenent provides the necessary structures for the exchange of data.
+ The smart contracts provide guarantees of valid submissions and of delivery of incentive.
+ The survey issuer publishes a Survey asset that contains the set of valid answers.
+ The 
## Off-chain component
+ The off-chain compenent provides a framework that ensures a single form being issued to a single information provider. It also builds upon the confidentiality guarantee of  data.

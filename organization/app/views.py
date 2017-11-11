from flask import jsonify, request, render_template
from random import shuffle, choice
from string import ascii_uppercase
from rest.api import *
from organization.app import *

currentRandomMessages = []
pubKeyList = ['pubkey']
pubKeyClaimedToken = []
formDB = {}
surveyID = 'surveyID-ABCDE'
form = {
    'question-1': {
        'question': 'Kya aapke masudo me dard hai?',
        'allowedAnswers': {'option1': 'Haan', 'option2': 'Na'}
    },
    'question-2': {
        'question': 'Kya aapke toothpaste me namak hai?',
        'allowedAnswers': {'option1': 'Haan', 'option2': 'Na'}
    },
    'question-3': {
        'question': 'Kya aap chutiye ho?',
        'allowedAnswers': {'option1': 'Haan', 'option2': 'Na'}
    }
}


def isValidPubKey(pubKey):
    return pubKey in pubKeyList


def isValidRandomMessage(randomMessage):
    return randomMessage in currentRandomMessages


def generateRandomMessage():
    randomMessage = generateSurveyToken()
    currentRandomMessages.append(randomMessage)
    return randomMessage


def decrypt(encryptedRandomMessage, pubKey):
    return encryptedRandomMessage[::-1]


def checkRandomMessage(encryptedRandomMessage, pubKey):
    if not isValidPubKey(pubKey):
        return False
    randomMessage = decrypt(encryptedRandomMessage, pubKey)
    # TODO: Use next line for prod
    # if isValidRandomMessage(randomMessage) and not pubKey in pubKeyClaimedToken:
    if isValidRandomMessage(randomMessage):
        currentRandomMessages.remove(randomMessage)
        pubKeyClaimedToken.append(pubKey)
        return True
    return False


def generateSurveyToken():
    tokenLength = 12
    surveyToken = ''.join(choice(ascii_uppercase) for i in range(tokenLength))
    return surveyToken


def publishAssignSurveyToken():
    pass


def retrieveForm():
    print("retrieveForm()")
    questions = list(form.keys())
    shuffle(questions)
    mapping = dict(zip(form.keys(), questions))
    print(mapping)
    formPermute = {}
    for key in mapping:
        formPermute[mapping[key]] = form[key]
    surveyToken = generateSurveyToken()
    formDB[surveyToken] = mapping
    # TODO: implement publishAssignSurveyToken()
    publishAssignSurveyToken()
    formPackage = {'surveyID': surveyID, 'surveyToken': surveyToken, 'form': formPermute}
    print(formPackage)
    return formPackage


@app.route('/test', methods=['GET'])
def get_test():
    return str(getTimestamp())


@app.route('/form', methods=['GET', 'POST'])
def serve_form():
    if request.method == 'GET':
        data = {'randomMessage': generateRandomMessage()}
        return jsonify(data)
    else:
        data = request.json
        if not 'encryptedRandomMessage' in data or not 'pubKey' in data:
            return jsonify({'error': 'data missing in json'})
        if checkRandomMessage(data['encryptedRandomMessage'], data['pubKey']):
            print("Calling jsonify(retrieveForm())")
            return jsonify(retrieveForm())
        else:
            return jsonify({'error': 'auth failed'})


@app.route('/form/generate', methods=['GET', 'POST'])
def serve_form_generate():
    if request.method == 'GET':
        return render_template('form_generate.html', form=form)

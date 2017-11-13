from flask import jsonify, request, render_template
from random import shuffle, choice
from string import ascii_uppercase
from rest.api import *
from organization.app import *
import json
from datetime import timedelta

organizationID = "o2"
organizationAccountID = "oa2"
currentRandomMessages = []
pubKeyList = ['pubkey']
pubKeyClaimedToken = {}
formMappingDB = {}
formDB = {}
surveyID = ''
surveyID_DB = []
form = {
    'question1': {
        'question': 'How much would you pay to watch an episode of Game of Thrones?',
        'allowedAnswers': {'1': '50', '2': '25', '3': 'Nothing'}
    },
    'question2': {
        'question': 'Which other show will you pay to watch?',
        'allowedAnswers': {'1': 'Suits', '2': 'Breaking Bad', '3': 'Silicon Valley'}
    },
    'question3': {
        'question': 'How often do you download episodes from torrents?',
        'allowedAnswers': {'1': 'Never', '2': 'A few times a month', '3': 'Every week'}
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
    # if isValidRandomMessage(randomMessage) and not pubKey in pubKeyClaimedToken[surveyID]:
    if isValidRandomMessage(randomMessage):
        currentRandomMessages.remove(randomMessage)
        if not surveyID in pubKeyClaimedToken:
            pubKeyClaimedToken[surveyID] = []
        pubKeyClaimedToken[surveyID].append(pubKey)
        return True
    return False


def generateSurveyToken():
    tokenLength = 12
    surveyToken = ''.join(choice(ascii_uppercase) for i in range(tokenLength))
    return surveyToken


def publishAssignSurveyToken(surveyToken, surveyID, consumerID):
    status = postAssignSurveyToken(surveyToken, surveyID, consumerID)


def publishSurvey(inputForm, inputSurveyID, payOut, expiry, questionRange, optionRange):
    global form
    global formDB
    global surveyID
    global surveyID_DB
    form_bak = form.copy()
    formDB_bak = formDB.copy()
    surveyID_bak = surveyID
    surveyID_DB_bak = surveyID_DB.copy()
    form = inputForm
    print('#######################################\nForm:')
    print(form)
    print('#######################################')
    if inputSurveyID in surveyID_DB:
        return False
    surveyID = inputSurveyID
    surveyID_DB.append(surveyID)
    if surveyID not in formDB and surveyID!='':
        formDB[surveyID] = form
    status = postSurvey(surveyID, str(form), "localhost", "oa2", payOut, timedelta(days=expiry), questionRange, optionRange)
    if not 'error' in status:
        return status
    form = form_bak
    formDB = formDB_bak
    surveyID = surveyID_bak
    surveyID_DB = surveyID_DB_bak
    return status


def generateFormForConsumer(consumerID):
    print("generateFormForConsumer()")
    print(form)
    questions = list(form.keys())
    shuffle(questions)
    # mapping stores ( original question no.: new question no. )
    mapping = dict(zip(form.keys(), questions))
    print(mapping)
    formPermute = {}
    for key in mapping:
        formPermute[mapping[key]] = form[key]
    surveyToken = generateSurveyToken()
    formMappingDB[surveyToken] = mapping
    # TODO: implement publishAssignSurveyToken()
    publishAssignSurveyToken(surveyToken, surveyID, consumerID)
    formPackage = {'surveyID': surveyID, 'surveyToken': surveyToken, 'form': formPermute}
    print(formPackage)
    return formPackage


def retreiveSubmittedForm(surveyID):
    submitSurveys = getGeneral('SubmitSurvey')
    assignSurveyTokens = getGeneral('AssignSurveyToken')
    #temp_target = []
    target = []
    for submitSurvey in submitSurveys:
        for assignSurveyToken in assignSurveyTokens:
            if(assignSurveyToken['claimed'] and assignSurveyToken['survey'].split('#')[1]==surveyID and assignSurveyToken['surveyToken']==submitSurvey['surveyToken'] and assignSurveyToken['surveyToken'] in formMappingDB):
                submittedForm = {}
                filledForm = json.loads(submitSurvey['filledForm'])
                mapping = formMappingDB[assignSurveyToken['surveyToken']]
                for q in mapping:
                    submittedForm[q] = filledForm[mapping[q]]
                #temp_target.append((submitSurvey, assignSurveyToken, formMappingDB[assignSurveyToken['surveyToken']], formDB[surveyID], submittedForm))
                formValues = {}
                form = formDB[surveyID]
                for q in submittedForm:
                    formValues[form[q]['question']] = form[q]['allowedAnswers'][submittedForm[q]]
                target.append({'filledForm': formValues, 'surveyID': surveyID, 'assignSurveyToken': assignSurveyToken, 'submitSurvey': submitSurvey})
    return target


@app.route('/test', methods=['GET'])
def get_test():
    return str(getTimestamp())


@app.route('/form', methods=['GET', 'POST'])
def serve_form():
    if request.method == 'GET':
        data = {'randomMessage': generateRandomMessage(), 'surveyID': surveyID}
        return jsonify(data)
    else:
        data = request.json
        if not 'encryptedRandomMessage' in data or not 'pubKey' in data or not 'consumerID' in data:
            return jsonify({'error': 'data missing in json'})
        if checkRandomMessage(data['encryptedRandomMessage'], data['pubKey']):
            print("Calling jsonify(generateFormForConsumer())")
            return jsonify(generateFormForConsumer(data['consumerID']))
        else:
            return jsonify({'error': 'auth failed'})


@app.route('/form/generate', methods=['GET', 'POST'])
def serve_form_generate():
    if request.method == 'GET':
        return render_template('form_generate.html', form=form)
    else:
        data = request.form
        if not data:
            status = {'error': 'no form'}
        if not 'form' in data or not 'surveyID' in data or not 'surveyFunds' in data or not 'payOut' in data or not 'expiry' in data or not 'optionRange' in data or not 'questionRange' in data:
            status = {'error': 'data missing in form'}
        else:
            status = []
            try:
                formJson = json.loads(data['form'].replace("'",'"'))
            except:
                return render_template('display.html', display={'error': "error in json.loads(data['form'])"})
            ret = publishSurvey(formJson, data['surveyID'], data['payOut'], int(data['expiry']), ['question'+str(x) for x in range(1,int(data['questionRange'])+1)], int(data['optionRange']))
            if 'error' in ret:
                status = [ret['error']['message'], {'help': 'Try using a unique surveyID'}]
            else:
                status.append(ret)
                status.append(postPublishSurvey(data['surveyID'], data['surveyFunds'], organizationAccountID))
                status.append(getSurvey(data['surveyID']))
        return render_template('display.html', display=status)


@app.route('/form/retrieve', methods=['GET', 'POST'])
def serve_form_retrieve():
    if request.method=='GET':
        return render_template('form_retrieve.html', display=retreiveSubmittedForm(surveyID), surveyID_DB=surveyID_DB)
    else:
        return render_template('form_retrieve.html', display=retreiveSubmittedForm(request.form['arg']), surveyID_DB=surveyID_DB)


@app.route('/display/survey')
def serve_display_survey():
    display = getSurvey('')
    return render_template('display_surveys.html', display=display)

@app.route('/display/status')
def serve_display_status():
    display = []
    display.append(getOrganization("o2"))
    display.append(getOrganizationAccount("oa2"))
    display.append({'surveyID': surveyID})
    display.append({'surveyID_DB': surveyID_DB})
    display.append({'formDB': formDB})
    for sid in surveyID_DB:
        display.append(getSurvey(sid))
    return render_template('display_blocks.html', display=display)


@app.route('/display/general', methods=['GET', 'POST'])
def serve_display_general():
    if request.method=='GET':
        return render_template('display_general.html', display=getGeneral())
    else:
        # return render_template('display.html', display=request.form)
        return render_template('display_general.html', display=getGeneral(request.form['arg']))


@app.route('/display/assignSurveyToken')
def serve_display_assignSurveyToken():
    display = getAssignSurveyToken('')
    return render_template('display_blocks.html', display=display)

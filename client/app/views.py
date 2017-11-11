import json
from flask import render_template, request, redirect, url_for, session
from rest.api import *
from client.app import *

pubKey = 'pubkey'
consumerID = "c2"
consumerAccountID = "ca2"
clientTokens = {}
clientForms = {}


def encrypt(randomMessage):
    return randomMessage[::-1]


@app.route('/test', methods=['GET'])
def serve_test():
    return str(getTimestamp())


@app.route('/requestForm', methods=['GET'])
def requestForm():
    if request.method == 'GET':
        return render_template('request.html')


@app.route('/sendHash', methods=['GET', 'POST'])
def sendHash():
    if request.method == 'POST':
        request_ip = request.form['request-ip']
        session['request-ip'] = request_ip

        url = "http://" + request_ip + ":" + ORGANIZATION_PORT + "/form"
        randomMessage = requests.get(url).json()['randomMessage']
        encryptedRandomMessage = encrypt(randomMessage)

        return render_template('sendHash.html',
                               randomMessage=randomMessage,
                               encryptedRandomMessage=encryptedRandomMessage)
    else:
        return render_template('sendHash.html',
                               randomMessage="Error",
                               encryptedRandomMessage="Error")


@app.route('/generateForm', methods=['GET', 'POST'])
def generateForm():
    if request.method == 'POST':
        if 'from-token' in request.form and request.form['from-token']:
            surveyID = request.form['surveyID']
            surveyToken = request.form['surveyToken']
            form = clientForms[surveyToken]
            return render_template('form.html',
                                   randomMessage='Authenticated',
                                   response=form,
                                   surveyID=surveyID,
                                   authenticated=True)
        else:
            url = "http://" + session['request-ip'] + ":" + ORGANIZATION_PORT + "/form"
            form = requests.post(url, json={'encryptedRandomMessage': request.form['encryptedRandomMessage'],
                                            'pubKey': pubKey, 'consumerID': consumerID}).json()

            if "error" not in dict(form).keys():
                clientTokens[form['surveyID']] = form['surveyToken']
                clientForms[form['surveyToken']] = form

                print(clientTokens)
                return render_template('form.html',
                                       randomMessage='Authenticated',
                                       response=form,
                                       surveyID=form['surveyID'],
                                       authenticated=True)
            else:
                return render_template('form.html',
                                       randomMessage=form['error'],
                                       authenticated=False)
    else:
        return redirect(url_for('requestForm'))


@app.route('/publishBlock/<string:surveyID>', methods=['GET', 'POST'])
def publishBlockOnFabric(surveyID):
    if request.method == 'POST':
        filledForm = json.dumps(request.form)
        # TODO: Replace "valid" with filledForm
        postSubmitSurvey("valid", clientTokens[surveyID], consumerAccountID)
        return redirect(url_for('requestForm'))


@app.route('/tokens', methods=['GET', 'POST'])
def viewAllTokens():
    if request.method == 'GET':
        clientTokensData = {}
        tokenClaimStatus = {}
        for token in clientTokens:
            tokenClaimStatus[clientTokens[token]] = getAssignSurveyToken(clientTokens[token])['claimed']
            print(tokenClaimStatus)
            clientTokensData[token] = {'surveyToken': clientTokens[token],
                                       'on-chain': getAssignSurveyToken(clientTokens[token])}
        return render_template('tokens.html',
                               clientTokens=clientTokensData, claimed=tokenClaimStatus)


@app.route('/display/status')
def serve_display_status():
    display = []
    display.append(getConsumer("c2"))
    display.append(getConsumerAccount("ca2"))
    return render_template('display_blocks.html', display=display)

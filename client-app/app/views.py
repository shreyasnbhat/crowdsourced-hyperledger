from app import *
from flask import render_template, request, abort, redirect, url_for, session
import requests, json

pubKey = 'pubkey'
consumerAccountNumber = "ca1"
clientTokens = []


def encrypt(randomMessage):
    return randomMessage[::-1]


@app.route('/requestForm', methods=['GET'])
def requestForm():
    if request.method == 'GET':
        return render_template('request.html')


@app.route('/sendHash', methods=['GET', 'POST'])
def sendHash():
    if request.method == 'POST':
        request_ip = request.form['request-ip']
        session['request-ip'] = request_ip

        # url = "http://" + request_ip + ":9899/form"
        # randomMessage = requests.get(url).json()['randomMessage']
        randomMessage = "RANDOMTOKEN"
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
        print(session['request-ip'])

        # url = "http://" + session['request-ip'] + ":9899/form"
        # form = requests.post(url,json={'encryptedRandomMessage': request.form['encryptedRandomMessage'],'pubKey': pubKey}).json()

        form = {"surveyToken": "RANDOM",
                "surveyID": "ABCD-S1",
                "form": {
                    "question-1": {
                        "allowedAnswers": {
                            0: "Yes",
                            1: "No"
                        },
                        "question": "Is flask a cool way to design web apps?"
                    },
                    "question-2": {
                        "allowedAnswers": {
                            0: "Yes",
                            1: "No"
                        },
                        "question": "Is flask a cool way to design web apps?"
                    },
                    "question-3": {
                        "allowedAnswers": {
                            0: "Yes",
                            1: "No"
                        },
                        "question": "Is flask a cool way to design web apps?"
                    }
                }
                }

        if "error" not in dict(form).keys():
            clientTokens.append(form['surveyToken'])
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

        block_data = {
            "$class": "org.acme.survey.SubmitSurvey",
            "filledForm": filledForm,
            "consumerAccount": consumerAccountNumber,
            "survey": surveyID,
            "transactionId": "",
            "timestamp": "2017-11-09T18:45:48.819Z"
        }

        print(block_data)

        blockchain_endpoint = "http://192.168.43.177:3000/api/SubmitSurvey"
        block_post_response = requests.post(blockchain_endpoint, json=block_data).text
        print(block_post_response)
        return redirect(url_for('requestForm'))


@app.route('/tokens', methods=['GET'])
def viewAllTokens():
    if request.method == 'GET':
        return render_template('tokens.html',
                               clientTokens=clientTokens)

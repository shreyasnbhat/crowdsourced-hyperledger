import requests
from datetime import datetime
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from rest import REST_API_BASE_ENDPOINT

url = "http://" + REST_API_BASE_ENDPOINT + ":3000/api/"
headers = {'content-type': 'application/json'}


def getTimestamp():
    return str(datetime.today().isoformat())


def getGeneral(arg='/system/historian'):
    response = requests.get(url + arg+ '/', headers=headers).json()
    print(response)
    return response


def postConsumer(id):
    data = {
        "$class": "org.acme.survey.Consumer",
        "aadharID": id,
        "name": "consumer" + id,
        "email": "consumer" + id + "@example.com"
    }
    response = requests.post(url + 'Consumer', json=data, headers=headers).json()
    print(response)
    return response


def getConsumer(id):
    response = requests.get(url + 'Consumer/' + id, headers=headers).json()
    print(response)
    return response


def deleteConsumer(id):
    response = requests.delete(url + 'Consumer/' + id, headers=headers).text
    print(response)
    return response


def postConsumerAccount(id, consumerID):
    data = {
        "$class": "org.acme.survey.ConsumerAccount",
        "consumerAccountID": id,
        "tokens": 0,
        "consumer": consumerID
    }
    response = requests.post(url + 'ConsumerAccount', json=data, headers=headers).json()
    print(response)
    return response


def getConsumerAccount(id):
    response = requests.get(url + 'ConsumerAccount/' + id, headers=headers).json()
    print(response)
    return response


def deleteConsumerAccount(id):
    response = requests.delete(url + 'ConsumerAccount/' + id, headers=headers).text
    print(response)
    return response


def postOrganization(id):
    data = {
        "$class": "org.acme.survey.Organization",
        "organizationID": id,
        "name": "organization" + id,
        "email": "organization" + id + "@example.com"
    }
    response = requests.post(url + 'Organization', json=data, headers=headers).json()
    print(response)
    return response


def getOrganization(id):
    response = requests.get(url + 'Organization/' + id, headers=headers).json()
    print(response)
    return response


def deleteOrganization(id):
    response = requests.delete(url + 'Organization/' + id, headers=headers).text
    print(response)
    return response


def postOrganizationAccount(id, organizationID):
    data = {
        "$class": "org.acme.survey.OrganizationAccount",
        "organizationAccountID": id,
        "tokens": 100000,
        "organization": organizationID
    }
    response = requests.post(url + 'OrganizationAccount', json=data, headers=headers).json()
    print(response)
    return response


def getOrganizationAccount(id):
    response = requests.get(url + 'OrganizationAccount/' + id, headers=headers).json()
    print(response)
    return response


def deleteOrganizationAccount(id):
    response = requests.delete(url + 'OrganizationAccount/' + id, headers=headers).text
    print(response)
    return response


def postSurvey(id, form, website, organizationAccountID, payOut, expiryTimeDelta, questionRange, optionRange):
    data = {
        "$class": "org.acme.survey.Survey",
        "surveyID": id,
        "form": form,
        "website": website,
        "expiryTime": str((datetime.now() + expiryTimeDelta).isoformat()),
        "payOut": payOut,
        "tokens": 0,
        "questionRange": questionRange,
        "optionRange": optionRange,
        "organizationAccount": organizationAccountID
    }
    response = requests.post(url + 'Survey', json=data, headers=headers).json()
    print(response)
    return response


def getSurvey(id):
    response = requests.get(url + 'Survey/' + id, headers=headers).json()
    print(response)
    return response


def deleteSurvey(id):
    response = requests.delete(url + 'Survey/' + id, headers=headers).text
    print(response)
    return response


def postAssignSurveyToken(surveyToken, surveyID, consumerID):
    data = {
          "$class": "org.acme.survey.AssignSurveyToken",
          "surveyToken": surveyToken,
          "claimed": "false",
          "survey": surveyID,
          "consumer": consumerID
        }
    response = requests.post(url + 'AssignSurveyToken', json=data, headers=headers).json()
    print(response)
    return response


def getAssignSurveyToken(id):
    response = requests.get(url + 'AssignSurveyToken/' + id, headers=headers).json()
    print(response)
    return response


def deleteAssignSurveyToken(id):
    response = requests.delete(url + 'AssignSurveyToken/' + id, headers=headers).text
    print(response)
    return response


def postPublishSurvey(surveyID, surveyFunds, organizationAccountID):
    data = {
        "$class": "org.acme.survey.PublishSurvey",
        "surveyFunds": surveyFunds,
        "survey": surveyID,
        "organizationAccount": organizationAccountID,
        "timestamp": getTimestamp()
    }
    response = requests.post(url + 'PublishSurvey', json=data, headers=headers).json()
    print(response)
    return response


def postSubmitSurvey(filledForm, surveyToken, consumerAccountID):
    data = {
        "$class": "org.acme.survey.SubmitSurvey",
        "filledForm": filledForm,
        "surveyToken": surveyToken,
        "consumerAccount": consumerAccountID,
        "assignSurveyToken": surveyToken,
        "timestamp": getTimestamp()
    }
    response = requests.post(url + 'SubmitSurvey', json=data, headers=headers).json()
    print(response)
    return response

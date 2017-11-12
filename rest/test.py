from api import *
from datetime import timedelta

postAssignSurveyToken("st1", "s13", "c1")
getAssignSurveyToken("st1")

postSubmitSurvey("{'question1': 1, 'question2': 2, 'question3': 3}", "st1", "ca1")
getConsumerAccount("ca1")
getSurvey("s13")

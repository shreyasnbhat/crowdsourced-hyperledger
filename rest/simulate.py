from api import *
from datetime import timedelta

postConsumer("c1")
getConsumer("c1")

postConsumerAccount("ca1","c1")
getConsumerAccount("ca1")

postOrganization("o1")
getOrganization("o1")

postOrganizationAccount("oa1","o1")
getOrganizationAccount("oa1")

postSurvey("s1", "oa1", 10, timedelta(days=1))
getSurvey("s1")

postPublishSurvey("s1", 9000, "oa1")
getSurvey("s1")
getOrganizationAccount("oa1")

postAssignSurveyToken("st1", "s1", "c1")
getAssignSurveyToken("st1")

deleteAssignSurveyToken("st1")
deleteConsumerAccount("ca1")
deleteConsumer("c1")
deleteSurvey("s1")
deleteOrganizationAccount("oa1")
deleteOrganization("o1")

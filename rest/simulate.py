from rest import api
from datetime import timedelta

api.postConsumer("c1")
api.getConsumer("c1")

api.postConsumerAccount("ca1","c1")
api.getConsumerAccount("ca1")

api.postOrganization("o1")
api.getOrganization("o1")

api.postOrganizationAccount("oa1","o1")
api.getOrganizationAccount("oa1")

api.postSurvey("s1", "oa1", 10, timedelta(days=1))
api.getSurvey("s1")

api.postPublishSurvey("s1", 9899, "oa1")
api.getSurvey("s1")
api.getOrganizationAccount("oa1")

api.deleteConsumerAccount("ca1")
api.deleteConsumer("c1")
api.deleteSurvey("s1")
api.deleteOrganizationAccount("oa1")
api.deleteOrganization("o1")

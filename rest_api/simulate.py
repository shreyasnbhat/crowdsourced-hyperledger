import rest_api
from datetime import timedelta

rest_api.postConsumer("c1")
rest_api.getConsumer("c1")

rest_api.postConsumerAccount("ca1","c1")
rest_api.getConsumerAccount("ca1")

rest_api.postOrganization("o1")
rest_api.getOrganization("o1")

rest_api.postOrganizationAccount("oa1","o1")
rest_api.getOrganizationAccount("oa1")

rest_api.postSurvey("s1", "oa1", 10, timedelta(days=1))
rest_api.getSurvey("s1")

rest_api.postPublishSurvey("s1", 9899, "oa1")
rest_api.getSurvey("s1")
rest_api.getOrganizationAccount("oa1")

rest_api.deleteConsumerAccount("ca1")
rest_api.deleteConsumer("c1")
rest_api.deleteSurvey("s1")
rest_api.deleteOrganizationAccount("oa1")
rest_api.deleteOrganization("o1")

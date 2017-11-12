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

postSurvey("s13", "oa1", 10, timedelta(days=1), ['question'+str(x) for x in range(1,int(3+1))], 3)
getSurvey("s13")

postPublishSurvey("s13", 9000, "oa1")
getSurvey("s13")
getOrganizationAccount("oa1")

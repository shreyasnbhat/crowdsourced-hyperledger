import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from rest.api import *

postConsumer("c2")

postConsumerAccount("ca2","c2")

postOrganization("o2")

postOrganizationAccount("oa2","o2")

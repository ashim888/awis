# awis ![Travis CI](https://travis-ci.org/ashim888/awis.svg?branch=master) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ashim888/awis/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ashim888/awis/?branch=master)

A python script that generates a custom url and query string used to query [Amazon's Alexa Web Information Service (AWIS)](https://aws.amazon.com/awis/). You may want to check the [getting started section on the FAQ](https://aws.amazon.com/awis/faqs/#general_5).

## Sending a UrlInfo request
```python
from myawis import *
import xmltodict

response_groups = ",".join(
    ["RelatedLinks", "Categories", "Rank", "ContactInfo", "RankByCountry",
     "UsageStats", "Speed", "Language", "OwnedDomains", "LinksInCount",
     "SiteData", "AdultContent"])
obj = CallAwis(
    'www.domain.com', response_groups, Access_Key_ID, Secret_Access_Key)
urlinfo = obj.urlinfo()
result = xmltodict.parse(
    str(urlinfo))["aws:UrlInfoResponse"]["Response"]["UrlInfoResult"]["Alexa"]
```
More info in [the docs on UrlInfo](https://docs.aws.amazon.com/AlexaWebInfoService/latest/ApiReference_UrlInfoAction.html)

## Sending a TrafficHistory request
```python
from myawis import *
obj = CallAwis('www.domain.com', 'History', Access_Key_ID, Secret_Access_Key)
obj.traffichistory(RANGE, START)
# RANGE is optional. Defaults to 31
# START is optional. Defaults to 20070801
```
More info in [the docs on TrafficHistory](https://docs.aws.amazon.com/AlexaWebInfoService/latest/ApiReference_TrafficHistoryAction.html)

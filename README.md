# awis ![Travis CI](https://travis-ci.org/ashim888/awis.svg?branch=master) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ashim888/awis/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ashim888/awis/?branch=master)

A python script that generates a custom url and query string used to query [Amazon's Alexa Web Information Service (AWIS)](https://aws.amazon.com/awis/). You may want to check the [getting started section on the FAQ](https://aws.amazon.com/awis/faqs/#general_5).

## UrlInfo request
```python
from myawis import *

obj = CallAwis('github.com', URLINFO_RESPONSE_GROUPS, Access_Key_ID, Secret_Access_Key)
urlinfo = obj.urlinfo()
```
More info in [the docs on UrlInfo](https://docs.aws.amazon.com/AlexaWebInfoService/latest/ApiReference_UrlInfoAction.html)

### Output sample
```python
import pprint

pprint.pprint(flatten_urlinfo(urlinfo))

{'CategoryData.0.AbsolutePath': 'Top/Computers/Software/Configuration_Management/Tools/Git',
 'CategoryData.0.Title': 'Tools/Git',
 'CategoryData.1.AbsolutePath': 'Top/Computers/Open_Source/Project_Hosting',
 'CategoryData.1.Title': 'Open Source/Project Hosting',
 'ContactInfo.CompanyStockTicker': None,
 'ContactInfo.DataUrl.#text': 'github.com',
 'ContactInfo.DataUrl.@type': 'canonical',
 'ContactInfo.Email': None,
 'ContactInfo.OwnerName': None,
 'ContactInfo.PhoneNumbers.PhoneNumber': None,
 'ContactInfo.PhysicalAddress': None,
 'ContentData.AdultContent': None,
 'ContentData.DataUrl.#text': 'github.com',
 'ContentData.DataUrl.@type': 'canonical',
 'ContentData.Language': None,
 'ContentData.LinksInCount': '81310',
 'ContentData.OwnedDomains': None,
 'ContentData.SiteData.Description': 'GitHub is the best place to share code '
                                     'with friends, co-workers, classmates, '
                                     'and complete strangers. Over four '
                                     'million people use GitHub to build '
                                     'amazing things together.',
 'ContentData.SiteData.Title': 'GitHub',
 'ContentData.Speed.MedianLoadTime': '1675',
 'ContentData.Speed.Percentile': '53',
 'ContributingSubdomain.codeload.github.com.Months.1.PageViews.PerUser': '1.26',
 'ContributingSubdomain.codeload.github.com.Months.1.PageViews.Percentage': '0.58%',
 'ContributingSubdomain.codeload.github.com.Months.1.Reach.Percentage': '2.39%',
[...]
 'ContributingSubdomain.status.github.com.Months.1.PageViews.PerUser': '1.1',
 'ContributingSubdomain.status.github.com.Months.1.PageViews.Percentage': '0.07%',
 'ContributingSubdomain.status.github.com.Months.1.Reach.Percentage': '0.34%',
 'Country.AU.Contribution.PageViews': '0.8%',
 'Country.AU.Contribution.Users': '1.0%',
 'Country.AU.Rank': '74',
[...]
 'Country.US.Contribution.PageViews': '21.0%',
 'Country.US.Contribution.Users': '21.3%',
 'Country.US.Rank': '45',
 'OutputTimestamp': '2017-08-14T18:48:45.026723',
 'Related.DataUrl.#text': 'github.com',
 'Related.DataUrl.@type': 'canonical',
 'RelatedLink.0.DataUrl.#text': 'zenofshen.com/posts/ajax-sortable-lists-tutorial',
 'RelatedLink.0.DataUrl.@type': 'canonical',
 'RelatedLink.0.NavigableUrl': 'http://zenofshen.com/posts/ajax-sortable-lists-tutorial',
 'RelatedLink.0.Title': 'zen of shen - script.aculo.us Ajax Sortable Lists '
                        'Tutorial',
[...]
 'RelatedLink.9.DataUrl.#text': 'www.ubuntu.com/',
 'RelatedLink.9.DataUrl.@type': 'canonical',
 'RelatedLink.9.NavigableUrl': 'http://www.ubuntu.com/',
 'RelatedLink.9.Title': 'Ubuntu Linux',
 'TrafficData.DataUrl.#text': 'github.com',
 'TrafficData.DataUrl.@type': 'canonical',
 'TrafficData.Rank': '58',
 'UsageStatistic.Days.1.PageViews.PerMillion.Delta': '-44.22%',
 'UsageStatistic.Days.1.PageViews.PerMillion.Value': '944',
 'UsageStatistic.Days.1.PageViews.PerUser.Delta': '-14.06%',
 'UsageStatistic.Days.1.PageViews.PerUser.Value': '4.28',
 'UsageStatistic.Days.1.PageViews.Rank.Delta': '40',
 'UsageStatistic.Days.1.PageViews.Rank.Value': '92',
 'UsageStatistic.Days.1.Rank.Delta': '+26',
 'UsageStatistic.Days.1.Rank.Value': '84',
 'UsageStatistic.Days.1.Reach.PerMillion.Delta': '-34.99%',
 'UsageStatistic.Days.1.Reach.PerMillion.Value': '8,380',
 'UsageStatistic.Days.1.Reach.Rank.Delta': '+19',
 'UsageStatistic.Days.1.Reach.Rank.Value': '83',
[...]
 'UsageStatistic.Months.3.PageViews.PerMillion.Delta': '+5.46%',
 'UsageStatistic.Months.3.PageViews.PerMillion.Value': '1,573',
 'UsageStatistic.Months.3.PageViews.PerUser.Delta': '-3.69%',
 'UsageStatistic.Months.3.PageViews.PerUser.Value': '5.220',
 'UsageStatistic.Months.3.PageViews.Rank.Delta': '-1',
 'UsageStatistic.Months.3.PageViews.Rank.Value': '49',
 'UsageStatistic.Months.3.Rank.Delta': '-3',
 'UsageStatistic.Months.3.Rank.Value': '58',
 'UsageStatistic.Months.3.Reach.PerMillion.Delta': '+9.67%',
 'UsageStatistic.Months.3.Reach.PerMillion.Value': '12,830',
 'UsageStatistic.Months.3.Reach.Rank.Delta': '-1',
 'UsageStatistic.Months.3.Reach.Rank.Value': '67'}
```

## TrafficHistory request
```python
from myawis import *

obj = CallAwis('www.domain.com', 'History', Access_Key_ID, Secret_Access_Key)
obj.traffichistory(RANGE, START)
# RANGE is optional. Defaults to 31
# START is optional. Defaults to 20070801
```
More info in [the docs on TrafficHistory](https://docs.aws.amazon.com/AlexaWebInfoService/latest/ApiReference_TrafficHistoryAction.html)

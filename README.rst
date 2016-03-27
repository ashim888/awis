myawis
======

.. image:: https://codecov.io/github/ashim888/awis/coverage.svg?branch=master
    :target: https://codecov.io/github/ashim888/awis?branch=master

A python script that generates a custom url and query string used to query Amazon's Alexa Web Information Service (AWIS).


Sending a ``UrlInfo`` request

  from myawis import *
  obj=CallAwis('www.domain.com','ResponseGroup',Access_Key_ID,Secret_Access_Key)
  obj.urlinfo()



Sending a ``TrafficHistory`` request

  from myawis import *
  obj=CallAwis('www.domain.com','History',Access_Key_ID,Secret_Access_Key)
  obj.traffichistory(RANGE,START)

``NOTE``: RANGE and START are optional if not present then it would use default Range=31 and START=20070801

#### UrlInfo RESPONSE GROUP
As provided by Alexa web information Service, Response Groups can be of following type while making a request
URL: https://docs.aws.amazon.com/AlexaWebInfoService/latest/


| Response Group| Data Returned    | 
| --------------|------------------|
| RelatedLinks  | Up to 11 related links|
| Categories    | Up to 3 DMOZ (Open Directory) categories the site belongs to|
| Rank  		| The Alexa three month average traffic rank|
| RankByCountry | Percentage of viewers, page views, and traffic rank broken out by country|
| UsageStats  	| Usage statistics such as reach and page views|
| ContactInfo 	| Contact information for the site owner or registrar|
| AdultContent  | Whether the site is likely to contain adult content ('yes' or 'no')|
| Speed 		| Median load time and percent of known sites that are slower|
| Language  	| Content language code and character-encoding (note that this may not match the language or character encoding of any given page on the website because the languange and character set returned are those of the majority of pages) |
| OwnedDomains 	| Other domains owned by the same owner as this site|
| LinksInCount 	| A count of links pointing in to this site|
| SiteData 		| Title, description, and date the site was created|


#### UrlInfo META-RESPONSE GROUP

| Response Group| Data Returned    | 
| --------------|------------------|
| Related  		| Up to 11 related links and up to 3 DMOZ categories (equivalent to ResponseGroup=RelatedLinks,Categories)|
| TrafficData   | Traffic rank and usage statistics (equivalent to ResponseGroup=Rank,UsageStats)|
| ContentData  	| Information about the site's content (equivalent to ResponseGroup=SiteData,AdultContent,Popups,Speed,Language)|

####TrafficHistory RESPONSE GROUP
| Response Group| Data Returned    | 
| --------------|------------------|
| History  		| The TrafficHistory action returns the daily Alexa Traffic Rank, Reach per Million Users, and Unique Page Views per Million Users for each day since August 2007. |


# awis
A python script that generates a custom url and query string used to query Amazon's Alexa Web Information Service (AWIS).

#### RESPONSE GROUP
As provided by Alexa web information Service, Response Groups can be of following type while making a request

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





###Sending a request
```
>>> from myawis import *
>>> obj=CallAwis('www.domain.com','ResponseGroup',Access_Key_ID,Secret_Access_Key)
>>> obj.urlinfo()

```

clone the project and create a virtual env

```
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```
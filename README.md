# awis
A python script that genrates a custom url and query string used to query Amazon's Alexa Web Information Service (AWIS).


###Sending a request
```
>>> from myawis import *
>>> obj=CallAwis('www.domain.com',Access_Key_ID,Secret_Access_Key)
>>> obj.urlinfo()

```

clone the project and create a virtual env

```
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```
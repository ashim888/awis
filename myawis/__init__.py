import datetime
import urllib
import hmac
import hashlib
import base64
import requests
import sys
from bs4 import BeautifulSoup

class CallAwis(object):
	def __init__(self,domainname,responsegroup, access_id, secret_access_key):
		self.domainname=domainname
		self.responsegroup=responsegroup
		self.access_id = access_id
		self.secret_access_key = secret_access_key
		self.SignatureVersion = "2"
		self.SignatureMethod = "HmacSHA256"
		self.ServiceHost = "awis.amazonaws.com"
		self.range="31"
		self.PATH = "/"

	def create_timestamp(self):
	    now = datetime.datetime.now()
	    timestamp = now.isoformat()
	    return timestamp

	def create_uri(self,params):
	    params = [(key, params[key])
	        for key in sorted(params.keys())]
	    return urllib.urlencode(params)

	def create_signature(self):
	    Uri = self.create_uri(self.params)
	    msg = "\n".join(["GET", self.ServiceHost, self.PATH, Uri])
	    hmac_signature = hmac.new(self.secret_access_key, msg, hashlib.sha256)
	    signature = base64.b64encode(hmac_signature.digest())
	    return urllib.quote(signature)

	def urlinfo(self):
		#Query Options  # refer to AWIS API reference for full details.
		Action = "UrlInfo"
		self.params = {
	    'Action':Action,
	    'Url':self.domainname,
	    'ResponseGroup':self.responsegroup,
	    'SignatureVersion':self.SignatureVersion,
	    'SignatureMethod':self.SignatureMethod,
	    'Timestamp': self.create_timestamp(),
	    'AWSAccessKeyId':self.access_id,
	    }

		uri = self.create_uri(self.params)
		signature = self.create_signature()

		url = "http://%s/?%s&Signature=%s" % (self.ServiceHost, uri, signature)
		r=requests.get(url)
		soup=BeautifulSoup(r.text.encode('utf-8'),'xml')
		return soup

	def traffichistory(self,myrange='31',start='20070801'):
		Action="TrafficHistory"
		self.params={
		'Action':Action,
		'AWSAccessKeyId':self.access_id,
		'SignatureMethod':self.SignatureMethod,
		'SignatureVersion':self.SignatureVersion,
		'Timestamp':self.create_timestamp(),
		'Url':self.domainname,
		'ResponseGroup':self.responsegroup,
		'Range':myrange,
		'Start':start,
		}
		uri = self.create_uri(self.params)
		signature = self.create_signature()

		url = "http://%s/?%s&Signature=%s" % (self.ServiceHost, uri, signature)
		r=requests.get(url)
		soup=BeautifulSoup(r.text.encode('utf-8'),'xml')
		return soup


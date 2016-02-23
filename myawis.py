import datetime
import urllib
import hmac
import hashlib
import base64
import requests
import sys

class CallAwis(object):
	def __init__(self,domainname, access_id, secret_access_key):
		self.domainname=domainname
		self.access_id = access_id
		self.secret_access_key = secret_access_key

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
	    hmac_signature = hmac.new(self.secret, msg, hashlib.sha256)
	    signature = base64.b64encode(hmac_signature.digest())
	    return urllib.quote(signature)

	def urlinfo(self):
		#Query Options  # refer to AWIS API reference for full details.
		Action = "UrlInfo" 
		Url = self.domainname
		ResponseGroup = "RankByCountry"

		#Config Options
		self.AWSAccessKeyId = self.access_id
		self.secret = self.secret_access_key
		SignatureVersion = "2"
		SignatureMethod = "HmacSHA256"
		self.ServiceHost = "awis.amazonaws.com"
		self.PATH = "/"
		self.params = {
	    'Action':Action,
	    'Url':Url,
	    'ResponseGroup':ResponseGroup,
	    'SignatureVersion':SignatureVersion,
	    'SignatureMethod':SignatureMethod,
	    'Timestamp': self.create_timestamp(),
	    'AWSAccessKeyId':self.AWSAccessKeyId,
	    }

		uri = self.create_uri(self.params)
		signature = self.create_signature()

		url = "http://%s/?%s&Signature=%s" % (self.ServiceHost, uri, signature)
		# print url
		r=requests.get(url)
		# h = BeautifulSoup(r.text, "html5lib")
		print r.text
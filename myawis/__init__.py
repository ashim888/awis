import datetime
import hmac
import hashlib
import base64
import requests
import xmltodict
from bs4 import BeautifulSoup
try:
    from urllib import quote, urlencode
except ImportError:
    from urllib.parse import quote, urlencode

URLINFO_RESPONSE_GROUPS = ",".join(
    ["RelatedLinks", "Categories", "Rank", "ContactInfo", "RankByCountry",
     "UsageStats", "Speed", "Language", "OwnedDomains", "LinksInCount",
     "SiteData", "AdultContent"])


def create_timestamp():
    now = datetime.datetime.now()
    timestamp = now.isoformat()
    return timestamp


def is_string(obj):
    try:
        return isinstance(obj, basestring)  # python 2
    except NameError:
        return isinstance(obj, str)  # python 3


class CallAwis(object):

    def __init__(self, domainname, responsegroup, access_id, secret_access_key):
        self.domainname = domainname
        self.responsegroup = responsegroup
        self.access_id = access_id
        self.secret_access_key = secret_access_key
        self.SignatureVersion = "2"
        self.SignatureMethod = "HmacSHA256"
        self.ServiceHost = "awis.amazonaws.com"
        self.range = "31"
        self.PATH = "/"

    def create_uri(self, params):
        params = [(key, params[key])
                  for key in sorted(params.keys())]
        return urlencode(params)

    def create_signature(self):
        Uri = self.create_uri(self.params)
        msg = "\n".join(["GET", self.ServiceHost, self.PATH, Uri])
        try:
            hmac_signature = hmac.new(
                self.secret_access_key, msg, hashlib.sha256)
        except TypeError:
            hmac_signature = hmac.new(self.secret_access_key.encode(
                'utf-8'), msg.encode('utf-8'), hashlib.sha256)
        signature = base64.b64encode(hmac_signature.digest())
        return quote(signature)

    def urlinfo(self):
            # Query Options  # refer to AWIS API reference for full details.
            # Action =
        self.params = {
            'Action': "UrlInfo",
            'Url': self.domainname,
            'ResponseGroup': self.responsegroup,
            'SignatureVersion': self.SignatureVersion,
            'SignatureMethod': self.SignatureMethod,
            'Timestamp': create_timestamp(),
            'AWSAccessKeyId': self.access_id,
        }

        uri = self.create_uri(self.params)
        signature = self.create_signature()

        url = "http://%s/?%s&Signature=%s" % (self.ServiceHost, uri, signature)
        return self.return_output(url)

    def traffichistory(self, myrange=31, start=20070801):
        # Action="TrafficHistory"
        self.params = {
            'Action': "TrafficHistory",
            'AWSAccessKeyId': self.access_id,
            'SignatureMethod': self.SignatureMethod,
            'SignatureVersion': self.SignatureVersion,
            'Timestamp': create_timestamp(),
            'Url': self.domainname,
            'ResponseGroup': self.responsegroup,
            'Range': myrange,
            'Start': start,
        }
        uri = self.create_uri(self.params)
        signature = self.create_signature()
        url = "http://%s/?%s&Signature=%s" % (self.ServiceHost, uri, signature)
        return self.return_output(url)

    def cat_browse(self, path):
        # Action=''
        self.params = {
            'Action': "CategoryListings",
            'AWSAccessKeyId': self.access_id,
            'SignatureMethod': self.SignatureMethod,
            'SignatureVersion': self.SignatureVersion,
            'Timestamp': create_timestamp(),
            'ResponseGroup': 'Listings',
            'Path': quote(path),
        }
        uri = self.create_uri(self.params)
        signature = self.create_signature()
        url = "http://%s/?%s&Signature=%s" % (self.ServiceHost, uri, signature)
        return self.return_output(url)

    def return_output(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text.encode('utf-8'), 'xml')
        return soup


def flatten_urlinfo(urlinfo, shorter_keys=True):
    """ Takes a urlinfo object and returns a flat dictionary."""
    def flatten(value, prefix=""):
        if is_string(value):
            _result[prefix[1:]] = value
            return
        try:
            len(value)
        except (AttributeError, TypeError):  # a leaf
            _result[prefix[1:]] = value
            return

        try:
            items = value.items()
        except AttributeError:  # an iterable, but not a dict
            last_prefix = prefix.split(".")[-1]
            if shorter_keys:
                prefix = "." + last_prefix

            if last_prefix == "Country":
                for v in value:
                    country = v.pop("@Code")
                    flatten(v, ".".join([prefix, country]))
            elif last_prefix in ["RelatedLink", "CategoryData"]:
                for i, v in enumerate(value):
                    flatten(v, ".".join([prefix, str(i)]))
            elif value[0].get("TimeRange"):
                for v in value:
                    time_range = ".".join(tuple(v.pop("TimeRange").items())[0])
                    # python 3 odict_items don't support indexing
                    if v.get("DataUrl"):
                        time_range = ".".join([v.pop("DataUrl"), time_range])
                    flatten(v, ".".join([prefix, time_range]))
            else:
                msg = prefix + " contains a list we don't know how to flatten."
                raise NotImplementedError(msg)
        else:  # a dict, go one level deeper
            for k, v in items:
                flatten(v, ".".join([prefix, k]))

    _result = {}
    info = xmltodict.parse(str(urlinfo))
    flatten(info["aws:UrlInfoResponse"]["Response"]["UrlInfoResult"]["Alexa"])
    _result["OutputTimestamp"] = create_timestamp()
    return _result

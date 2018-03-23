import datetime
import hashlib
import hmac

import requests  # pip install requests
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

TRAFFICINFO_RESPONSE_GROUPS = "History"
CATEGORYBROWSE_RESPONSE_GROUPS = ",".join(["Categories", "RelatedCategories", "LanguageCategories", "LetterBars"])


def is_string(obj):
    try:
        return isinstance(obj, basestring)  # python 2
    except NameError:
        return isinstance(obj, str)  # python 3

class CallAwis(object):
    def __init__(self, access_id, secret_access_key):
        self.access_id = access_id
        self.secret_access_key = secret_access_key

    def create_v4_signature(self, request_params):
        '''
        Create URI and signature headers based on AWS V4 signing process.
        Refer to https://docs.aws.amazon.com/AlexaWebInfoService/latest/ApiReferenceArticle.html for request params.
        :param request_params: dictionary of request parameters
        :return: URL and header to be passed to requests.get
        '''

        method = 'GET'
        service = 'awis'
        host = 'awis.us-west-1.amazonaws.com'
        region = 'us-west-1'
        endpoint = 'https://awis.amazonaws.com/api'
        request_parameters = urlencode([(key, request_params[key]) for key in sorted(request_params.keys())])

        # Key derivation functions. See:
        # http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
        def sign(key, msg):
            return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

        def getSignatureKey(key, dateStamp, regionName, serviceName):
            kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
            kRegion = sign(kDate, regionName)
            kService = sign(kRegion, serviceName)
            kSigning = sign(kService, 'aws4_request')
            return kSigning

        # Create a date for headers and the credential string
        t = datetime.datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope

        # Create canonical request
        canonical_uri = '/api'
        canonical_querystring = request_parameters
        canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'
        signed_headers = 'host;x-amz-date'
        payload_hash = hashlib.sha256(''.encode('utf8')).hexdigest()
        canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

        # Create string to sign
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf8')).hexdigest()

        # Calculate signature
        signing_key = getSignatureKey(self.secret_access_key, datestamp, region, service)

        # Sign the string_to_sign using the signing_key
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

        # Add signing information to the request
        authorization_header = algorithm + ' ' + 'Credential=' + self.access_id + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
        headers = {'X-Amz-Date':amzdate, 'Authorization':authorization_header, 'Content-Type': 'application/xml', 'Accept': 'application/xml'}

        # Create request url
        request_url = endpoint + '?' + canonical_querystring

        return request_url, headers

    def urlinfo(self, domain, response_group = URLINFO_RESPONSE_GROUPS):
        '''
        Provide information about supplied domain as specified by the response group
        :param domain: Any valid URL
        :param response_group: Any valid urlinfo response group
        :return: Traffic and/or content data of the domain in XML format
        '''
        params = {
            'Action': "UrlInfo",
            'Url': domain,
            'ResponseGroup': response_group
        }

        url, headers = self.create_v4_signature(params)
        return self.return_output(url, headers)

    def traffichistory(self, domain, response_group=TRAFFICINFO_RESPONSE_GROUPS, myrange=31, start=20070801):
        '''
        Provide traffic history of supplied domain
        :param domain: Any valid URL
        :param response_group: Any valid traffic history response group
        :return: Traffic and/or content data of the domain in XML format
        '''
        params = {
            'Action': "TrafficHistory",
            'Url': domain,
            'ResponseGroup': response_group,
            'Range': myrange,
            'Start': start,
        }

        url, headers = self.create_v4_signature(params)
        return self.return_output(url, headers)

    def cat_browse(self, domain, path, response_group=CATEGORYBROWSE_RESPONSE_GROUPS, descriptions='True'):
        '''
        Provide category browse information of specified domain
        :param domain: Any valid URL
        :param path: Valid category path
        :param response_group: Any valid traffic history response group
        :return: Traffic and/or content data of the domain in XML format
        '''
        params = {
            'Action': "CategoryListings",
            'ResponseGroup': 'Listings',
            'Path': quote(path),
            'Descriptions': descriptions
        }

        url, headers = self.create_v4_signature(params)
        return self.return_output(url, headers)

    def return_output(self, url, headers):
        r = requests.get(url, headers=headers)
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
    _result["OutputTimestamp"] = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    return _result

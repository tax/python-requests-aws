# -*- coding: utf-8 -*-
import base64
import hmac

from hashlib import sha1 as sha
py3k = False
try:
    from urlparse import urlparse
    from base64 import encodestring
 
except:
    py3k = True
    from urllib.parse import urlparse
    from base64 import encodebytes as encodestring

from email.utils import formatdate

from requests.auth import AuthBase


class S3Auth(AuthBase):

    """Attaches AWS Authentication to the given Request object."""

    service_base_url = 's3.amazonaws.com'
    # List of Query String Arguments of Interest
    special_params = [
        'acl', 'location', 'logging', 'partNumber', 'policy', 'requestPayment',
        'torrent', 'versioning', 'versionId', 'versions', 'website', 'uploads',
        'uploadId', 'response-content-type', 'response-content-language',
        'response-expires', 'response-cache-control', 'delete', 'lifecycle',
        'response-content-disposition', 'response-content-encoding'
    ]

    def __init__(self, access_key, secret_key, service_url=None):
        if service_url:
            self.service_base_url = service_url
        self.access_key = str(access_key)
        self.secret_key = str(secret_key)

    def __call__(self, r):
        # Create date header if it is not created yet.
        if not 'date' in r.headers and not 'x-amz-date' in r.headers:
            r.headers['date'] = formatdate(
                timeval=None,
                localtime=False,
                usegmt=True)
        signature = self.get_signature(r)
        if py3k:
            signature = signature.decode('utf-8')
        r.headers['Authorization'] = 'AWS %s:%s' % (self.access_key, signature)
        return r

    def get_signature(self, r):
        canonical_string = self.get_canonical_string(
            r.url, r.headers, r.method)
        if py3k:
            key = self.secret_key.encode('utf-8')
            msg = canonical_string.encode('utf-8')
        else:
            key = self.secret_key
            msg = canonical_string
        h = hmac.new(key, msg, digestmod=sha)
        return encodestring(h.digest()).strip()

    def get_canonical_string(self, url, headers, method):
        parsedurl = urlparse(url)
        objectkey = parsedurl.path[1:]
        query_args = sorted(parsedurl.query.split('&'))

        bucket = parsedurl.netloc[:-len(self.service_base_url)]
        if len(bucket) > 1:
            # remove last dot
            bucket = bucket[:-1]

        interesting_headers = {
            'content-md5': '',
            'content-type': '',
            'date': ''}
        for key in headers:
            lk = key.lower()
            try:
                lk = lk.decode('utf-8')
            except:
                pass
            if headers[key] and (lk in interesting_headers.keys() or lk.startswith('x-amz-')):
                interesting_headers[lk] = headers[key].strip()

        # If x-amz-date is used it supersedes the date header.
        if not py3k:
            if 'x-amz-date' in interesting_headers:
                interesting_headers['date'] = ''
        else:
            if 'x-amz-date' in interesting_headers:
                interesting_headers['date'] = ''

        buf = '%s\n' % method
        for key in sorted(interesting_headers.keys()):
            val = interesting_headers[key]
            if key.startswith('x-amz-'):
                buf += '%s:%s\n' % (key, val)
            else:
                buf += '%s\n' % val

        # append the bucket if it exists
        if bucket != '':
            buf += '/%s' % bucket

        # add the objectkey. even if it doesn't exist, add the slash
        buf += '/%s' % objectkey

        params_found = False

        # handle special query string arguments
        for q in query_args:
            k = q.split('=')[0]
            if k in self.special_params:
                if params_found:
                    buf += '&%s' % q
                else:
                    buf += '?%s' % q
                params_found = True
        return buf

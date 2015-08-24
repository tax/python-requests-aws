import unittest
import os
import requests
import hashlib
import sys
from awsauth import S3Auth

PY3 = sys.version > '3'

if PY3:
    from base64 import encodebytes as encodestring
else:
    from base64 import encodestring


TEST_BUCKET = 'testpolpol2'
ACCESS_KEY = 'ACCESSKEYXXXXXXXXXXXX'
SECRET_KEY = 'AWSSECRETKEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
if 'AWS_ACCESS_KEY' in os.environ:
    ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
if 'AWS_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['AWS_SECRET_KEY']


class TestAWS(unittest.TestCase):
    def setUp(self):
        self.auth = S3Auth(ACCESS_KEY, SECRET_KEY)

    def get_content_md5(self, data):
        hashdig = hashlib.md5(data.encode('utf-8').strip()).digest()
        signature = encodestring(hashdig)
        if PY3:
            return signature.decode('utf-8').strip()
        return signature.strip()

    def test_put_get_delete(self):
        url = 'http://' + TEST_BUCKET + '.s3.amazonaws.com/myfile.txt'
        testdata = 'Sam is sweet'
        r = requests.put(url, data=testdata, auth=self.auth)
        self.assertEqual(r.status_code, 200)
        # Downloading a file
        r = requests.get(url, auth=self.auth)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, 'Sam is sweet')
        # Removing a file
        r = requests.delete(url, auth=self.auth)
        self.assertEqual(r.status_code, 204)

    def test_put_get_delete_filnamehasplus(self):
        testdata = 'Sam is sweet'
        filename = 'my+file.txt'
        url = 'http://' + TEST_BUCKET + '.s3.amazonaws.com/%s' % (filename)
        r = requests.put(url, data=testdata, auth=self.auth)
        self.assertEqual(r.status_code, 200)
        # Downloading a file
        r = requests.get(url, auth=self.auth)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, testdata)
        # Removing a file
        r = requests.delete(url, auth=self.auth)
        self.assertEqual(r.status_code, 204)

    def test_put_get_delete_filname_encoded(self):
        testdata = 'Sam is sweet'
        filename = 'my%20file.txt'
        url = 'http://' + TEST_BUCKET + '.s3.amazonaws.com/%s' % (filename)
        r = requests.put(url, data=testdata, auth=self.auth)
        self.assertEqual(r.status_code, 200)
        # Downloading a file
        r = requests.get(url, auth=self.auth)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, testdata)
        # Removing a file
        r = requests.delete(url, auth=self.auth)
        self.assertEqual(r.status_code, 204)

    def test_put_get_delete_cors(self):
        url = 'http://' + TEST_BUCKET + '.s3.amazonaws.com/?cors'
        testdata = '<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">\
                            <CORSRule>\
                            <AllowedOrigin>*</AllowedOrigin>\
                            <AllowedMethod>POST</AllowedMethod>\
                            <MaxAgeSeconds>3000</MaxAgeSeconds>\
                            <AllowedHeader>Authorization</AllowedHeader>\
                        </CORSRule>\
                    </CORSConfiguration>'
        headers = {'content-md5': self.get_content_md5(testdata)}
        r = requests.put(url, data=testdata, auth=self.auth, headers=headers)
        self.assertEqual(r.status_code, 200)
        # Downloading current cors configuration
        r = requests.get(url, auth=self.auth)
        self.assertEqual(r.status_code, 200)
        # Removing removing cors configuration
        r = requests.delete(url, auth=self.auth)
        self.assertEqual(r.status_code, 204)

    def test_put_get_delete_tagging(self):
        url = 'http://' + TEST_BUCKET + '.s3.amazonaws.com/?tagging'
        testdata = '<Tagging>\
                        <TagSet>\
                            <Tag>\
                                <Key>Project</Key>\
                                <Value>Project 1</Value>\
                            </Tag>\
                        </TagSet>\
                    </Tagging>'
        headers = {'content-md5': self.get_content_md5(testdata)}
        r = requests.put(url, data=testdata, auth=self.auth, headers=headers)
        self.assertEqual(r.status_code, 204)
        # Downloading current cors configuration
        r = requests.get(url, auth=self.auth)
        self.assertEqual(r.status_code, 200)
        # Removing removing cors configuration
        r = requests.delete(url, auth=self.auth)
        self.assertEqual(r.status_code, 204)

    def test_put_get_notification(self):
        url = 'http://' + TEST_BUCKET + '.s3.amazonaws.com/?notification'
        testdata = '<NotificationConfiguration></NotificationConfiguration>'
        headers = {'content-md5': self.get_content_md5(testdata)}
        r = requests.put(url, data=testdata, auth=self.auth, headers=headers)
        self.assertEqual(r.status_code, 200)
        # Downloading current cors configuration
        r = requests.get(url, auth=self.auth)
        self.assertEqual(r.status_code, 200)
        # No Delete ?notification API, empty <NotificationConfiguration>
        # tag is default

    def test_canonical_string_not_using_encoded_query_params(self):
        url = 'https://bucket.ca.tier3.io/object-name?partNumber=1&uploadId=TFDSheOgTxC2Tsh1qVK73A%3D%3D' # NOQA
        headers = {
            'Content-Length': 0,
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'User-Agent': 'python-requests/2.7.0 CPython/2.7.6 Linux/3.13.0-24-generic',
            'Connection': 'keep-alive',
            'date': 'Fri, 21 Aug 2015 16:08:26 GMT',
        }
        method = 'PUT'
        canonical_string = self.auth.get_canonical_string(url, headers, method)
        self.assertTrue('TFDSheOgTxC2Tsh1qVK73A%3D%3D' not in canonical_string)
        self.assertTrue('TFDSheOgTxC2Tsh1qVK73A==' in canonical_string)

        url = 'https://bucket.ca.tier3.io/object-name?partNumber=1&uploadId=not%escaped'
        canonical_string = self.auth.get_canonical_string(url, headers, method)
        self.assertTrue('not%escaped' in canonical_string)

if __name__ == '__main__':
    unittest.main()

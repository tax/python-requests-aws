import unittest
import os
import requests
from awsauth import S3Auth
import hashlib
import base64


TEST_BUCKET = 'testpolpol'
ACCESS_KEY = 'ACCESSKEYXXXXXXXXXXXX'
SECRET_KEY = 'AWSSECRETKEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
if 'AWS_ACCESS_KEY' in os.environ:
    ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
if 'AWS_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['AWS_SECRET_KEY']

class TestAWS(unittest.TestCase):
    def setUp(self):
        self.auth=S3Auth(ACCESS_KEY, SECRET_KEY)
    
    def test_put_get_delete(self):
        testdata = 'Sam is sweet'
        r = requests.put('http://'+ TEST_BUCKET + '.s3.amazonaws.com/myfile.txt', data=testdata, auth=self.auth)
        self.assertEqual(r.status_code, 200)
        # Downloading a file
        r = requests.get('http://'+ TEST_BUCKET + '.s3.amazonaws.com/myfile.txt', auth=self.auth)
        self.assertEqual(r.status_code, 200) 
        self.assertEqual(r.text, 'Sam is sweet')
        # Removing a file
        r = requests.delete('http://'+ TEST_BUCKET + '.s3.amazonaws.com/myfile.txt', auth=self.auth)
        self.assertEqual(r.status_code, 204)        
        
    def test_put_get_delete_filnamehasplus(self):
        testdata = 'Sam is sweet'
        filename = 'my+file.txt'
        url = 'http://'+ TEST_BUCKET + '.s3.amazonaws.com/%s'%(filename)
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
        url = 'http://'+ TEST_BUCKET + '.s3.amazonaws.com/%s'%(filename)
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
        url = 'http://'+ TEST_BUCKET + '.s3.amazonaws.com/?cors'
        testdata = '<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">\
                            <CORSRule>\
                            <AllowedOrigin>*</AllowedOrigin>\
                            <AllowedMethod>POST</AllowedMethod>\
                            <MaxAgeSeconds>3000</MaxAgeSeconds>\
                            <AllowedHeader>Authorization</AllowedHeader>\
                        </CORSRule>\
                    </CORSConfiguration>'
        content_md5 = base64.encodestring(hashlib.md5(testdata.strip()).digest()).strip()
        r = requests.put(url, data=testdata, auth=self.auth, headers={'content-md5': content_md5})
        self.assertEqual(r.status_code, 200)
        # Downloading current cors configuration
        r = requests.get(url, auth=self.auth)
        self.assertEqual(r.status_code, 200)
        # Removing removing cors configuration
        r = requests.delete(url, auth=self.auth)
        self.assertEqual(r.status_code, 204)

    def test_put_get_delete_tagging(self):
        url = 'http://'+ TEST_BUCKET + '.s3.amazonaws.com/?tagging'
        testdata = '<Tagging>\
                        <TagSet>\
                            <Tag>\
                                <Key>Project</Key>\
                                <Value>Project 1</Value>\
                            </Tag>\
                        </TagSet>\
                    </Tagging>'
        content_md5 = base64.encodestring(hashlib.md5(testdata.strip()).digest()).strip()
        r = requests.put(url, data=testdata, auth=self.auth, headers={'content-md5': content_md5})
        self.assertEqual(r.status_code, 204)
        # Downloading current cors configuration
        r = requests.get(url, auth=self.auth)
        self.assertEqual(r.status_code, 200)
        # Removing removing cors configuration
        r = requests.delete(url, auth=self.auth)
        self.assertEqual(r.status_code, 204)

    def test_put_get_notification(self):
        url = 'http://'+ TEST_BUCKET + '.s3.amazonaws.com/?notification'
        testdata = '<NotificationConfiguration></NotificationConfiguration>'
        content_md5 = base64.encodestring(hashlib.md5(testdata.strip()).digest()).strip()
        r = requests.put(url, data=testdata, auth=self.auth, headers={'content-md5': content_md5})
        self.assertEqual(r.status_code, 200)
        # Downloading current cors configuration
        r = requests.get(url, auth=self.auth)
        self.assertEqual(r.status_code, 200)
        # No Delete ?notification API, empty <NotificationConfiguration> tag is default

if __name__ == '__main__':
    unittest.main()

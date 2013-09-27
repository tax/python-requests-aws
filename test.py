import unittest
import os
import requests
from awsauth import S3Auth


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

if __name__ == '__main__':
    unittest.main()

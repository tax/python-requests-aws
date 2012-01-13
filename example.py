import requests
from awsauth import S3Auth

ACCESS_KEY = 'ACCESSKEYXXXXXXXXXXXX'
SECRET_KEY = 'AWSSECRETKEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'        

# Creating a file
r = requests.put('http://mybucket.s3.amazonaws.com/myfile.txt', data='Sam is sweet', auth=S3Auth(ACCESS_KEY, SECRET_KEY))

# Downloading a file
r = requests.get('http://mybucket.s3.amazonaws.com/myfile.txt', auth=S3Auth(ACCESS_KEY, SECRET_KEY))
if r.content == 'Sam is sweet':
    print 'Hala Madrid!'

# Removing a file
r = requests.delete('http://mybucket.s3.amazonaws.com/myfile.txt', auth=S3Auth(ACCESS_KEY, SECRET_KEY))
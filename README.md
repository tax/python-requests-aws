#S3 using python-requests

AWS authentication for Amazon S3 for the wonderful [pyhon requests library](http://python-requests.org)

- Tested with python 2.6
- At the moment only S3 is supported

## Usage


```python
import requests
from awsauth import S3Auth

ACCESS_KEY = 'ACCESSKEYXXXXXXXXXXXX'
SECRET_KEY = 'AWSSECRETKEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'        

s = 'Sam is sweet'
# Creating a file
r = requests.put('http://mybucket.s3.amazonaws.com/file.txt', data=s, auth=S3Auth(ACCESS_KEY, SECRET_KEY))

# Downloading a file
r = requests.get('http://mybucket.s3.amazonaws.com/file.txt', auth=S3Auth(ACCESS_KEY, SECRET_KEY))
if r.content == 'Sam is sweet':
    print 'Hala Madrid!'

# Removing a file
r = requests.delete('http://mybucket.s3.amazonaws.com/file.txt', auth=S3Auth(ACCESS_KEY, SECRET_KEY))

```

## Installation
Installing requests-aws is simple with pip:

```
    $ pip install requests-aws
```

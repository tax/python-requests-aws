#S3 using python-requests

AWS authentication for Amazon S3 for the wonderful [pyhon requests library](http://python-requests.org)

- Tested with python 2.6 and python 3.3.2
- At the moment only S3 is supported

## Usage


```python
import requests
from awsauth import S3Auth

ACCESS_KEY = 'ACCESSKEYXXXXXXXXXXXX'
SECRET_KEY = 'AWSSECRETKEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'        

s = 'Sam is sweet'
# Creating a file
r = requests.put('http://mybuck.s3.amazonaws.com/file.txt', data=s, auth=S3Auth(ACCESS_KEY, SECRET_KEY))

# Downloading a file
r = requests.get('http://mybuck.s3.amazonaws.com/file.txt', auth=S3Auth(ACCESS_KEY, SECRET_KEY))
if r.text == 'Sam is sweet':
    print "It works"

# Removing a file
r = requests.delete('http://mybuck.s3.amazonaws.com/file.txt', auth=S3Auth(ACCESS_KEY, SECRET_KEY))

```

## Installation
Installing requests-aws is simple with pip:

```
    $ pip install requests-aws
```

[![Build Status](https://travis-ci.org/tax/python-requests-aws.png?branch=master)](https://travis-ci.org/tax/python-requests-aws)

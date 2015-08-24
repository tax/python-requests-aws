#S3 using python-requests

AWS authentication for Amazon S3 for the wonderful [pyhon requests library](http://python-requests.org)

[![Build Status](https://travis-ci.org/tax/python-requests-aws.svg?branch=master)](https://travis-ci.org/tax/python-requests-aws)

- Tested with python 2.7 and python 3
- At the moment only S3 is supported

## Usage


```python
import requests
from awsauth import S3Auth

ACCESS_KEY = 'ACCESSKEYXXXXXXXXXXXX'
SECRET_KEY = 'AWSSECRETKEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'        

url = 'http://mybuck.s3.amazonaws.com/file.txt'
s = 'Lola is sweet'
# Creating a file
r = requests.put(url, data=s, auth=S3Auth(ACCESS_KEY, SECRET_KEY))

# Downloading a file
r = requests.get(url, auth=S3Auth(ACCESS_KEY, SECRET_KEY))
if r.text == 'Lola is sweet':
    print "It works"

# Removing a file
r = requests.delete(url, auth=S3Auth(ACCESS_KEY, SECRET_KEY))

```

## Installation
Installing requests-aws is simple with pip:

```
    $ pip install requests-aws
```


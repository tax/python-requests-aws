#!/usr/bin/env python

from __future__ import print_function
import requests
from awsauth import S3Auth

ACCESS_KEY = "ACCESSKEYXXXXXXXXXXXX"
SECRET_KEY = "AWSSECRETKEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# https://forums.aws.amazon.com/thread.jspa?threadID=28799:
# http://docs.amazonwebservices.com/AmazonS3/latest/API/RESTObjectDELETE.html
acceptable_accesscodes = (200, 204)

if __name__ == '__main__':

    # Data needs to be in unicode, or it will fail
    data = u'Sam is sweet'

    bucket = 'mybucket'
    object_name = ['myfile.txt', 'my+file.txt']

    for o in object_name:
        # Creating a file
        url = 'http://{0}.s3.amazonaws.com/{1}'.format(bucket, o)
        r = requests.put(url, data=data, auth=S3Auth(ACCESS_KEY, SECRET_KEY))
        if r.status_code not in acceptable_accesscodes:
            r.raise_for_status()

        # Downloading a file
        url = 'http://{0}.s3.amazonaws.com/{1}'.format(bucket, o)
        r = requests.get(url, auth=S3Auth(ACCESS_KEY, SECRET_KEY))
        if r.status_code not in acceptable_accesscodes:
            r.raise_for_status()

        if r.content == data:
            print('Hala Madrid!')

        # Removing a file
        url = 'http://{0}.s3.amazonaws.com/{1}'.format(bucket, o)
        r = requests.delete(url, auth=S3Auth(ACCESS_KEY, SECRET_KEY))
        if r.status_code not in acceptable_accesscodes:
            r.raise_for_status()

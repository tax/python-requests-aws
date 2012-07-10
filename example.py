#!/usr/bin/env python

import requests

from awsauth import S3Auth

import StringIO

import gzip

import urllib

ACCESS_KEY = "ACCESSKEYXXXXXXXXXXXX"
SECRET_KEY = "AWSSECRETKEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

acceptableAccessCodes = (200, 204) # # https://forums.aws.amazon.com/thread.jspa?threadID=28799: http://docs.amazonwebservices.com/AmazonS3/latest/API/RESTObjectDELETE.html

if __name__ == '__main__':

    confirmIt = u'Sam is sweet' # Data needs to be in unicode, or it will fail

    bucketName = 'mybucket'
    objectName = ['myfile.txt', 'my+file.txt']

    for o in objectName:
        # Creating a file
        r = requests.put(('http://%s.s3.amazonaws.com/%s' % (bucketName, o)), data=confirmIt, auth=S3Auth(ACCESS_KEY, SECRET_KEY))
        if r.status_code not in acceptableAccessCodes:
            r.raise_for_status()

        # Downloading a file
        r = requests.get(('http://%s.s3.amazonaws.com/%s' % (bucketName, o)), auth=S3Auth(ACCESS_KEY, SECRET_KEY))
        if r.status_code not in acceptableAccessCodes:
            r.raise_for_status()

        if r.content == confirmIt:
            print 'Hala Madrid!'

        # Removing a file
        r = requests.delete(('http://%s.s3.amazonaws.com/%s' % (bucketName, o)), auth=S3Auth(ACCESS_KEY, SECRET_KEY))
        if r.status_code not in acceptableAccessCodes:
            r.raise_for_status()

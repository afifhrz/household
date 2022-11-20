# from django.test import TestCase

# Create your tests here.
import requests
import urllib
import json

url = "https://data-asg.goldprice.org/dbXRates/IDR"

req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')
response = urllib.request.urlopen(req)
res = response.read()      # a `bytes` object
html = json.loads(res)
print(html['items'][0]['xauPrice'])
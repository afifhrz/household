# from django.test import TestCase

# Create your tests here.
import urllib
import requests
import json

# print (requests.get())
url = 'https://query1.finance.yahoo.com/v8/finance/chart/EKAD.JK'

req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')
response = urllib.request.urlopen(req)
data = response.read()      # a `bytes` object
html = data.decode('utf-8') # a `str`; this step can't be used if data is binary
html = json.loads(html)
print (html['chart']['result'][0]['meta']['previousClose'])
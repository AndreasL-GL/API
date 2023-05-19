import urllib.request, urllib.parse, urllib.error
import json
import ssl
api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'
# https://developers.google.com/maps/documentation/geocoding/intro
if api_key is False:
    api_key = 42
    serviceurl = 'http://py4e-data.dr-chuck.net/json?'
else :
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def getlocation(location_name):
    address = location_name

    if len(address) < 1: return None
    parms = dict()
    parms['address'] = address
    
    if api_key is not False: parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    try:
        js = json.loads(data)
    except:
        js = None
    if not js or 'status' not in js or js['status'] != 'OK':
        print('==== Failure To Retrieve ====')
        print(data)
        return (0,0)
    print(json.dumps(js, indent=4))
    print(js["results"][0]['formatted_address'])
    lat=js["results"][0]["geometry"]["location"]["lat"]
    lon=js["results"][0]["geometry"]["location"]["lng"]
    
    return (lat,lon)
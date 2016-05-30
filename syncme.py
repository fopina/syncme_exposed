#!/usr/bin/python

import requests
import json

class SyncME(object):
    def register(self, phone):
        params={
            'device_uid':'',
            'country':'',
            'phone': phone,
            'is_push':False,
            'google_ads_id':'',
            'android_id':'',
            'contacts':{
                'INT_DIALING_CODE':'',
                'PHONE_NUMBER':'',
                'DEVICE_TYPE':'ANDROID',
                'OPERATION_SYSTEM':'Android 5.0.2 SDK 21',
                'LOCATION_COUNTRY':'',
                'LOCATION_ZIPCODE':'0',
                'DEVICE_UDID':'',
                'CONTACTS':[],
                'google_ads_id':'',
                'android_id':''
            },
            'APPLICATION_VERSION':'3.4.6',
            'version_number':215,
            'APPLICATION_ID':''
        }
        
        r = self._call('register_2',params)
        self._token = r['token']
        
    def caller_id(self, phone):
        params={
            "phone":phone,
            "manufacturer":"",
            "model":"",
            "version_code":21,
            "is_search":True,
            "is_outgoing":False,
            "locale":"en_GB",
            "get_hints":True,
            "ACCESS_TOKEN":self._token,
            "APPLICATION_VERSION":"3.4.6",
            "version_number":1
        }
           
        r = self._call('caller_id/caller_id/v2',params)
        return r
        
    def save_token(self, filename):
        with open(filename, 'wb') as f:
            f.write(self._token)
            
    def load_token(self, filename):
        with open(filename, 'rb') as f:
            self._token = f.read()
        
    def _call(self, method, params):
        r = requests.post(
            'https://api.sync.me/api/%s' % method,
            data='params=%s' % json.dumps(params),
            headers={"User-Agent": 'Sync.ME Android3.4.6'}
        )
        if r.status_code != 200:
            raise Exception('BAH')
        j = r.json()
        if j['error_code'] < 0:
            raise Exception('%(error_description)s (code %(error_code)d)' % j)
        return j
    

def enable_logging():
    import logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1
    
def pprint(j):
    print(json.dumps(
        j,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    ))
    
    
if __name__ == "__main__":
    #enable_logging()
    import os.path
    import sys
    
    if len(sys.argv) < 2:
        print('Usage: %s [phone number]' % __file__)
        exit(1)
        
    token_file = os.path.expanduser("~/.syncmeexp")
    
    s = SyncME()
    try:
        s.load_token(token_file)
    except IOError:
        print('No token found, registering...')
        s.register('351932123123')
        s.save_token(token_file)
        
    pprint(s.caller_id(sys.argv[1]))

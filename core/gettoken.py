import __init__
import requests,urllib3,json
from urllib.parse import urljoin
from conf import settings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def wazuhToken():
    user,pswd = settings.wazuh_api_user,settings.wazuh_api_pswd
    wazuh_gettoken_url = urljoin(settings.wazuh_api_addr,settings.wazuh_gettoken_api)
    r = requests.get(wazuh_gettoken_url,auth=(user,pswd),verify=False)
    token = r.json()['data']['token']
    return token

def cmdbToken():
    return settings.cmdb_token

def executeToken():
    return settings.execute_token

if __name__ == "__main__":
    print(wazuhToken())

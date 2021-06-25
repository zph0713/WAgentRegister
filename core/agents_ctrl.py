import __init__
import requests
from urllib.parse import urljoin
from conf import settings
from conf.settings import logger
from core.gettoken import wazuhToken
from core.analysislogic import WAgentsAnalysis

class WAgentsCtrl(object):
    def __init__(self,cloud_filter):
        self.WAA = WAgentsAnalysis(cloud_filter)

    def query_agents_status(self):
        pass


    def remove_agents(self,ip_list):
        agent_id_list = self.WAA.agents_via_ip_query_id(ip_list)
        url = urljoin(settings.wazuh_api_addr,settings.wazuh_agents_api)
        headers = {'Content-Type': 'application/json',
                    'Authorization': f'Bearer {wazuhToken()}'}
        for agent in agent_id_list:
            payload = {'agents_list':agent,'status':'disconnected','older_than':'1d'}
            logger.debug('remove agent : {}'.format(agent))
            res = requests.delete(url,headers=headers,verify=False,params=payload)
            logger.debug(res.url)
            logger.info(res.text)

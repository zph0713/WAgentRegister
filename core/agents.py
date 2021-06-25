import __init__
import requests
from urllib.parse import urljoin
from conf import settings
from conf.settings import logger
from core.gettoken import wazuhToken


class WAgents(object):
    def __init__(self):
        self.agents_disconnected_ip_list = list()
        self.agents_active_ip_list = list()
        self.agents_full_info = list()
        self.split_pages_query()

    def get_server_count(self):
        logger.debug('get agents result count..')
        payload = {'limit':'1'}
        headers = {'Content-Type': 'application/json',
                    'Authorization': f'Bearer {wazuhToken()}'}
        url = urljoin(settings.wazuh_api_addr,settings.wazuh_agents_api)
        res = requests.get(url,verify=False,params=payload,headers=headers)
        logger.debug('url : {}'.format(res.url))
        logger.debug('result : {}'.format(res.json()))
        count = res.json()['data']['total_affected_items']
        logger.info('agnets results count : {}'.format(count))
        return count

    def split_pages_query(self):
        logger.debug('start split query..')
        count = self.get_server_count()
        pages = count // 500
        for page in range(0,pages + 1):
            offset_num = page * 500
            self.get_agents_info(offset_num)

    def get_agents_info(self,offset_num,limit_num=500):
        url = urljoin(settings.wazuh_api_addr,settings.wazuh_agents_api)
        headers = {'Content-Type': 'application/json',
                    'Authorization': f'Bearer {wazuhToken()}'}
        payload = {'limit':500,'offset':offset_num}
        res = requests.get(url,headers=headers,verify=False,params=payload)
        logger.debug('url : {}'.format(res.url))
        agents_data = res.json()['data']['affected_items']
        for agentinfo in agents_data:
            if agentinfo['status'] == 'disconnected':
                self.agents_disconnected_ip_list.append(agentinfo['ip'])
                self.agents_full_info.append(agentinfo)
            elif agentinfo['status'] == 'active':
                self.agents_active_ip_list.append(agentinfo['ip'])
                self.agents_full_info.append(agentinfo)
            else:
                pass



if __name__ == "__main__":
    WA = WAgents()
    print(WA.agents_full_info)

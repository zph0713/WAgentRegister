import __init__
import requests
import os,json
from conf import settings
from conf.settings import logger
from core.gettoken import cmdbToken
from core.agents import WAgents


class CmdbVms(object):
    def __init__(self):
        self.stopped_server_info_list = list()
        self.stoped_ip_list = list()
        self.running_server_info_list = list()
        self.running_ip_list = list()
        self.split_pages_query()

    def get_server_count(self):
        logger.debug('get cmdbvm result count..')
        payload = {'limit':'1'}
        header = {'X-Token':cmdbToken()}
        res = requests.get(settings.cmdb_get_server_url,params=payload,headers=header)
        count = res.json()['data']['count']
        logger.info('cmdbvm results count : {}'.format(count))
        return count

    def split_pages_query(self):
        logger.debug('start split query..')
        count = self.get_server_count()
        pages = count // 1000
        for page in range(0,pages + 1):
            offset_num = page * 1000
            self.get_server_info(offset_num)

    def get_server_info(self,offset_num,limit_num=1000):
        payload = {'limit':limit_num,'offset':offset_num}
        headers = {'X-Token':cmdbToken()}
        res = requests.get(settings.cmdb_get_server_url,params=payload,headers=headers)
        print(res.url)
        results = res.json()['data']['results']
        status,whitelist = read_file(settings.white_list)
        for result in results:
            if result['private_ip_address'] in whitelist:
                logger.debug('{} in whitelist: '.format(result['private_ip_address']))
                continue
            if result['system_list'] != []:
                #result = result.update(result['system_list'][0])
                result = dict(result,**result['system_list'][0])
                del result['system_list']
            else:
                del result['system_list']
            if result['status'] == 'stopped':
                self.stopped_server_info_list.append(result)
                self.stoped_ip_list.append(result['private_ip_address'])
            else:
                if result['agent_status'] == '正常':
                    self.running_server_info_list.append(result)
                    self.running_ip_list.append(result['private_ip_address'])
                else:
                    pass

def read_file(file):
    logger.debug('white list got')
    try:
        with open(file, "r") as f:
            _f = f.read()
            return True, _f
    except IOError as ex:
        print(str(ex))
        return False, str(ex)




if __name__ == '__main__':
    CV = CmdbVms()
    stopip = CV.running_server_info_list
    print(stopip)

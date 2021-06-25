import __init__
import requests
import json
import os
import re
import time
from urllib.parse import urljoin
from core.gettoken import executeToken
from core.cachefile import CacheData
from conf import settings
from conf.settings import logger

class ExecuteDeploy(object):
    def __init__(self):
        self.CD = CacheData()
        self.execute_record = list()

    '''
    def split_execute(self,ip_list):
        logger.info('split execute..')
        task_name_prefix = 'wazuh_agent_install_'
        count = 0
        for i in range(0,len(ip_list),10):
            count+=1
            split_task_name = task_name_prefix+str(count)
            split_ip_list = ip_list[i:i+10]
            print(split_task_name,split_ip_list)
            #self.execute_deploy(split_task_name,split_ip_list)
    '''

    def split_execute(self,ip_list):
        logger.info('split execute..')
        task_name_prefix = 'wazuh_agent_install_'
        count = 0
        for ip in ip_list:
            count+=1
            task_name = task_name_prefix+str(count)
            post_params = self.analysis_tags(ip)
            #print(task_name,ip,post_params)
            time.sleep(1)
            self.execute_deploy(task_name,ip,post_params)

    def analysis_tags(self,ipaddr):
        datas = self.CD.get_cache(settings.cmdb_cache)
        group_mapping = {'阿里云':'aliyun','腾讯云':'tencent','AWS':'aws','首都在线':'shoudu'}
        for data in datas['data']['running_server_info_list']:
            if ipaddr == data['private_ip_address']:
                post_params = "{},{},{},{},{},{}".format(settings.post_params,
                                                    data.get('env','null'),
                                                    data.get('application_type','null'),
                                                    data.get('zone','null'),
                                                    data.get('department','ops'),
                                                    group_mapping.get(data.get('cloud_vendor','null')))
                return post_params

    def execute_deploy(self,stn,sil,post_params):
        print(post_params)
        list_ip = list()
        list_ip.append(sil)
        logger.info('start push install agents..')
        headers = {'X-Token':executeToken(),'Content-Type':'application/json'}
        payload = {
            "script_id": 27,
            "params": post_params,
            "ip_list": list_ip,
            "task_name": stn,
            "trigger_type": "immediately"
        }
        logger.info(stn)
        logger.info(list_ip)
        logger.info(post_params)
        res = requests.post(settings.execute_url,headers=headers,data=json.dumps(payload),timeout=10)
        print(res.json())
        task_id = res.json()['info']['task_id']
        logger.info(task_id)
        self.execute_record.append(task_id)
        self.CD.record_install_data_to_file(self.execute_record)

    def echo_deploy_status(self,task_id_list):
        logger.info('show install status..')
        headers = {'X-Token':executeToken(),'Content-Type':'application/json'}
        for task_id in task_id_list:
            url = urljoin(settings.echo_excute_url,task_id) + '/'
            res = requests.get(url,headers=headers)
            results = res.json()['info']
            logger.debug(res.url)
            kv = dict()
            dkv = dict()
            for k,v in results.items():
                if k != 'task_details':
                    kv[k] = v
                else:
                    dkv[k] = v
            logger.info(kv)
            for detail in dkv['task_details']:
                logger.info(detail['stdout'])
                logger.error(detail['stderr'])

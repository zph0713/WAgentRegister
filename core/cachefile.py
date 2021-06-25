import __init__
import os,sys
import json
from datetime import datetime
from time import time,sleep
from conf import settings
from conf.settings import logger
from core.cmdbvm import CmdbVms
from core.agents import WAgents



class CacheData(object):
    def __init__(self,force_get_data=False):
        self.force_get_data = force_get_data
        self.load_cache_path()

    def load_cache_path(self):
        self.cmdb_cache_path = settings.cmdb_cache
        self.agents_cache_path = settings.agents_cache
        self.install_task_status_path = settings.install_task_status

    def get_cache(self,cache_path):
        if self.force_get_data == False:
            try:
                with open(cache_path,'r') as load_f:
                    load_dict = json.load(load_f)
                    file_time = load_dict['query_time']
                    now_time = time()
                    interval = (datetime.fromtimestamp(now_time)-datetime.fromtimestamp(file_time)).seconds
                    if interval > 3600:
                        logger.info('cache expired now getting current data..')
                        if cache_path == settings.cmdb_cache:
                            self.get_cmdb_data_to_file()
                        else:
                            self.get_agents_data_to_file()
                        with open(cache_path,'r') as load_f:
                            load_dict = json.load(load_f)
                            return load_dict
                    logger.info('cache got..')
                    return load_dict
            except json.decoder.JSONDecodeError:
                logger.debug('Initialize cache..')
                if cache_path == settings.cmdb_cache:
                    self.get_cmdb_data_to_file()
                else:
                    self.get_agents_data_to_file()
                with open(cache_path,'r') as load_f:
                    load_dict = json.load(load_f)
                    return load_dict
        else:
            logger.info('force getting data')
            if cache_path == settings.cmdb_cache:
                self.get_cmdb_data_to_file()
            else:
                self.get_agents_data_to_file()
            with open(cache_path,'r') as load_f:
                load_dict = json.load(load_f)
                return load_dict

    def install_task_cache(self):
        with open(self.install_task_status_path,'r') as load_f:
            load_dict = json.load(load_f)
            return load_dict

    def cache_dump(self,filepath,data):
        with open(filepath,'w') as outfile:
            outfile.write(json.dumps(data))

    def record_install_data_to_file(self,record_list):
        self.cache_dump(settings.install_task_status,record_list)

    def get_cmdb_data_to_file(self):
        logger.info('getting cmdb data..')
        timedata_dict = dict()
        datadict = dict()
        CV = CmdbVms()
        datadict['stopped_server_info_list'] = CV.stopped_server_info_list
        datadict['stoped_ip_list'] = CV.stoped_ip_list
        datadict['running_server_info_list'] = CV.running_server_info_list
        datadict['running_ip_list'] = CV.running_ip_list
        timedata_dict['query_time'] = time()
        timedata_dict['data'] = datadict
        logger.info('cmdb data got..')
        self.cache_dump(self.cmdb_cache_path,timedata_dict)

    def get_agents_data_to_file(self):
        logger.info('getting agents data..')
        timedata_dict = dict()
        datadict = dict()
        WA = WAgents()
        datadict['agents_disconnected_ip_list'] = WA.agents_disconnected_ip_list
        datadict['agents_active_ip_list'] = WA.agents_active_ip_list
        datadict['agents_full_info'] = WA.agents_full_info
        timedata_dict['query_time'] = time()
        timedata_dict['data'] = datadict
        logger.info('agents data got..')
        self.cache_dump(self.agents_cache_path,timedata_dict)

if __name__ == '__main__':
    CD = CacheData()
    #CD.get_cmdb_data_to_file()
    CD.get_agents_data_to_file()

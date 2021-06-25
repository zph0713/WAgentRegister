import __init__
from core.cachefile import CacheData
from conf import settings
from conf.settings import logger




class WAgentsAnalysis(object):
    def __init__(self,cloud_filter,force_get_data=False):
        self.CD = CacheData(force_get_data)
        self.cmdb_cache = self.CD.get_cache(settings.cmdb_cache)
        self.agents_cache = self.CD.get_cache(settings.agents_cache)

        self.wazuh_disconnected_ip = self.agents_cache['data']['agents_disconnected_ip_list']
        self.wazuh_active_ip = self.agents_cache['data']['agents_active_ip_list']
        self.agents_full_info = self.agents_cache['data']['agents_full_info']

        self.cmdbvm_running_ip = self.cmdb_cache['data']['running_ip_list']
        self.cmdbvm_stoped_ip = self.cmdb_cache['data']['stoped_ip_list']
        self.cmdbvm_all_ip = self.cmdbvm_running_ip + self.cmdbvm_stoped_ip
        self.cmdbvm_running_info = self.cmdb_cache['data']['running_server_info_list']
        self.cmdbvm_stoped_info = self.cmdb_cache['data']['stopped_server_info_list']

        self.need_alert_info = list()
        self.current_need_alert_ip_list = list()
        self.need_remove_info = list()
        self.need_remove_shutdown_info = list()
        self.need_addagents_info = list()
        self.current_need_addagents_ip_list = list()
        self.complete_info_construction(cloud_filter)

    def comparative_ip(self):
        logger.info('start comparative data..')
        wazuh_agents_ip_list = self.wazuh_disconnected_ip + self.wazuh_active_ip
        cmdb_ip_list = self.cmdbvm_running_ip + self.cmdbvm_stoped_ip
        need_alert_ip_list = list(set(self.wazuh_disconnected_ip) & set(self.cmdbvm_running_ip))
        need_remove_ip_list = list(set(self.wazuh_disconnected_ip) & set(self.cmdbvm_stoped_ip))
        for ip in self.wazuh_disconnected_ip:
            if ip not in cmdb_ip_list:
                need_remove_ip_list.append(ip)
        need_addagent_ip_list = list(set(self.cmdbvm_running_ip) - set(wazuh_agents_ip_list))
        return need_alert_ip_list,need_remove_ip_list,need_addagent_ip_list

    def complete_info_construction(self,cloud_filter):
        logger.info('build complete infomation..')
        cloud_vendor = settings.cloud_mappings
        alert_ip,remove_ip,addagents_ip = self.comparative_ip()
        for cmdbruninfo in self.cmdbvm_running_info:
            if cloud_filter == None:
                if cmdbruninfo['private_ip_address'] in alert_ip:
                    self.need_alert_info.append(cmdbruninfo)
                elif cmdbruninfo['private_ip_address'] in addagents_ip:
                    self.need_addagents_info.append(cmdbruninfo)
            else:
                if cmdbruninfo['private_ip_address'] in alert_ip and cmdbruninfo['cloud_vendor'] == cloud_vendor[cloud_filter]:
                    self.need_alert_info.append(cmdbruninfo)
                elif cmdbruninfo['private_ip_address'] in addagents_ip and cmdbruninfo['cloud_vendor'] == cloud_vendor[cloud_filter]:
                    self.need_addagents_info.append(cmdbruninfo)
        for cmdbstopinfo in self.cmdbvm_stoped_info:
            if cmdbstopinfo['private_ip_address'] in remove_ip:
                self.need_remove_info.append(cmdbstopinfo)
        for agentstopinfo in self.wazuh_disconnected_ip:
            if agentstopinfo not in self.cmdbvm_all_ip:
                self.need_remove_shutdown_info.append(agentstopinfo)

        for current_need_alert in self.need_alert_info:
            self.current_need_alert_ip_list.append(current_need_alert['private_ip_address'])
        for current_need_addagents in self.need_addagents_info:
            self.current_need_addagents_ip_list.append(current_need_addagents['private_ip_address'])

    def agents_via_ip_query_id(self,ip_list):
        id_list = list()
        for ip in ip_list:
            for info in self.agents_full_info:
                if ip == info['ip']:
                    id_list.append(info['id'])
                    ip_id = info['ip']+'->'+info['id']
                    logger.debug(ip_id)
        return id_list

if __name__ == '__main__':
    WAA = WAgentsAnalysis()
    WAA.agents_via_ip_query_id()

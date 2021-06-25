import __init__
from core.notifications import MailProcess
from core.analysislogic import WAgentsAnalysis
from core.executedeploy import ExecuteDeploy
from core.cachefile import CacheData
from core.dataformat import format_to_tables,show_list
from core.agents_ctrl import WAgentsCtrl
from conf.settings import logger


class MainActive(object):
    def __init__(self,cloud_filter):
        self.ED = ExecuteDeploy()
        self.CD = CacheData()
        self.WAA = WAgentsAnalysis(cloud_filter)
        self.WAC = WAgentsCtrl(cloud_filter)

    def remove_agents_process(self,ip_list=None):
        id_list = self.WAA.agents_via_ip_query_id(ip_list)
        logger.info('The following machine is offline in WAZUH, VMs has shutdown, will remove on WAZUH!!!')
        if ip_list == None:
            logger.info('# WARNING: !!!!!')
            format_to_tables(self.WAA.need_remove_info)
            show_list(self.WAA.need_remove_shutdown_info)
            input_yn = input('WARNING: !!!!! Please confirm to remove agents on wazuh|yes or no ? yes/no : ')
            if input_yn == 'yes':
                logger.info('start remove agents on wazuh...')
                self.WAC.remove_agents(self.WAA.need_remove_shutdown_info)
            else:
                logger.info('exit')
        else:
            self.WAC.remove_agents(id_list)

    def add_agents_process(self,ip_list=None):
        logger.info('The following machines need to install the Wazuh Agent, now start pushing the installation command!!!!')
        if ip_list == None:
            logger.info('# WARNING: !!!!!')
            format_to_tables(self.WAA.need_addagents_info)
            #print(self.WAA.current_need_addagents_ip_list)
            logger.info('# WARNING: !!!!!')
            input_yn = input('WARNING: !!!!!Please confirm to push full installation|yes or no ? yes/no : ')
            if input_yn == 'yes':
                logger.info('start push install task...')
                self.ED.split_execute(self.WAA.current_need_addagents_ip_list)
            else:
                logger.info('exit')
        else:
            self.ED.split_execute(ip_list)

    def check_install_results(self,id_list=None):
        logger.info('Check install task status')
        if id_list is None:
            install_task_cache = self.CD.install_task_cache()
            self.ED.echo_deploy_status(install_task_cache)
        else:
            logger.info(id_list)
            self.ED.echo_deploy_status(id_list)

if __name__ == '__main__':
    MP = MainActive()
    MP.check_install_results()

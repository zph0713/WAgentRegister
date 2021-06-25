import __init__
from core.analysislogic import WAgentsAnalysis
from core.notifications import MailProcess
from core.dataformat import format_to_tables,show_list
from core.mainprocess import MainActive
import argparse


def war_manager():
    parser = argparse.ArgumentParser(add_help=True,description='WAgentsRegister')
    parser.add_argument('-r','--remove_agents_args',help="remove_agents")
    parser.add_argument('-F','--force_get_data',action="store_true",help="force getting current data")
    parser.add_argument('-R','--remove_agents',action="store_true",help="remove_agents")
    parser.add_argument('-m','--notification_mail',help="inotification_mail,example:{lost_agents|down_agents|to_add}")
    parser.add_argument('-c','--check_results_args',help="install task results")
    parser.add_argument('-C','--check_results',action="store_true",help="install task results")
    parser.add_argument('-s','--show_infomation',help="show_infomation,example:{lost_agents|down_agents|to_add} ")
    parser.add_argument('-a','--add_agents_args',help="add_agents_args,install task results for arg,split used ',' ")
    parser.add_argument('-A','--add_agents',action="store_true",help="add_agents,install task results, ")
    parser.add_argument('-f','--filter',help="filter query field")

    obj = parser.parse_args()
    if obj.filter:
        WAA = WAgentsAnalysis(obj.filter,obj.force_get_data)
        MP = MailProcess(obj.filter)
        MA = MainActive(obj.filter)
    else:
        WAA = WAgentsAnalysis(None,obj.force_get_data)
        MP = MailProcess(None)
        MA = MainActive(None)
    if obj.show_infomation:
        if obj.show_infomation == 'lost_agents':
            format_to_tables(WAA.need_alert_info)
        elif obj.show_infomation == 'down_agents':
            format_to_tables(WAA.need_remove_info)
            show_list(WAA.need_remove_shutdown_info)
        elif obj.show_infomation == 'to_add':
            format_to_tables(WAA.need_addagents_info)
        else:
            print('example:{lost_agents|down_agents|to_add}')
    elif obj.notification_mail:
        if obj.notification_mail == 'lost_agents':
            MP.send_mail('lost_agents')
        elif obj.notification_mail == 'down_agents':
            MP.send_mail('down_agents')
        elif obj.notification_mail == 'to_add':
            MP.send_mail('to_add')
        else:
            print('example:{lost_agents|down_agents|to_add}')
    elif obj.add_agents_args:
        ip_list = obj.add_agents_args.split(',')
        MA.add_agents_process(ip_list)
    elif obj.check_results_args:
        id_list = obj.check_results_args.split(',')
        MA.check_install_results(id_list)
    elif obj.check_results:
        MA.check_install_results()
    elif obj.add_agents:
        MA.add_agents_process()
    elif obj.remove_agents_args:
        ip_list = obj.remove_agents_args.split(',')
        MA.remove_agents_process(ip_list)
    elif obj.remove_agents:
        MA.remove_agents_process()


if __name__ == '__main__':
    war_manager()

import __init__
from conf.settings import logger
from prettytable import PrettyTable


def format_to_tables(data_list):
    data_table = PrettyTable(['count','private_ip_address','status','cloud_vendor','agent_status','application_type'])
    count = 0
    for data in data_list:
        count+=1
        data_table.add_row([count,data['private_ip_address'],data['status'],data['cloud_vendor'],data['agent_status'],data['application_type']])
    logger.info(data_table)

def show_list(ip_list):
    data = dict()
    data['count'] = len(ip_list)
    data['shutdown_ip'] = ip_list
    logger.info(data)

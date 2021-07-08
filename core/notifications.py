import __init__
import pandas as pd
import os
import sys
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from conf import settings
from common.mails import Mail
from conf.settings import logger
from core.analysislogic import WAgentsAnalysis



class MailProcess(object):
    def __init__(self,cloud_filter):
        self.WAA = WAgentsAnalysis(cloud_filter)

    def generator_attachment(self,filename,data):
        df = pd.DataFrame(data=data)
        df = df.fillna(' ')
        html_mail_body = df.to_html(escape=False)
        att_list = list()
        file_path = os.path.join(settings.CacheDir,filename+'.html')
        att_list.append(file_path)
        with open(file_path,'w') as att:
            att.write(html_mail_body)
        return att_list

    def prepare_mail_content(self,need_active):
        if need_active == 'lost_agents':
            mail_subject = '[WazuhAgentsRegister]Agents Disconnected'
            mail_body = 'Wazuh disconnected machines: {}'.format(len(self.WAA.need_alert_info))
            mail_att = self.generator_attachment(need_active,self.WAA.need_alert_info)
        elif need_active == 'down_agents':
            mail_subject = '[WazuhAgentsRegister]VMs Server has offline'
            mail_body = 'CMDB shutdown machines: {}'.format(len(self.WAA.need_remove_info))
            mail_att = self.generator_attachment(need_active,self.WAA.need_remove_info)
        elif need_active == 'to_add':
            mail_subject = '[WazuhAgentsRegister]Need Register VMs'
            mail_body = 'The number of new installations currently required: {}'.format(len(self.WAA.need_addagents_info))
            mail_att = self.generator_attachment(need_active,self.WAA.need_addagents_info)
        else:
            exit(1)
        return mail_subject,mail_body,mail_att

    def send_mail(self,need_active):
        sub,body,att = self.prepare_mail_content(need_active)
        ML = Mail()
        ML.send_email(sub,body,att)


class SlackProcess(object):
    def __init__(self):
        pass

if __name__ == '__main__':
    MP = MailProcess('aliyun')
    MP.send_mail('lost_agents')

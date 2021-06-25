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

    def generator_html_mail(self,data):
        df = pd.DataFrame(data=data)
        df = df.fillna(' ')
        html_mail_body = df.to_html(escape=False)
        return html_mail_body

    def prepare_mail_content(self,need_active):
        if need_active == 'lost_agents':
            mail_subject = '[WazuhAgentsRegister]Agents Disconnected'
            mail_body = self.generator_html_mail(self.WAA.need_alert_info)
        elif need_active == 'down_agents':
            mail_subject = '[WazuhAgentsRegister]VMs Server has offline'
            mail_body = self.generator_html_mail(self.WAA.need_remove_info)
        elif need_active == 'to_add':
            mail_subject = '[WazuhAgentsRegister]Need Register VMs'
            mail_body = self.generator_html_mail(self.WAA.need_addagents_info)
        else:
            exit(1)
        return mail_subject,mail_body

    def send_mail(self,need_active):
        sub,body = self.prepare_mail_content(need_active)
        ML = Mail()
        ML.send_email(sub,body)


class SlackProcess(object):
    def __init__(self):
        pass

if __name__ == '__main__':
    MP = MailProcess()
    MP.send_mail('lost_agents')

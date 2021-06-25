import __init__
import os
import sys
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from conf import settings
from conf.settings import logger



class Mail(object):
    def __init__(self):
        self.smtp_user = settings.smtp_info.get('smtp_user')
        self.smtp_passwd = settings.smtp_info.get('smtp_passwd')
        self.smtp_server = settings.smtp_info.get('smtp_server')
        self.src_address = settings.smtp_info.get('src_address')
        self.smtp_port = settings.smtp_info.get('smtp_port')

    def send_email(self, subject, html_mail_body, attachments=None):
        logger.info('send mail..')
        logger.info('to {}'.format(settings.RECEIVERS))
        msg = MIMEMultipart()
        Receivers = ','
        msg['Subject'] = subject
        msg['From'] = self.src_address
        msg['To'] = Receivers.join(settings.RECEIVERS)
        msg.attach(MIMEText(html_mail_body, 'html'))

        if attachments and len(attachments) > 0:
            for f in attachments:
                with open(f, 'rb') as fil:
                    part = MIMEApplication(fil.read(), Name=basename(f))
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                msg.attach(part)

        smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
        #smtp.set_debuglevel(1)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(self.smtp_user, self.smtp_passwd)
        smtp.sendmail(self.src_address, settings.RECEIVERS, msg.as_string())
        smtp.quit()

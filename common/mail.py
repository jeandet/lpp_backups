#!/usr/bin/env python3

__author__ = "Alexis Jeandet"
__copyright__ = "Copyright 2017, Laboratory of Plasma Physics"
__credits__ = []
__license__ = "GPLv2"
__version__ = "1.0.0"
__maintainer__ = "Alexis Jeandet"
__email__ = "alexis.jeandet@member.fsf.org"
__status__ = "Development"

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(server, sender, recipients, subject, html_body):
    print(server)
    print(sender)
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients
    msg.attach(MIMEText(html_body, 'html'))
    s = smtplib.SMTP(server)
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()

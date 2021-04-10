from datetime import datetime, date
import os
import smtplib
import pathlib

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.mime.base import MIMEBase

# location of saved plot
filename = str(date.today()) + ".png"
dir = pathlib.Path(__file__).parent.absolute()
folder = r"/results/"
path = str(dir) + folder + filename

def send_email(path,dir):
    '''
        Send results via email
    '''

    COMMASPACE = ', '

    g_secret = os.environ['G-PW']
    mail1 = os.environ['MAIL1']
    mail2 = os.environ['MAIL2']

    gmail_user = mail1
    gmail_password = g_secret

    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = 'Simple Data Report: Time analysis'
    msg['From'] = gmail_user
    msg['To'] = COMMASPACE.join([mail1, mail2])
    msg.preamble = 'Simple Data Report: Time analysis'

    # Open the files in binary mode.  Let the MIMEImage class automatically
    # guess the specific image type.
    with open(path, 'rb') as fp:
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename='hours_plot.png')
        img.add_header('X-Attachment-Id', '0')
        img.add_header('Content-ID', '<0>')
        fp.close()
        msg.attach(img)

    # Attach the HTML email
    msg.attach(MIMEText(
    '''
    <html>
        <body>
            <h1 style="text-align: center;">Simple Data Report</h1>
            <p>Here could be a short description of the data.</p>
            <p><img src="cid:0"></p>
        </body>
    </html>'
    ''',
    'html', 'utf-8'))

    # Send the email via our own SMTP server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)

    server.sendmail(gmail_user, [mail1, mail2], msg.as_string())
    server.quit()

send_email(path, dir)
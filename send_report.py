from datetime import datetime, date
import pandas as pd
import numpy as np
import copy
import os
import smtplib
import matplotlib.pyplot as plt
import pathlib

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.mime.base import MIMEBase

#Dataset
x = [1,2,3,4,5,6,7,8,9,10]
y = [1,2,3,4,5,8,8,9,3,1]

def create_visualization(x,y):
    '''
        Create Visualization
    '''

    # Font size
    SMALL_SIZE = 18
    MEDIUM_SIZE = 20
    BIGGER_SIZE = 22

    plt.rc('font', size=22)          # controls default text sizes
    plt.rc('axes', titlesize=22)     # fontsize of the axes title
    plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
    plt.rc('legend', fontsize=18)    # legend fontsize
    plt.rc('figure', titlesize=22)  # fontsize of the figure title

    #plot diagram with matplotlib
    fig, ax = plt.subplots(figsize=(14, 7))

    #ax.bar(range(len(x_target)), y_target, width=0.35, label="Target working hours", color="grey")
    ax.bar(x,y, color='grey')
    #ax.set(xlabel='Day', ylabel='Hours [h]', title=f'Working hours')
    ax.set(xlabel='Day', ylabel='Hours [h]')

    #ax.legend(title="University")
    #plt.xticks(range(len(x)), y, size='small')

    #plt.xticks(rotation=45)
    # plt.show()

    # save the plot with date as filename in /results/
    filename = str(date.today()) + ".png"
    dir = pathlib.Path(__file__).parent.absolute()
    folder = r"/results/"
    path = str(dir) + folder + filename
    fig.savefig(path, dpi=fig.dpi)

    return path, dir

path, dir = create_visualization(x,y)

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
    msg['Subject'] = 'Working Hours Calc'
    msg['From'] = gmail_user
    msg['To'] = COMMASPACE.join([mail1, mail2])
    msg.preamble = 'Working Hours Calc'

    # to add an attachment is just add a MIMEBase object to read a picture locally.
    # with open(str(dir) + folder, 'w') as f:
    #     # set attachment mime and file name, the image type is png
    #     mime = MIMEBase('image', 'png', filename=filename)
    #     # add required header data:
    #     mime.add_header('Content-Disposition', 'attachment', filename='img1.png')
    #     mime.add_header('X-Attachment-Id', '0')
    #     mime.add_header('Content-ID', '<0>')
    #     # read attachment file content into the MIMEBase object
    #     mime.set_payload(f.read())
    #     # # encode with base64
    #     # encoders.encode_base64(mime)
    #     # add MIMEBase object to MIMEMultipart object
    #     msg.attach(mime)

    # # Open the files in binary mode.  Let the MIMEImage class automatically
    # # guess the specific image type.
    with open(path, 'rb') as fp:
        #fp = open(path, 'rb')
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename='hours_plot.png')
        img.add_header('X-Attachment-Id', '0')
        img.add_header('Content-ID', '<0>')
        fp.close()
        msg.attach(img)

    # msg.add_alternative("""\
    # <!DOCTYPE html>
    # <html>
    #     <body>
    #         <h1 style="color:SlateGray;">This is an HTML Email!</h1>
    #         <img src="results/2021-04-06.png" alt="Italian Trulli">
    #     </body>
    # </html>
    # """, subtype='html')


    msg.attach(MIMEText(
    '''
    <html>
        <body>
            <h1 style="text-align: center;">Simple Data Report</h1>
            <p><img src="cid:0"></p>
        </body>
    </html>'
    ''',
    'html', 'utf-8'))

    # import codecs
    # f = codecs.open(str(dir) + "/email.html", 'r')
    # string = f.read()
    # print(string)
    # msg.attach(MIMEText(string,'html', 'utf-8'))

    # Send the email via our own SMTP server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)

    server.sendmail(gmail_user, [mail1, mail2], msg.as_string())
    server.quit()

send_email(path, dir)
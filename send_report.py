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

import codecs

#Dataset
x = [1,2,3,4,5,6,7,8,9,10]
y = [1,2,3,4,5,8,8,9,3,1]

def create_visualization(x,y):
    '''
        Create Visualization
        return:
            - saves the created plot in ./results/
            - dir: path to working directory
            - path: path to saved plot
    '''

    plt.rc('font', size=22)          # controls default text sizes
    plt.rc('axes', titlesize=22)     # fontsize of the axes title
    plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
    plt.rc('legend', fontsize=18)    # legend fontsize
    plt.rc('figure', titlesize=22)  # fontsize of the figure title

    #plot diagram with matplotlib
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.bar(x,y, color='grey')
    ax.set(xlabel='Day', ylabel='Hours [h]')

    # save the plot with date as filename in ./results/
    filename = str(date.today()) + ".png"

    # working directory
    dir = pathlib.Path(__file__).parent.absolute()

    # folder where the plots should be saved
    folder = r"/results/"

    path_plot = str(dir) + folder + filename

    # save plot
    fig.savefig(path_plot, dpi=fig.dpi)

    return path_plot, dir

path_plot, dir = create_visualization(x,y)

# path to plot image
filename = str(date.today()) + ".png"
dir = pathlib.Path(__file__).parent.absolute()
folder = r"/results/"
path = str(dir) + folder + filename

# path to header image
folder_img = r"/img/"
path_img =  str(dir) + folder_img + "header_img.png"

# Settings
from_mail = os.environ['from_mail']  # "test.name@googlemail.com"
from_password = os.environ['G-PW']  # "password123"
to_mail = os.environ['to_mail']  # "test@outlook.com"
smtp_server = "smtp.gmail.com"
smtp_port = 465

def send_email(path_plot, smtp_server, smtp_port, from_mail, from_password, to_mail):
    '''
        Send results via email
    '''

    COMMASPACE = ', '

    from_password = os.environ['G-PW']
    from_mail = os.environ['from_mail']
    to_mail = os.environ['to_mail']

    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = 'Simple Data Report: Time analysis'
    msg['From'] = from_mail
    msg['To'] = COMMASPACE.join([from_mail, to_mail])
    msg.preamble = 'Simple Data Report: Time analysis'

    # Open the files in binary mode.  Let the MIMEImage class automatically
    # guess the specific image type.
    with open(path, 'rb') as fp:
        #fp = open(path, 'rb')
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename='hours_plot.png')
        img.add_header('X-Attachment-Id', '0')
        img.add_header('Content-ID', '<0>')
        fp.close()
        msg.attach(img)

    with open(path_img, 'rb') as fp:
        #fp = open(path, 'rb')
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename='header.png')
        img.add_header('X-Attachment-Id', '1')
        img.add_header('Content-ID', '<1>')
        fp.close()
        msg.attach(img)

    # Attach the HTML email
    f = codecs.open(str(dir) + "/email.html", 'r')
    string = f.read()

    # Replace the relative path to images with ContentID
    html_string = string.replace("./results/2021-04-08.png", "cid:0")
    html_string = html_string.replace("./img/header_img.png", "cid:1")

    msg.attach(MIMEText(html_string, 'html', 'utf-8'))

    # Send the email via our own SMTP server
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.ehlo()
    server.login(from_mail, from_password)

    server.sendmail(from_mail, [from_mail, to_mail], msg.as_string())
    server.quit()

send_email(path_plot, smtp_server, smtp_port, from_mail, from_password, to_mail)
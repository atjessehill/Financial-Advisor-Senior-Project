import smtplib
from os import path
import config
import os

from string import Template

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


MY_ADDRESS = 'stockmarketsubscription@gmail.com'
PASSWORD = 'ajdn2019seniorproject'


def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """

    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails


def read_template(filename):
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def integrated_test():

    basepath = path.dirname(__file__)
    contact_path = path.abspath(path.join(basepath, "contacts.txt"))

    names, emails = get_contacts(contact_path)  # read contacts

    report_file = open('output/E81WN.html')
    html = report_file.read()

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    img_data = open('1O247.png', 'rb').read()

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()

        # setup the parameters of the message
        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = "Your Personalized Weekly Stock Research"

        # add in the message body
        msg.attach(MIMEText(html, 'html'))
        # We reference the image in the IMG SRC attribute by the ID we give it below

        image = MIMEImage(img_data, name=os.path.basename('graph.png'))
        msg.attach(image)

        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg

    # Terminate the SMTP session and close the connection
    s.quit()

def django_email(email, template, graph):

    print(email, template, graph, '******')
    #basepath = path.dirname(__file__)
    # contact_path = path.abspath(path.join(basepath, "contacts.txt"))
    #
    # names, emails = get_contacts(contact_path)  # read contacts

    graph_path = 'frontend/static/images/graphs/' + graph
    template_path = 'frontend/static/output/emailOutput/' + template

    graph_path = os.path.abspath(os.path.join(graph_path))

    template_path = os.path.abspath(os.path.join(template_path))

    print(template_path)
    report_file = open(template_path)
    html = report_file.read()

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    img_data = open(graph_path, 'rb').read()

    # For each contact, send the email:
    # for name, email in zip(names, emails):
    msg = MIMEMultipart()

    # setup the parameters of the message
    msg['From'] = MY_ADDRESS
    msg['To'] = email
    msg['Subject'] = "Your Personalized Weekly Stock Research"

    # add in the message body
    msg.attach(MIMEText(html, 'html'))
    # We reference the image in the IMG SRC attribute by the ID we give it below

    image = MIMEImage(img_data, name=os.path.basename(graph_path))
    msg.attach(image)

    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()


if __name__ == '__main__':
    integrated_test()
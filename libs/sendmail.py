import sendgrid
import os
from sendgrid.helpers.mail import Email, Content, Mail
from appsrc import variables
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SENDGRID_API_KEY=os.environ.get('SENDGRID_API_KEY', '')
APPNAME=os.environ.get('APPNAME', '')
FROM_EMAIL = Email("contact@jraulouvre.net", "JR Au Louvre")
SUBJECT = {'fr' :  "JR Au Louvre - Confirmation d'inscription", 
'en' : "JR Au Louvre : Registration confirmation"}


def print_html_doc():
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(loader=FileSystemLoader('templates/jraulouvre'),
                         trim_blocks=True)
    print(j2_env.get_template('email.html').render())


def sendEmail(emailTo, Firstname, Lastname, Birthdate, Confirmation, Id, Shift, Telephone, Language):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    
    bcc = "contact@jraulouvre.net"
    #content = Content("text/plain", "Hello, Email!")
    data =  Environment(loader=FileSystemLoader('templates/jraulouvre'),
                        trim_blocks=True).get_template('email_' + Language + '.html').render(
                        Firstname=Firstname,
                        Lastname=Lastname,
                        Birthdate = Birthdate,
                        Email=emailTo,
                        Confirmation=Confirmation,
                        Shift=Shift,
                        Id=Id ,  
                        Telephone=Telephone,
                        language=Language, 
                        appname=APPNAME,
                        Date =  datetime.now().strftime("%d-%m-%Y"))
    


    dataPerso = {
    "personalizations": [
        {
        "to": [{
                "email": emailTo
            }],
        "subject": SUBJECT[Language]
        }
    ],
    "from": {
        "email": "contact@jraulouvre.net"
    },
    "bcc":
    {
        "email":bcc
    },
    "content": [
        {
        "type": "text/html",
        "value": data
        }
    ]
    }

    response = sg.client.mail.send.post(request_body=dataPerso)
    
    # previous version without bcc
    #mail_html = Content(type_='text/html', value=data)
    #to_email = Email(emailTo)
    #mail = Mail(FROM_EMAIL, SUBJECT[Language], to_email, mail_html)
    #response = sg.client.mail.send.post(request_body=mail.get())


    #print("#####################")
    #print(response.status_code)
    #print("#####################")
    #print(response.body)
    #print("#####################")
    #print(response.headers)
    #print("#####################")

#sendEmail('augustin.rieunier@gmail.com', "Augustin", "Rieunier", "27-04-1983", "ZERE", "2344", "Shift Name")

#mail_html = Content(type_='text/html', value='<h1>Test Mail</h1><p>This is a test email message.</p>')
#mail_txt = Content(type_='text/plain', value='This is a test email message.')
#mail = Mail(mail_from, mail_subject, mail_to, mail_html)
#mail.add_content(mail_txt)
#response = sg.client.mail.send.post(request_body=mail.get())
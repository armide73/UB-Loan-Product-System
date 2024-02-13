import jinja2
from dotenv import load_dotenv
load_dotenv()
import requests
import os


class ToSendMail():

    def __init__(self):
        self.template_loader = jinja2.FileSystemLoader("templates")
        self.template_env = jinja2.Environment(loader=self.template_loader)


    def render_template(self,template_filename, **context):
        return self.template_env.get_template(template_filename).render(**context)


    def send_simple_message(self,username='',sendto='armide.tuyi@gmail.com'):
        return requests.post(
            f"https://api.mailgun.net/v3/{os.getenv('MAILGUN_DOMAIN')}/messages",
            auth=("api", f"{os.getenv('MAILGUN_API_KEY')}"),
            data={"from": f"UNGUKA <mailgun@{os.getenv('MAILGUN_DOMAIN')}>",
                "to": [sendto],
                "subject": "UNGUKA BANK ACCOUNT CREATED",
                "text": "UNGUKA BANK ACCOUNT IS SUCCESSFULLY CREATED",
                "html": self.render_template("pages/email.html",username=username)
                })
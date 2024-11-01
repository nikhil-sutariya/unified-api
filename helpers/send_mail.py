from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Environment, FileSystemLoader
from config import get_settings, logger
import smtplib
import os

settings = get_settings()

def send(subject:str, recipient: list | str, template_name:str, context: dict):
    try:
        message = MIMEMultipart('alternative')
        message['From'] = settings.smtp_email_from
        message['To'] = ', '.join(recipient) if type(recipient) == list else recipient
        message['Subject'] = subject

        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template(template_name)
        html_content = template.render(context)

        html_part = MIMEText(html_content, 'html')
        message.attach(html_part)

        images = ['redoc.png', 'firestore-fb.png']

        for image_name in images:
            image_path = os.path.join('static/images', image_name)

            if os.path.exists(image_path):
                with open(image_path, 'rb') as img_file:
                    img = MIMEBase('application', 'octet-stream')
                    img.set_payload(img_file.read())
                    encoders.encode_base64(img)
                    img.add_header('Content-Disposition', f'attachment; filename={image_name}')
                    message.attach(img)

        with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            
            if isinstance(recipient, list):
                server.sendmail(message['From'], recipient, message.as_string())
            else:
                server.sendmail(message['From'], message['To'], message.as_string())
    
    except Exception as e:
        logger.error(str(e))

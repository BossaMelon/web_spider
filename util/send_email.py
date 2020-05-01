import smtplib
from email.mime.text import MIMEText
import config


def send_email(message):
    fromx = config.email_address
    to = config.email_address
    msg = MIMEText(message)
    msg['Subject'] = 'info from python'
    msg['From'] = fromx
    msg['To'] = to

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.ehlo()
    server.login(config.email_address, config.email_password)
    server.sendmail(fromx, to, msg.as_string())
    server.quit()


if __name__ == '__main__':
    course_title = 'course'
    total_time = 123124.9876
    message = f'{course_title} download complete! Total time: {total_time:.2f}s'
    send_email(message)


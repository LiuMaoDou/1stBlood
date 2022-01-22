import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
me = "liujian_nan1986@163.com"


def send_email_ted(title, content, who):
    # ### 1.邮件内容配置 ###
    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = formataddr(["Ted Liu", me])
    msg['Subject'] = title

    # ### 2.发送邮件 ###
    server = smtplib.SMTP_SSL("smtp.163.com")
    server.login(me, "***")
    server.sendmail(me, who, msg.as_string())
    server.quit()


if __name__ == "__main__":
    send_email_ted('题目','内容','liujiannan1986@gmail.com')
    print("---Email Sent---")

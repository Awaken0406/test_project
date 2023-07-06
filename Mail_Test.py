import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# 邮件发送方的邮箱地址和邮箱密码
sender_email = 'SenGeMail@163.com'
sender_password = 'TKTHLXRKIFHWZRXY'

# 邮件接收方的邮箱地址
recipient_email = '734697554@qq.com'

# 邮件主题和内容
subject = '邮件测试!!!'
body = '邮件测试!'

# 创建 MIMEMultipart 对象，用于组合邮件主体和附件
message = MIMEMultipart()
message['Subject'] = subject
message['From'] = sender_email
message['To'] = recipient_email

# 添加邮件正文
message.attach(MIMEText(body))

# 添加附件

filename = 'example.txt'
with open(filename, 'rb') as f:
    attachment = MIMEApplication(f.read(), _subtype='txt')
    attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    #message.attach(attachment)



# 链接邮件服务器并发送邮件
with smtplib.SMTP_SSL('smtp.163.com', 465) as server:
    server.login(sender_email, sender_password)
    ret = server.sendmail(sender_email, recipient_email, message.as_string())

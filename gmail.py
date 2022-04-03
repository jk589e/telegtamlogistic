import smtplib as smtp
import os; import locale;
os.environ["PYTHONIOENCODING"] = "utf-8";
user = 'jk58e91@yandex.ru'
password = 'IWillSurv1ve'


dest_email = 'evejiny@gmail.com'
subject ='zhopa'
email_text = 'code 12344556'




message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(user,
                                                       dest_email,
                                                       subject,
                                                       email_text)

server = smtp.SMTP_SSL('smtp.yandex.com')
server.set_debuglevel(1)
server.ehlo(user)
server.login(user, password)
server.auth_plain()
server.sendmail(user, dest_email, message)
server.quit()

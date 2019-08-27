import unittest
from HTMLTestRunner import HTMLTestRunner
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

def new_file(test_dir):
	lists = os.listdir(test_dir)
	lists.sort(key=lambda fn:os.path.getmtime(test_dir+'\\'+fn))
	file_path = os.path.join(test_dir, lists[-1])
	return file_path

def send_email(newfile):
	f = open(newfile, 'rb')
	mail_body=f.read()
	f.close()
	smtpserver = "smtp.163.com"
	user = "your_email_address"
	passwd = "your_email_password"
	sender = user
	receiver = "target_email_address"
	subject = "自动定时发送报告%s" % (time.strftime("%Y%m%d"))

	msg = MIMEMultipart()

	msg_html = MIMEText(mail_body, 'html', 'utf-8')
	msg_html['Content-Disposition'] = 'attachment; filename="TestReport.html'
	msg.attach(msg_html)

	msg['From'] = sender
	msg['To'] = receiver
	msg['Subject'] = subject

	smtp = smtplib.SMTP()
	smtp.connect(smtpserver, '25')
	# smtp.set_debuglevel(1)
	smtp.login(user, passwd)
	smtp.sendmail(sender, receiver, msg.as_string())
	smtp.quit()

if __name__ == '__main__':
	print("=============AutoTest Start=============")
	test_dir = r"test_case"
	test_report_dir = r"report"
	# from test_case import test_baidu
	# from test_case import test_youdao

	# suite = unittest.TestSuite()
	# suite.addTest(test_baidu.BaiduTest("test_baidu"))
	# suite.addTest(test_youdao.YoudaoTest("test_youdao"))
	discover = unittest.defaultTestLoader.discover(test_dir, pattern="test_*.py")
	now = time.strftime("%Y-%m-%d_%H_%M_%S_")
	filename = test_report_dir+"\\"+now+"result.html"
	fp = open(filename, 'wb')
	runner = HTMLTestRunner(stream=fp, title=u'测试报告', description=u'用例执行情况:')
	runner.run(discover)
	# runner.run(suite)
	fp.close()
	new_report=new_file(test_report_dir)
	send_email(new_report)

	print("=============AutoTest Over==============")

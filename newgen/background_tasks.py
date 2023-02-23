from background_task import background
import smtplib
import ssl
from email.message import EmailMessage
import datetime
import secrets
import string
import datetime
#EMAIL DATA
from newgen.functions import NewVerificationNote, GetEmailByClosedId, IsJobDeclined, Acceptjob
email_sender = 'gfifx1@gmail.com'
email_password = 'ilvmmqpvobmckmbr'


@background(schedule=5)
def confirming_email(email, request_id):
	print(f"Confirmation sended to  {email} at {datetime.datetime.now()}")

	email_receiver = email
	subject = 'Подтверждение E-mail'
	alphabet = string.ascii_letters + string.digits
	password = ''.join(secrets.choice(alphabet) for i in range(20))  # for a 20-character password
	body = f"Если Ваша организация создавала заявку, то для подтверждения Email и внесения его в базу скопируйте код активации (ниже) и перейдите по ссылке \n\n{password} \n\n\n http://127.0.0.1:8000/confirm_email/"
	em = EmailMessage()
	em['From'] = email_sender
	em['To'] = email_receiver
	em['Subject'] = subject
	em.set_content(body)
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
		smtp.login(email_sender, email_password)
		smtp.sendmail(email_sender, email_receiver, em.as_string())
	NewVerificationNote(password,request_id,email)





@background(schedule=5)
def new_request_opened(email, problem):
	print(f"new_request_opened from {email} was open at {datetime.datetime.now()}")
	email_receiver = email
	subject = 'Новая заявка'
	body = f"Ваша заявка {problem} открыта"
	em = EmailMessage()
	em['From'] = email_sender
	em['To'] = email_receiver
	em['Subject'] = subject
	em.set_content(body)
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
		smtp.login(email_sender, email_password)
		smtp.sendmail(email_sender, email_receiver, em.as_string())

@background(schedule = 3)
def request_is_closed(close_request_id,encrypted_url):
	email = GetEmailByClosedId(close_request_id)
	print(f"Result sended to  {email} at {datetime.datetime.now()}")
	email_receiver = email
	subject = 'Отчёт о выполненной работе'

	body = f"Работа по Вашей заявке выполена.\n\n Перейдите по ссылке ниже для подтверждения и оценки выполненной работы\n\n http://127.0.0.1:8000/job_evaluation/{encrypted_url}\n\nЕсли не будет предпринято никаких действий, то через 2 дня выполненная работа будет считаться принятой"
	em = EmailMessage()
	em['From'] = email_sender
	em['To'] = email_receiver
	em['Subject'] = subject
	em.set_content(body)
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
		smtp.login(email_sender, email_password)
		smtp.sendmail(email_sender, email_receiver, em.as_string())
	accept_if_forgotten(close_request_id)

@background(schedule = datetime.timedelta(days=2))
def accept_if_forgotten(close_request_id):
	try:
		if IsJobDeclined(close_request_id) is None:
			Acceptjob(close_request_id)
	except Exception as e:
		print(e)

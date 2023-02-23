import os
from django.contrib.auth.models import User
#from notifications.signals import notify
import base64
from PIL import Image
import io
import datetime
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from newgen.classes import *
from newgen.models import *

from django.contrib import messages

def AddFullReport(worker_fullname, object_name, spended_time):

	if not TotalSpendedTimeOnObject.objects.filter(worker_fullname = worker_fullname,object_name = object_name).exists():
		export = TotalSpendedTimeOnObject()
		export.worker_fullname = worker_fullname
		export.object_name = object_name
		export.spended_time = spended_time
		export.save()
	else:
		export = TotalSpendedTimeOnObject.objects.filter(worker_fullname = worker_fullname,object_name = object_name).first()
		export.spended_time = export.spended_time + float(spended_time)
		export.save()

def AddWorkNote(worker_id, object_id, spended_time, comments):

	work = Work()

	try:
		note_id = Work.objects.latest("note_id").note_id + 1
	except:
		note_id = 1
	work.note_id = note_id
	work.worker_id = worker_id
	work.object_id = object_id
	work.date = datetime.date.today()
	work.spended_time = spended_time
	work.comments = comments

	work.save()

def AddEmail(email):
	new_email = Email()
	try:
		email_id = Email.objects.latest("email_id").email_id + 1
	except:
		email_id = 1
	new_email.email_id = email_id
	new_email.email = email
	new_email.status = False
	new_email.save()

def GetWorker(request):
	return Worker.objects.filter(user_id = request.user.id).first()

def GetObject(request, item):
	return request.POST.get(item)

def GetWorkerByName(short_name):
	for worker in Worker.objects.all():
		if str(worker.fullname).split(" ")[0] +" "+str(worker.fullname).split(" ")[1] == short_name:
			return worker

def GetWorkersResults(worker_fullname):
	dates = []
	objects = []
	spended_time = []

	list_of_works = []
	for work in Work.objects.filter(worker_id = worker_fullname):
		objects.append(str(work.object_id))
		dates.append(work.date)
		spended_time.append(work.spended_time)
	for i in range(len(dates)):
		list_of_works.append(EndedWorks(objects[i],dates[i], spended_time[i]))

	return list_of_works

def NewVerificationNote(code,request_id,email):
	verification = EmailVerification()
	try:
		note_id = EmailVerification.objects.latest("note_id").note_id + 1
	except:
		note_id = 1
	verification.note_id = note_id
	verification.activation_code = code
	verification.open_request = GetFirstFilteredNote(OpenRequest,"note_id", request_id)
	verification.expiry_date = datetime.date.today() + datetime.timedelta(days=2)
	verification.email = email
	verification.save()

def GetInstallers():
	installers_ids = []
	installers = []
	for user in User.objects.all():
		if str( user.groups.all().first()) == "Монтажники":
			installers_ids.append(user.id)

	for installer_id in installers_ids:
		installers.append(Worker.objects.filter(user = installer_id).first())
	return installers

def GetGroupMembers(group_name):
	filling_list = []
	ids = []
	for user in User.objects.all():
		if str(user.groups.all().first()) == group_name:
			ids.append(user.id)
	for user_id in ids:
		filling_list.append(Worker.objects.filter(user = user_id).first())
	return filling_list

def GetFirstFilteredNote(model, field, subject):
	search_type = 'contains'
	filter = field + '__' + search_type
	return model.objects.filter(**{ filter: subject }).first()

def IsExists(model, field, subject):
	search_type = 'contains'
	filter = field + '__' + search_type
	return model.objects.filter(**{ filter: subject }).exists()

def AddNewRequestNote(request):
	is_email_active = True
	new_request = OpenRequest()

	email = GetObject(request,"email")
	
	if GetFirstFilteredNote(Email,"email",email) == None:
		AddEmail(email)
		is_email_active = False

	try:
		note_id = OpenRequest.objects.latest("note_id").note_id + 1
	except:
		note_id = 1

	new_request.note_id = note_id
	new_request.organisation = GetObject(request,"organisation")
	new_request.phone_number = GetObject(request,"phohe_number")
	new_request.priority = GetFirstFilteredNote(UrgencyStatus,"status",GetObject(request,"priority"))
	new_request.date = datetime.date.today()
	new_request.problem_description = GetObject(request,"problem_description")

	if not is_email_active:
		new_request.email =GetFirstFilteredNote(Email,"email",email)
		new_request.status = GetFirstFilteredNote(RequestStatus,"status_id",3)
		new_request.save()
		messages.success(request, "Для подтверждения Email Вам отправлено письмо на почту, проверьте")
		confirming_email(email,new_request.note_id)
	else:
		cur_email = GetFirstFilteredNote(Email,"email",email)
		new_request.email = cur_email
		if cur_email.is_active:
			new_request.status = GetFirstFilteredNote(RequestStatus,"status_id",1)
			messages.success(request, "Новая заявка создана")
		else:
			confirming_email(email,new_request.note_id)
			new_request.status = GetFirstFilteredNote(RequestStatus,"status_id",3)
			messages.success(request, "Для подтверждения Email Вам отправлено письмо на почту, проверьте")
		new_request.save()

def GetFirstWord(sentence):
	return sentence.split(" ")[0]

def GetPhotos(request):
	photos = []
	for i in range(3):
		photo_name = f"{GetObject(request,'request_id')}_{datetime.datetime.now().hour}_{datetime.datetime.now().minute}_{i}.jpg"
		print(photo_name)
		asas = str(request.POST.get("photo" + str(i+1) + "base")).split(",")[1]
		ct = str(request.POST.get("photo" + str(i+1) + "base")).split(",")[0]
		image = base64.b64decode(asas)
		byt = io.BytesIO(base64.b64decode(asas))
		image = InMemoryUploadedFile(byt,field_name='picture',name=photo_name,content_type=ct,size=sys.getsizeof(byt),charset=None)
		photos.append(image)
	return photos


def CloseRequest(open_request_id,responsible_list,photos,comment):

	try:
		note_id = ClosedRequest.objects.latest("note_id").note_id + 1
	except:
		note_id = 1

	closed_request = ClosedRequest()
	closed_request.note_id = note_id
	closed_request.open_request = GetFirstFilteredNote(OpenRequest,"note_id",open_request_id)
	closed_request.date = datetime.date.today()
	closed_request.photo_1 = photos[0]
	closed_request.photo_2 = photos[1]
	closed_request.photo_3 = photos[2]
	closed_request.comment = comment
	closed_request.responsible = "_".join(person for person in responsible_list)

	closed_request.save()
	return note_id

def GetEmailByClosedId(closed_request_id):
	open_request_id = GetFirstFilteredNote(ClosedRequest,"note_id",closed_request_id).open_request
	return str(GetFirstFilteredNote(OpenRequest,"note_id",open_request_id.note_id).email)

def IsJobDeclined(closed_request_id):
	open_request_id = GetFirstFilteredNote(ClosedRequest,"note_id",closed_request_id).open_request
	return DeclinedRequest.objects.filter(open_request = open_request_id.note_id).first()
def Acceptjob(closed_request_id):
	note = GetFirstFilteredNote(ClosedRequest,"note_id",closed_request_id)
	note.is_accepted = True
	note.save()

def AddDeclinedRequest(open_request, responsible, comment):
	try:
		note_id = DeclinedRequest.objects.latest("note_id").note_id + 1
	except:
		note_id = 1

	declined_request = DeclinedRequest()
	declined_request.note_id = note_id
	declined_request.responsible = responsible
	declined_request.date = datetime.date.today()
	declined_request.open_request = open_request
	declined_request.comment = comment
	declined_request.save()
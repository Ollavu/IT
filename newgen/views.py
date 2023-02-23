from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import newgen.models as mo
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.forms.models import model_to_dict
from django.contrib import admin

#from top.objects import *
from newgen.tools import *
from newgen.functions import *
from newgen.background_tasks import *
#from top.open_func import *
from django.contrib.auth.models import Group

from django.template.loader import render_to_string
from django.db.models import Q

from cryptography.fernet import Fernet
cipher_key = Fernet.generate_key()
cipher = Fernet(cipher_key)


@login_required
def mainworker(request):

	if request.user.is_superuser:
		return HttpResponseRedirect(reverse('admin:index'))
	if str(request.user) == 'tools':
		return HttpResponseRedirect(reverse('tools'))
	if request.user.groups.first().id == 3:
		return HttpResponseRedirect(reverse('it'))

	user = request.user
	objects = []
	orig_notes =[]
	shedule_list = []

	#print(request.user.groups.first().id)
	#1 - ГРУППА БРИГАДИРОВ

	workers = engineers = GetGroupMembers("Монтажники")
	worker = GetWorker(request)
	history = GetWorkersResults(worker.worker_id)
	#print(request)
	#TOOL NOTE
	for tool_note in mo.ToolsReport.objects.filter(~Q(worker_id = worker.worker_id)):
		orig_notes.append(tool_note)

	#OBJECTS
	for objectx in mo.Object.objects.filter(is_active = True):
		objects.append(objectx.name)

	#SHEDULES
	shedules = mo.Shedule.objects.filter(date__gte = datetime.date.today())

	if shedules.exists():
		for shedule in shedules:
			if str(shedule.leader) == str(worker.fullname):
				shedule_list.append(shedule)
				continue
			if worker in shedule.workers.all():
				shedule_list.append(shedule)

	return render(request,"mainworker.html",{'objects': objects,'history':history, 'worker':worker,
		'user': user, 'workers': workers, 'orig_notes':orig_notes,
	  'shedule':shedule_list})

def notice_work(request):
	workers=[]

	#3 fields + token + object
	workers_to_notice = round((len(dict(request.POST.lists()))-2)/3)

	object_name = GetObject(request,"object")

	for i in range(workers_to_notice):
		worker_short_name = GetObject(request,"worker_" + str(i+1))
		time = GetObject(request,"time_" + str(i+1))
		comment = GetObject(request,"comment_" + str(i+1))
		worker = GetWorkerByName(worker_short_name)
		obj = GetFirstFilteredNote(mo.Object,"name",object_name)

		AddWorkNote(worker, obj, time, comment)
		AddFullReport(worker.fullname, obj.name, time)

	#bg_task()
	messages.success(request, "Всё записано, спасибо")
	return HttpResponseRedirect("../")

def tool_transfers(request):

	user = GetFirstFilteredNote (User, "username",request.user)
	workername = Worker.objects.filter(user = user.id).first().fullname

	try:
		temp_transfers_id = request.POST.getlist(workername)
		for note_id in temp_transfers_id:
			temp_note = GetFirstFilteredNote(mo.TempToolTransfers,"note_id",note_id)
			if request.POST.get(note_id) == "+":
				try:
					RefreshToolReportNote(temp_note.tool_name,temp_note.worker_id)
					AddToolForward(temp_note.tool_name,temp_note.worker_id,"")
				except Exception as e:
					print(e)
			temp_note.delete()
	except Exception as e:
		messages.warning(request,"Гавнина с обновой записей")
		return HttpResponseRedirect("../")
	messages.success(request, 'Данные по оборудованию обновлены')
	return HttpResponseRedirect("../")

def edit_tool(request):
	tool = GetTool(request.POST.get("tool"))
	if tool is None:
		messages.warning(request, "Такого инструмента нет")
		return HttpResponseRedirect("../")
	new_tool_name = request.POST.get("new_tool_name")
	try:
		tool.name = request.POST.get("new_tool_name")
		tool.save()
		messages.success(request, "Название изменено")
	except Exception as e:
		print(e)
		messages.warning(request,e)
		return HttpResponseRedirect("../")
	return HttpResponseRedirect("../")

def delete_tool(request):
	if DeleteTool(request.POST.get("tool")):
		messages.success(request, "Инструмент удалён из БД")
	else:
		messages.warning(request, "Что-то не то")
	return HttpResponseRedirect("../")

def tools(request):
	worker = GetWorker(request)
	tools =[]
	workers = []
	tools_notes = []
	transfers = []
	temp_transfers = []
	orig_notes =[]
	#TOOLS
	for tool in mo.Tools.objects.all():
		if  not mo.TempToolTransfers.objects.filter(tool_id = tool.tool_id).exists():
			tools.append(tool)

	#WORKER
	for another_worker in mo.Worker.objects.all():
		workers.append(another_worker)

	#TOOL NOTE
	for tool_note in mo.ToolsReport.objects.all():
		if str(tool_note.worker_id) != str(worker.fullname):
			orig_notes.append(tool_note)
		tools_notes.append(tool_note)
	#TRANSFERS
	for transfer in mo.ToolsForwarding.objects.order_by('-note_id'):
		transfers.append(transfer)

	#TEMP TRANSFERS
	for temp_transfer in mo.TempToolTransfers.objects.all():
		temp_transfers.append(temp_transfer)

	return render(request,"tools/tools.html",{'tools_notes': tools_notes, 'tools': tools, 'workers': workers,
	 'transfers':transfers, 'temp_transfers':temp_transfers, 'orig_notes':orig_notes})

def add_tool(request):
	if 'submit' in request.POST:
		print(111)
	if AddTool(request.POST.get("tool_name")):
		AddToolReportNote(request.POST.get("tool_name"))
		messages.success(request, "Новый инструмент добавлен")
	else:
		messages.warning(request,"Инструмент с таким названием уже есть")
	return HttpResponseRedirect("../")

def tool_forwarding(request):
	try:
		user = User.objects.filter(username = request.user).first()
		worker = Worker.objects.filter(user = user.id).first()
		tool = Tools.objects.filter(name = request.POST.get("tool")).first()
		comments = request.POST.get("comments")
		AddToolForward(tool, worker, comments)
		RefreshToolReportNote(tool, worker)
		messages.success(request, "Вы взяли инструмент")
	except Exception as e:
		print(e)
		messages.warning(request, "Инструмент не был оформлен на Вас")
	if str(request.user) == "tools":
		AddTempToolTransfer(tool, worker, comments)
	return HttpResponseRedirect("../")

def delete_temp_note(request):
	user = User.objects.filter(username = request.user).first()
	tool = mo.Tools.objects.filter(name = request.POST.get("tool_name")).first()
	worker = mo.Worker.objects.filter(fullname = request.POST.get("worker_name")).first()
	print(request)
	try:
		mo.ToolsForwarding.objects.filter(worker_id = worker.worker_id, tool_name = tool.tool_id).first().delete()
		mo.TempToolTransfers.objects.filter(worker_id = worker.worker_id, tool_id = tool.tool_id).first().delete()
		messages.success(request,"Передача отменена")
	except Exception as e:
		messages.error(request,str(e) +" temp")

	
	#ВЕРНУТЬ ПРОШЛОГО ХОЗЯИНА
	old_transfer = mo.ToolsForwarding.objects.filter(tool_name = tool.tool_id).first()
	old_worker = mo.Worker.objects.filter(fullname = old_transfer.worker_id).first()
	RefreshToolReportNote(tool,old_worker)
	return HttpResponseRedirect("../")


####################################################################################################################
def organisations_requests(request):
	if not request.session or not request.session.session_key:
		request.session.save()
	statuses = []
	for status in mo.UrgencyStatus.objects.all().order_by('-status_id'):
		statuses.append(status.status)
	return render(request,"organisations_requests.html",{'statuses':statuses})

def new_request(request):
	AddNewRequestNote(request)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def confirm_email(request):
	code = GetObject(request,"code")
	verification_obj =  GetFirstFilteredNote(EmailVerification,"activation_code",code)

	if verification_obj == None:
		messages.error(request, "Недействительный ключ активации")
	else:
		if datetime.date.today() > verification_obj.expiry_date:
			messages.error(request, "Данный ключ больше не активен")
		else:

			#ACTIVATE REQUEST
			related_request = mo.OpenRequest.objects.filter(note_id = verification_obj.open_request.note_id).first()
			related_request.status =  GetFirstFilteredNote(RequestStatus,"status_id",1)
			related_request.save()

			#ACTIVATE EMAIL
			related_email =GetFirstFilteredNote(mo.Email,"email",verification_obj.email)
			related_email.is_active = True
			related_email.save()

			#DELETE CODE
			GetFirstFilteredNote(EmailVerification,"activation_code",code).delete()
			messages.success(request, "Ваш Email подтверждён")

	return render(request,"inserting_auth_code.html")

def inserting_auth_code(request):
	return render(request,"inserting_auth_code.html")

def it(request):

	engineers = GetGroupMembers("Инженеры")
	active_requests = []
	accepted_requests = []

	for closed_request in ClosedRequest.objects.filter(is_accepted = True):
		accepted_requests.append(closed_request)

	for active_request in mo.OpenRequest.objects.filter(status = 1):
		if not len(ClosedRequest.objects.filter(open_request = active_request.note_id)):
			active_requests.append(active_request)

	return render(request,"it/it.html",{'active_requests':active_requests, 'engineers':engineers,'accepted_requests':accepted_requests})

def add_temp_close_request(request):
	open_request_id = GetObject(request,"request_id")
	photos = GetPhotos(request)
	responsible_list = request.POST.getlist("responsible")
	comment = GetObject(request,"comment")
	close_request_id = CloseRequest(open_request_id,responsible_list,photos,comment)
	messages.success(request, "Всё отправлено, спасибо")
	#encode id -> str -> bytes -> str -> remove "==" -> send email
	encrypted_text = cipher.encrypt(f'{close_request_id}'.encode('utf-8'))
	request_is_closed(close_request_id,encrypted_text.decode('utf-8').split("==")[0])

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def job_evaluation(request, encrypted_text):
	#get decrypted request id from request url^ ****'/****/content' and add '=='
	text = str(request.build_absolute_uri).split("'")[1].split("/")[2]
	text = text +"=="
	try:
		decoded_id = cipher.decrypt(text.encode('utf-8')).decode('utf-8')
	except:
		return HttpResponseRedirect(reverse('unknown_page'))
	#ЕСЛИ ЗАЯВКА УЖЕ ОБРАБОТАНА
	closed_request_note = GetFirstFilteredNote(ClosedRequest,"note_id",decoded_id)
	try:
		if closed_request_note.is_accepted is False and not (closed_request_note is None):
			open_request_note = closed_request_note.open_request
			return render(request,"it/job_evaluation.html",{"closed_note":closed_request_note,"opened_note":open_request_note})
		else:
			return HttpResponseRedirect(reverse('organisations_requests'))
	except:
		return HttpResponseRedirect(reverse('unknown_page'))

def evaluation(request):

	result = GetObject(request,"result")
	client_comment = GetObject(request,"client_comment")
	request_id = GetObject(request,"close_request_id")
	close_note = GetFirstFilteredNote(ClosedRequest,"note_id",request_id)
	close_note.client_comment = client_comment
	if result == "Принять":
		close_note.is_accepted = True
		close_note.save()
	else:
		close_note.delete()
		AddDeclinedRequest(close_note.open_request,close_note.responsible, close_note.client_comment)
	messages.success(request, "Всё отправлено, спасибо")
	return HttpResponseRedirect(reverse('organisations_requests'))


def unknown_page(request):
	return render(request,"404/404.html")

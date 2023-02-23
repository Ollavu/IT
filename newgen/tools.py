from newgen.models import *
from django.contrib.auth.models import User
import datetime

def AddToolReportNote(tool_name):
	note_id = 0
	if str(ToolsReport.objects.all().order_by('-note_id')[:1]) =="<QuerySet []>":
		note_id = 1
	else:
		for x in ToolsReport.objects.all().order_by('-note_id')[:1]:
			note_id = x.note_id
	new_note = ToolsReport()
	user = User.objects.filter(username = "tools").first()
	new_note.note_id = note_id + 1
	new_note.date = datetime.date.today()
	new_note.tool_name = Tools.objects.filter(name = tool_name).first()
	new_note.worker_id = Worker.objects.filter(user = user.id).first()
	new_note.save()

def AddTempToolTransfer(tool,worker, comments):
	note_id = 0
	if str(TempToolTransfers.objects.all().order_by('-note_id')[:1]) =="<QuerySet []>":
		note_id = 1
	else:
		for x in TempToolTransfers.objects.all().order_by('-note_id')[:1]:
			note_id = x.note_id
	note = TempToolTransfers()

	if str(TempToolTransfers.objects.filter(worker_id = worker.worker_id, tool_id = tool.tool_id)) =="<QuerySet []>":
		note.note_id = note_id + 1
		note.worker_id = worker
		note.tool_id = tool
		note.note = comments
		try:
			note.save()
			return True
		except:
			pass
	return False

def AddTool(tool_name):
	tool_id = 0
	if str(Tools.objects.all().order_by('-tool_id')[:1]) =="<QuerySet []>":
		tool_id = 1
	else:
		for x in Tools.objects.all().order_by('-tool_id')[:1]:
			tool_id = x.tool_id

	if str(Tools.objects.filter(name = tool_name)) =="<QuerySet []>":
		tool = Tools()
		tool.name = tool_name
		tool.tool_id = tool_id + 1
		try:
			tool.save()
			return True
		except Exception as e:
			pass 
	return False                      

def GetToolTransfers(worker):
	transfers = []
	for transfer in TempToolTransfers.objects.filter(worker_id = worker.worker_id):
		transfers.append(transfer)
	return transfers

def AddToolForward(tool,worker,comment):
	note_id = 0
	if str(ToolsForwarding.objects.all().order_by('-note_id')[:1]) =="<QuerySet []>":
		note_id = 1
	else:
		for x in ToolsForwarding.objects.all().order_by('-note_id')[:1]:
			note_id = x.note_id

	note = ToolsForwarding()
	note.note_id = note_id + 1
	note.date = datetime.date.today().strftime("%Y-%m-%d")
	note.tool_name = tool
	note.worker_id = worker
	if comment != "":
		note.note = comment
	else:
		note.note = "Замечаний нет"
	note.save()

def GetTool(tool_name):
	try:
		return Tools.objects.filter(name = tool_name).first()
	except Exception as e:
		print("Undefined tool")
		return None

def DeleteTool(tool_name):
	try:
		Tools.objects.filter(name = tool_name).first().delete()
	except Exception as e:
		return False
	return True

def GetWorkerTools(worker):
	tools = []
	for note in ToolsReport.objects.filter(worker_id = worker.worker_id):
		tools.append(note.tool_name)
	return tools

def RefreshToolReportNote(tool,worker):
	tool_obj = tool
	report = ToolsReport.objects.filter(tool_name = tool_obj.tool_id).first()
	report.worker_id = worker
	report.date = datetime.date.today()

	del tool_obj
	report.save()










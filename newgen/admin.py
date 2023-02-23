from django.contrib import admin

from .models import *
from .functions import GetFirstWord
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from rangefilter.filters import DateRangeFilter
from excel_response import ExcelResponse
from django.contrib.auth.models import PermissionsMixin
class MyAdminSite(AdminSite):


    def get_app_list(self, request):

        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        return app_list

class WorkerAdmin(admin.ModelAdmin):
	list_display = ('fullname','user','post','tabel')
	list_display_links = ('fullname','tabel',)
	search_fields = ('post', 'tabel')
	save_on_top = True

class ObjectAdmin(admin.ModelAdmin):
	list_display = ('name', 'is_active')
	list_display_links = ('name',)
	search_fields = ('name',  'is_active')
	save_on_top = True

class AdminTools(admin.ModelAdmin):
	list_display = ('name',)
	list_display_links = ('name',)
	search_fields = ('name',)

class AdminToolsReport(admin.ModelAdmin):
	list_display = ('date','tool_name',)
	list_display_links = ('date','tool_name',)
	search_fields = ('date', 'tool_name',)

class AdminToolsForwarding(admin.ModelAdmin):
	list_display = ('date','tool_name',)
	list_display_links = ('date','tool_name',)
	search_fields = ('date', 'tool_name')

class AdminTempToolTransfers(admin.ModelAdmin):
	list_display = ('tool_id','worker_id')
	list_display_links = ('tool_id','worker_id',)

#Выполненная работа
class AdminWork(admin.ModelAdmin ):

	list_display = ('worker_id','object_id','date','spended_time')
	list_display_links = ('worker_id','object_id','date',)
	list_filter = ('worker_id','object_id',('date', DateRangeFilter),)

	actions = ('export_requests_to_xlsx',)


	def export_requests_to_xlsx(self, request, queryset):
		#Дата с заголовками
		data = [[
		'ФИО',
		'Объект',
		'Дата работы',
		'Затраченное время',
		]]
		#ДОБАВЛЕНИЕ ЗНАЧЕНИЙ ВЫДЕЛЕННЫХ ЗАЯВОК
		for note in queryset:
			row = [
			str(note.worker_id),
			str(note.object_id),
			note.date,
			note.spended_time,
			]
			data.append(row)
		return ExcelResponse(data, output_filename = 'Test name', worksheet_name = 'Лист 1')

	export_requests_to_xlsx.short_description = 'Записать в Excel'

#ЭКСПОРТ ЗАКРЫТЫХ ЗАЯВОК В ЭКСЕЛЬ C ПОЛНОЙ ВЫБОРКОЙ ПО ДАТЕ
class AdminFulltimeObjectsToExport(admin.ModelAdmin ):

	list_display = ('worker_fullname','object_name','spended_time')
	list_display_links = ('worker_fullname','object_name',)
	list_filter = ('worker_fullname','object_name','spended_time')

	actions = ('export_fulltime_to_xlsx',)

	def export_fulltime_to_xlsx(self, request, queryset):
		#Дата с заголовками
		data = [[
		'ФИО',
		'Объект',
		'Полное время',
		]]

		#ДОБАВЛЕНИЕ ЗНАЧЕНИЙ ВЫДЕЛЕННЫХ ЗАЯВОК
		for note in queryset:
			row = [
			note.worker_fullname,
			note.object_name,
			note.spended_time,
			]
			data.append(row)

		self.message_user(request, 'Записано в Excel')
		return ExcelResponse(data, output_filename = 'Test name of fullreport', worksheet_name = 'Page 1')

	export_fulltime_to_xlsx.short_description = 'Записать выбранные выполненные работы в Excel'

class AdminShedule(admin.ModelAdmin):
	list_display = ('date','leader','display_stack','display_objects',)
	list_display_links = ('date','leader','display_stack','display_objects',)
	list_filter = ('date',)

	def display_stack(self, queryset):

		names = []

		head_of_brigade = Worker.objects.filter(fullname = str(queryset)).first().worker_id
		shedule = Shedule.objects.filter(leader = head_of_brigade).first()

		for worker in shedule.workers.all():
			names.append(GetFirstWord(str(worker.fullname)))

		return ', '.join(str(x) for x in names)

	def display_objects(self, queryset):

		objects = []

		for obj in queryset.target_objects.all():
			objects.append(obj.name)

		return ', '.join(str(x) for x in objects)

	display_stack.short_description = "Бригада"
	display_objects.short_description = "Планируемые объекты"
######################################################################
class AdminUrgencyStatus(admin.ModelAdmin):
	list_display = ('status_id','status',)
	list_display_links = ('status_id','status',)

class AdminEmail(admin.ModelAdmin):
	list_display = ('email_id','email','is_active',)
	list_display_links = ('email_id','email','is_active',)


class AdminOpenRequest(admin.ModelAdmin):
	list_display = ('organisation','date','status',)
	list_display_links  = ('organisation','date','status',)

class AdminClosedRequest(admin.ModelAdmin):
	list_display = ('open_request','responsible','date',"is_accepted")
	list_display_links  = ('open_request','responsible','date',)
	fields = ('note_id','open_request','date','mark_photo_1','mark_photo_2','mark_photo_3','comment',"is_accepted")
	readonly_fields = ('note_id','open_request','mark_photo_1','mark_photo_2','mark_photo_3')

class AdminRequestInCheck(admin.ModelAdmin):
	list_display = ('open_request','date',)
	list_display_links  = ('open_request','date',)

class AdminDeclinedRequest(admin.ModelAdmin):
	list_display = ('open_request','date','responsible',)
	list_display_links  = ('open_request','date','responsible',)

class AdminRequestStatus(admin.ModelAdmin):
	list_display = ('status_id','status',)
	list_display_links = ('status_id','status',)

class AdminEmailVerification(admin.ModelAdmin):
	list_display = ('open_request', 'expiry_date','email')
	list_display_links = ('open_request', 'expiry_date','email')

class AdminComment(admin.ModelAdmin):
	list_display = ('request','name',)
	list_display_links = ('request','name',)

admin.site = MyAdminSite()
admin.site.register(Email, AdminEmail)
admin.site.register(EmailVerification,AdminEmailVerification)
admin.site.register(RequestStatus, AdminRequestStatus)
admin.site.register(OpenRequest, AdminOpenRequest)
admin.site.register(ClosedRequest, AdminClosedRequest)
admin.site.register(RequestInCheck, AdminRequestInCheck)
admin.site.register(DeclinedRequest, AdminDeclinedRequest)
admin.site.register(UrgencyStatus,AdminUrgencyStatus)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(Shedule, AdminShedule)
admin.site.register(Object, ObjectAdmin)
admin.site.register(Work, AdminWork)
admin.site.register(TotalSpendedTimeOnObject, AdminFulltimeObjectsToExport)
admin.site.register(ToolsReport, AdminToolsReport)
admin.site.register(Tools, AdminTools)
admin.site.register(ToolsForwarding, AdminToolsForwarding)
admin.site.register(TempToolTransfers, AdminTempToolTransfers)
admin.site.register(Comment, AdminComment)


#Регистрируем стандартные
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)

from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.html import mark_safe
from newgen.functions import uploadPath

class Worker(models.Model):
	"""docstring for worker"""

	def __str__(self):
		return f"{self.fullname}"

	def number():
		no = Worker.objects.count()
		if no == None:
			return 1
		else:
			return no + 1
	
	worker_id = models.IntegerField(primary_key=True, default = number, verbose_name = "Номер сотрудника")
	user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, unique = True, verbose_name = "Пользователь")
	tabel = models.IntegerField(null=True, default = number, verbose_name = "Табельный номер")
	fullname = models.CharField(max_length=50, null=True, verbose_name = "ФИО")
	post = models.CharField(max_length=100, null=True, verbose_name = "Должность")
	coeff = models.FloatField(verbose_name = "Коэффициент")

	class Meta:

		verbose_name = "Монтажник"
		verbose_name_plural = "Монтажники"

class Tools(models.Model):
	tool_id = models.IntegerField(primary_key=True,  verbose_name = "Номер инструмента")
	name = models.CharField(max_length=150,  verbose_name='Название инструмента')

	class Meta:

		verbose_name = "Инструменты"
		verbose_name_plural = "Инструменты"

	def __str__(self):
		return f"{self.name}"

class ToolsReport(models.Model):
	def number():
		no = ToolsReport.objects.count()
		if no == None:
			return 1
		else:
			return no + 1
	note_id = models.IntegerField(primary_key=True, default = number, verbose_name = "Номер записи")
	date = models.DateField(verbose_name = "Дата постановки на учёт")
	tool_name =  models.ForeignKey(Tools,to_field='tool_id',max_length=50,on_delete=models.CASCADE, verbose_name = "Название инструмента")
	worker_id = models.ForeignKey(Worker,to_field='worker_id', on_delete=models.CASCADE,  verbose_name = "Ответственное лицо")

	class Meta:

		verbose_name = "Администрирование инструмента"
		verbose_name_plural = "Администрирование инструмента"

class ToolsForwarding(models.Model):
	def number():
		no = ToolsForwarding.objects.count()
		if no == None:
			return 1
		else:
			return no + 1
	note_id = models.IntegerField(primary_key=True, default = number, verbose_name = "Номер записи")
	date = models.DateField(verbose_name = "Дата постановки на учёт")
	tool_name =  models.ForeignKey(Tools,to_field='tool_id',max_length=50,on_delete=models.CASCADE, verbose_name = "Название инструмента")
	note = models.CharField(max_length=150,blank=True,verbose_name='Примечание')
	worker_id = models.ForeignKey(Worker,to_field='worker_id', on_delete=models.CASCADE,  verbose_name = "Ответственное лицо")

	class Meta:

		verbose_name = "История перебросов"
		verbose_name_plural = "История перебросов"

class TempToolTransfers(models.Model):
	def number():
		no = TempToolTransfers.objects.count()
		if no == None:
			return 1
		else:
			return no + 1
	note_id = models.IntegerField(primary_key=True, default = number, verbose_name = "Номер записи")
	worker_id = models.ForeignKey(Worker,to_field='worker_id', on_delete=models.CASCADE,  verbose_name = "Ответственное лицо")
	tool_id =  models.ForeignKey(Tools,to_field='tool_id',max_length=50,on_delete=models.CASCADE, verbose_name = "Название инструмента")
	note = models.CharField(max_length=150,blank=True,verbose_name='Примечание')

class Object(models.Model):

	def number():
		no = Object.objects.count()
		if no == None:
			return 1
		else:
			return no + 1

	object_id = models.IntegerField(primary_key=True, default = number, verbose_name = "Идентификационный номер")
	location = models.CharField(max_length=150, null=True, verbose_name = "Расположение")
	name = models.CharField(max_length=50, null=True, verbose_name = "Название")
	object_type = models.CharField(max_length=20, null=True, verbose_name = "Тип объекта")
	is_active = models.BooleanField(default = True, verbose_name = "Активен ли объект")

	def __str__(self):
		return f"{self.name}"

	class Meta:

		verbose_name = "Объект"
		verbose_name_plural = "Объекты"

class Work(models.Model):

	def number():
		no = Work.objects.count()
		if no == None:
			return 1
		else:
			return no + 1

	note_id = models.IntegerField(primary_key=True, default = number, verbose_name = "Номер записи")
	worker_id = models.ForeignKey(Worker,to_field='worker_id', on_delete=models.CASCADE,  verbose_name = "ФИО")
	object_id = models.ForeignKey(Object,to_field='object_id', on_delete=models.CASCADE, null=True, verbose_name = "Объект")
	date = models.DateField(verbose_name = 'Дата')
	spended_time = models.FloatField(max_length=25,verbose_name = 'Затраченное время')
	comments = models.CharField(max_length=300,blank=True,verbose_name='Комментарии')

	class Meta:

		verbose_name = "Выполненная работа"
		verbose_name_plural = "Выполненная работа"

class TotalSpendedTimeOnObject(models.Model):

	worker_fullname = models.CharField(max_length=150, verbose_name = 'ФИО')
	object_name = models.CharField(max_length=150, verbose_name = 'Объект')
	spended_time = models.FloatField(verbose_name = 'Затраченное время (часы)')

	class Meta:

		verbose_name = "Суммарное время на объекте в Excel"
		verbose_name_plural = "Суммарное время на объекте в Excel"

class Shedule(models.Model):

	def number():
		no = Shedule.objects.count()
		if no == None:
			return 1
		else:
			return no + 1

	shedule_id = models.IntegerField(primary_key=True, default = number, verbose_name = "Номер записи")
	date = models.DateField(verbose_name = 'Дата')	
	leader = models.ForeignKey(Worker,to_field='worker_id', on_delete=models.CASCADE, verbose_name = "Бригадир",related_name="leader")
	workers = models.ManyToManyField(Worker, verbose_name = "Состав бригады",blank=True, related_name="workers")
	target_objects = models.ManyToManyField(Object, verbose_name = "Планируемые объекты", related_name="target_objects")

	def __str__(self):
		return str(self.leader)

	class Meta:

		verbose_name = "Расписание объектов"
		verbose_name_plural = "Расписания объектов"
############################################################################
#REQUESTS
############################################################################


class UrgencyStatus(models.Model):

	def number():
		no = UrgencyStatus.objects.count()
		if no == None:
			return 1
		else:
			return no + 1

	status_id = models.IntegerField(primary_key=True, default = number, verbose_name = "Номер записи")
	status = models.CharField(max_length=30,  verbose_name='Статус')

	class Meta:

		verbose_name = "Статус заявки"
		verbose_name_plural = "Статусы заявок"

	def __str__(self):
		return f"{self.status}"

class Email(models.Model):

	def number():
		no = Email.objects.count()
		if no == None:
			return 1
		else:
			return no + 1

	email_id = models.IntegerField(primary_key=True, default = number, verbose_name = "Номер email")
	email = models.CharField(max_length=40,  verbose_name='Email')
	is_active = models.BooleanField(default = False, verbose_name = "Активно ли мыло")

	class Meta:

		verbose_name = "Email"
		verbose_name_plural = "Emails"

	def __str__(self):
		return f"{self.email}"

class RequestStatus(models.Model):

	def number():
		no = RequestStatus.objects.count()
		if no == None:
			return 1
		else:
			return no + 1

	status_id = models.IntegerField(primary_key=True, default = number, verbose_name = "Номер статуса")
	status = models.CharField(max_length=40,  verbose_name='Статус')

	class Meta:

		verbose_name = "Статус"
		verbose_name_plural = "Статусы"

	def __str__(self):
		return f"{self.status}"

class OpenRequest(models.Model):

	def number():
		no = OpenRequest.objects.count()
		if no == None:
			return 1
		else:
			return no + 1

	note_id = models.IntegerField(primary_key=True, default = number, verbose_name = "Номер записи")
	organisation = models.CharField(max_length=50,  verbose_name='Организация')
	phone_number = models.CharField(max_length=20,  verbose_name='Номер телефона')
	email = models.ForeignKey(Email, to_field="email_id", on_delete=models.CASCADE, verbose_name='Email')
	priority = models.ForeignKey(UrgencyStatus, to_field="status_id", on_delete=models.CASCADE, verbose_name='Статус срочности')
	problem_description = models.CharField(max_length=200,  verbose_name='Описание проблемы')
	date = models.DateField(verbose_name = 'Дата')
	status = models.ForeignKey(RequestStatus, to_field="status_id", on_delete=models.CASCADE, verbose_name='Статус заявки')

	class Meta:

		verbose_name = "Открытая заявка"
		verbose_name_plural = "Открытые заявки"

	def __str__(self):
		return f"{self.note_id}"

class ClosedRequest(models.Model):

	def number():
		no = ClosedRequest.objects.count()
		if no == None:
			return 1
		else:
			return no + 1

	note_id = models.IntegerField(primary_key=True, default = number, verbose_name = "Номер записи")
	open_request = models.ForeignKey(OpenRequest, to_field="note_id", on_delete=models.CASCADE, verbose_name='Открытая заявка')
	photo_1 = models.ImageField(upload_to=uploadPath(), blank=True, verbose_name='Фото 1',)
	photo_2 = models.ImageField(upload_to=uploadPath(), blank=True, verbose_name='Фото 2')
	photo_3 = models.ImageField(upload_to=uploadPath(), blank=True, verbose_name='Фото 3')
	rating = models.IntegerField(verbose_name = "Качество обслуживания",blank = True)
	comment = models.CharField(max_length=200,  verbose_name='Комментарий')
	date = models.DateField(verbose_name = 'Дата')
	responsible = models.CharField(max_length=100, verbose_name = "Ответственный(е)",blank = True)
	is_accepted = models.BooleanField(default=False)  

	class Meta:

		verbose_name = "Закрытая заявка"
		verbose_name_plural = "Закрытые заявки"

	def __str__(self):
		return f"{self.note_id}"

class RequestInCheck(models.Model):

	note_id = models.IntegerField(primary_key=True, verbose_name = "Номер записи")
	open_request = models.ForeignKey(OpenRequest, to_field="note_id", on_delete=models.CASCADE, verbose_name='Открытая заявка')
	date = models.DateField(verbose_name = 'Дата')
	time = models.TimeField(verbose_name = 'Время')

	class Meta:

		verbose_name = "Закрыта заявка в ожидании"
		verbose_name_plural = "Закрытые заявки в ожидании"

class DeclinedRequest(models.Model):

	note_id = models.IntegerField(primary_key=True, verbose_name = "Номер записи")
	open_request = models.ForeignKey(OpenRequest, to_field="note_id", on_delete=models.CASCADE, verbose_name='Открытая заявка')
	worker_id = models.ForeignKey(Worker,to_field='worker_id', on_delete=models.CASCADE, verbose_name = "Ответственный")
	organisation = models.CharField(max_length=50,  verbose_name='Организация')
	phone_number = models.CharField(max_length=20,  verbose_name='Номер телефона')
	email = models.ForeignKey(Email, to_field="email_id", on_delete=models.CASCADE, verbose_name='Email')
	priority = models.ForeignKey(UrgencyStatus, to_field="status_id", on_delete=models.CASCADE, verbose_name='Статус срочности')
	problem_description = models.CharField(max_length=200,  verbose_name='Описание проблемы')
	comment = models.CharField(max_length=200,  verbose_name='Комментарий')
	date = models.DateField(verbose_name = 'Дата')
	time = models.TimeField(verbose_name = 'Время')

	class Meta:

		verbose_name = "Непринятая заявка"
		verbose_name_plural = "Непринятые заявки"

	def __str__(self):
		return f"{self.note_id}"

class EmailVerification(models.Model):
	note_id = models.IntegerField(primary_key=True, verbose_name = "Номер записи")
	email = models.CharField(max_length=40,default = "test",  verbose_name='Email')
	activation_code = models.CharField(max_length=20,  verbose_name='Код активации')
	open_request = models.ForeignKey(OpenRequest, to_field="note_id", on_delete=models.CASCADE, verbose_name='Открытая заявка')
	expiry_date = models.DateField(verbose_name = 'Окончательный срок действия кода')

	class Meta:

		verbose_name = "Подтверждение Email"
		verbose_name_plural = "Подтверждения Email"

class Comment(models.Model):  
    request = models.ForeignKey(OpenRequest, to_field="note_id", 
			     on_delete=models.CASCADE)  
    name = models.CharField(max_length=80)  
    body = models.TextField()  
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)  

         
    def __str__(self):  
        return 'Comment by {} on {}'.format(self.name, self.request)

# P A E U
# P A P I U
# D A V O L E N
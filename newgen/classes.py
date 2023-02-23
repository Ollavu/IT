class EndedWorks(object):

	def __init__(self,obj,date,spended_time):
		super(EndedWorks, self).__init__()
		self.obj = obj
		self.date = date
		self.spended_time = spended_time

class ClosedRequests(object):

	def __init__(self,open_request,responsible,date):
		super(ClosedRequests, self).__init__()
		self.organisation = open_request.organisation
		self.start_date = open_request.date
		self.end_date = date
		self.responsible = responsible
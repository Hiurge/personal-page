import datetime
from flask_login import UserMixin

def time_now():
	return datetime.datetime.now(datetime.timezone.utc)+ datetime.timedelta(hours=+1)

class User(UserMixin):
	def __init__(self, user_id):
		self.user_id = user_id
	def get_id(self):
		return self.user_id
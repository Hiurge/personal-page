import psycopg2

class DataBaseManager():

	# Executes one passed command.
	def db_do(self, command):
		try:
			self.conn = psycopg2.connect('dbname={} user={}'.format(self.dbname, self.dbuser))
			self.cur = self.conn.cursor()
			self.cur.execute(command)
			self.conn.commit()
			self.conn.close()
			self.cur.close()
		except Exception as e:
			print(e)
	# Executes one passed command.
	def db_fetch(self, command):
		try:
			self.conn = psycopg2.connect('dbname={} user={}'.format(self.dbname, self.dbuser))
			self.cur = self.conn.cursor()
			self.cur.execute(command)
			result = self.cur.fetchall()
			self.conn.close()
			self.cur.close()
			return result
		except Exception as e:
			print(e)

class UserTableDB(DataBaseManager):

	table_name = 'users'
	table = [
		('id', 'serial PRIMARY KEY'),
		('name', 'text'),
		('password', 'text'),
		('info', 'text'),
		('email', 'text'),
		('created_at', 'timestamp'),
		('last_login', 'timestamp'),
		('comments', 'text')]
	column_names = [c[0] for c in table]
	
	def __init__(self, credentials):
		self.dbname = credentials['dbname']
		self.dbuser = credentials['dbuser']
		self.dbpswd = None
		self.dbport = None

	def create_user_table(self):
		columns_types = ', '.join( [ '"{}" {}'.format(tc[0], tc[1]) for tc in self.table])
		command = 'CREATE TABLE IF NOT EXISTS {} ( {} );'.format(self.table_name, columns_types)
		self.db_do( command)

	def create_user(self, user_content):
		# user_content = ['name', 'password','info', 'email','last_login', 'comments'] Values list
		columns = ', '.join(['"{}"'.format(col) for col in self.column_names[1:]])
		values  = ', '.join(["'{}'".format(v) for v in user_content])
		command = 'INSERT INTO {} ( {}) VALUES ( {});'.format(self.table_name, columns, values)
		self.db_do(command)

	def get_user(self, user_id):
		command =  '''SELECT * from {} WHERE id='{}';'''.format( self.table_name, user_id)
		user = self.db_fetch(command)
		return user
	
	def get_users(self):
		command =  '''SELECT * from {} Order By created_at DESC;'''.format( self.table_name)
		users = self.db_fetch(command)
		return users

	def update_user(self, updated_content, user_id):
		# updated_content = ['name', 'password','info', 'email','last_login', 'comments'] Values list
		updates = '''name='{}', password='{}', info='{}', email='{}', last_login='{}', comments='{}' '''.format(*updated_content)
		command	= '''UPDATE {} SET {} where id={};'''.format(self.table_name, updates, user_id)
		self.db_do(command)	

	def delete_user(self, user_id):
		command = '''DELETE FROM {} WHERE id='{}';'''.format(self.table_name, user_id)
		self.db_do( command)
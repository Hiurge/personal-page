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

	def create_table(self):
		columns_types = ', '.join( [ '"{}" {}'.format(tc[0], tc[1]) for tc in self.table])
		command = 'CREATE TABLE IF NOT EXISTS {} ( {} );'.format(self.table_name, columns_types)
		self.db_do( command)

	def insert(self, content):
		
		columns = ', '.join(['"{}"'.format(k) for k in content.keys()])
		values  = ', '.join(["'{}'".format(v) for k, v in content.items()])
		command = 'INSERT INTO {} ( {}) VALUES ( {});'.format(self.table_name, columns, values)
		self.db_do(command)

	def get_row(self, row_id):
		command =  '''SELECT * from {} WHERE id='{}';'''.format( self.table_name, row_id)
		row = self.db_fetch(command)
		return row
	
	def get_all_rows(self):
		command =  '''SELECT * from {} Order By created_at DESC;'''.format( self.table_name)
		rows = self.db_fetch(command)
		return rows

	def get_rows_where(self, request_dict):
		where = ', '.join(["{}='{}'".format(k,v) for k,v in request_dict.items()])
		command =  '''SELECT * from {} WHERE {} Order By created_at DESC;'''.format( self.table_name, where)
		rows = self.db_fetch(command)
		return rows

	def update_row(self, updated_content, row_id):
		# updated_content = {'k':'v'}
		update_string = ', '.join(["{}='{}'".format(k,v) for k,v in updated_content.items()])
		command	= '''UPDATE {} SET {} where id={};'''.format(self.table_name, update_string, row_id)
		self.db_do(command)	

	def delete_row(self, row_id):
		command = '''DELETE FROM {} WHERE id='{}';'''.format(self.table_name, row_id)
		self.db_do( command)

class UsersTable(DataBaseManager):

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

	def create_user(self, user_content):
		self.insert(user_content)
	def update_user(self, updated_content, user_id):
		self.update_row(updated_content, user_id)
	def delete_user(self, user_id):
		self.delete_row(user_id)
	def get_user(self, user_id):
		return self.get_row(user_id)
	def get_users(self):
		return self.get_all_rows()
	def get_users_where(self, request_dict):
		return self.get_rows_where(request_dict)


class PostsTable(DataBaseManager):

	table_name = 'posts'
	table = [
		('id', 'serial PRIMARY KEY'),
		('created_at', 'timestamp'),
		('creator_id', 'text'),
		('post_type', 'text'),
		('post', 'text'),]
	column_names = [c[0] for c in table]
	
	def __init__(self, credentials):
		self.dbname = credentials['dbname']
		self.dbuser = credentials['dbuser']
		self.dbpswd = None
		self.dbport = None

	def create_post(self, post_data):
		self.insert(self, post_data)
	def update_post(self, updated_post_data, post_id):
		self.update_row(updated_content, post_id)
	def delete_post(self, post_id):
		self.delete_row(post_id)
	def get_post(self, post_id):
		return self.get_row(post_id)
	def get_posts(self):
		return self.get_all_rows()
	def get_posts_where(self, request_dict):
		return self.get_rows_where(request_dict)

class CommentsTable(DataBaseManager):

	table_name = 'comments'
	table = [
		('id', 'serial PRIMARY KEY'),
		('created_at', 'timestamp'),
		('creator_id', 'text'),
		('comment_target_type', 'text'),
		('comment_target_id', 'text'),
		('comment', 'text'),]
	column_names = [c[0] for c in table]
	
	def __init__(self, credentials):
		self.dbname = credentials['dbname']
		self.dbuser = credentials['dbuser']
		self.dbpswd = None
		self.dbport = None

	def create_comment(self, comment_data):
		self.insert(self, comment_data)
	def update_comment(self, updated_comment_data, comment_id):
		self.update_row(updated_comment_data, comment_id)
	def delete_comment(self, comment_id):
		self.delete_row(comment_id)
	def get_comment(self, comment_id):
		return self.get_row(comment_id)
	def get_comments(self):
		return self.get_all_rows()
	def get_comments_where(self, request_dict):
		return self.get_rows_where(request_dict)
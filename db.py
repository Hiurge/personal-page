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

	# Executes one passed command, fg. insert, and returns last (newest), actual id.
	def db_do_return_id(self, command):
		try:
			self.conn = psycopg2.connect('dbname={} user={}'.format(self.dbname, self.dbuser))
			self.cur = self.conn.cursor()
			self.cur.execute(command)
			self.conn.commit()
			self.cur.execute('SELECT LASTVAL()')
			last_id = self.cur.fetchone()[0]
			self.conn.close()
			self.cur.close()
			return last_id
		except Exception as e:
			print(e)

	def create_table(self):
		columns_types = ', '.join( [ '"{}" {}'.format(tc[0], tc[1]) for tc in self.table])
		command = 'CREATE TABLE IF NOT EXISTS {} ( {} );'.format(self.table_name, columns_types)
		self.db_do( command)

	def insert(self, content):
		columns = ', '.join(['"{}"'.format(k) for k in content.keys()])
		values  = ', '.join(["'{}'".format(v) for v in content.values()])
		command = 'INSERT INTO {} ( {}) VALUES ( {});'.format(self.table_name, columns, values)
		self.db_do(command)

	def insert_return_id(self, content):
		columns = ', '.join(['"{}"'.format(k) for k in content.keys()])
		values  = ', '.join(["'{}'".format(v) for v in content.values()])
		command = 'INSERT INTO {} ( {}) VALUES ( {});'.format(self.table_name, columns, values)
		id_of_inserted_item = self.db_do_return_id(command)
		return id_of_inserted_item

	def get_row(self, row_id):
		command =  '''SELECT * from {} WHERE id='{}';'''.format( self.table_name, row_id)
		row = self.db_fetch(command)
		return row
	
	def get_all_rows(self):
		command =  '''SELECT * from {} Order By created_at DESC;'''.format( self.table_name)
		rows = self.db_fetch(command)
		return rows

	def get_rows_where(self, request_dict):
		where = ' and '.join(['''"{}"='{}' '''.format(k,v) for k,v in request_dict.items()])
		command =  '''SELECT * from {} WHERE {} Order By created_at DESC;'''.format( self.table_name, where)
		rows = self.db_fetch(command)
		return rows

	def get_rows_where2(self, request_dict):
		where = ' and '.join(['''"{}"='{}' '''.format(k,v) for k,v in request_dict.items()])
		command =  '''SELECT * from {} WHERE {};'''.format( self.table_name, where)
		rows = self.db_fetch(command)
		rows
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
		('role', 'text')]
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
		self.insert(post_data)
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
		('comment', 'text'),]
	column_names = [c[0] for c in table]
	
	def __init__(self, credentials):
		self.dbname = credentials['dbname']
		self.dbuser = credentials['dbuser']
		self.dbpswd = None
		self.dbport = None

	def add_comment_return_id(self, comment_data):
		# comment_data = {'created_at':'', 'comment':''}
		comment_id = self.insert_return_id(comment_data)
		return comment_id

	def get_comment(self, comment_id):
		return self.get_row(comment_id)


	def update_comment(self, updated_comment_data, comment_id):
		self.update_row(updated_comment_data, comment_id)
	def delete_comment(self, comment_id):
		self.delete_row(comment_id)
	def get_this_content_comments(self):
		return self.get_all_rows()

	def get_comments_where(self, request_dict):
		return self.get_rows_where(request_dict)


class MappingTable_UserPostComment(DataBaseManager):

	table_name = 'mapping_table'
	table = [
		('id', 'serial PRIMARY KEY'),
		('CID', 'text'), # Comment ID
		('UID', 'text'), # User ID
		('target_type', 'text'), # proj - project, PO - post, comment - other comment. 
		('PID', 'text'),] # Project / Article id
	column_names = [c[0] for c in table]
	
	def __init__(self, credentials):
		self.dbname = credentials['dbname']
		self.dbuser = credentials['dbuser']
		self.dbpswd = None
		self.dbport = None

	def add_mapping(self, mapping_data):
		self.insert(mapping_data)
		# mapping_data = {'CID':'', 'UID':'', 'target_type':'', 'PID':''}

	def get_this_content_comments_ids(self, this_content_id):
		comments_ids =  self.get_rows_where2( this_content_id)
		
		return comments_ids

import psycopg2

class PortfolioPageDB():

	def __init__(self, credentials):
		self.dbname = credentials['dbname']
		self.dbuser = credentials['dbuser']

	def create_lp_articles_table(self):
		table_name = 'lp_articles'
		columns_types = [ ('id', 'serial PRIMARY KEY'), ('title', 'text'),  ('author', 'text' ), ('publish_date', 'timestamp'), ('body', 'text'), ('category','text'), ('tags','text') ]
		columns_types = ', '.join( [ '"{}" {}'.format(tc[0], tc[1]) for tc in columns_types])
		command = 'CREATE TABLE IF NOT EXISTS {} ( {} );'.format(table_name,columns_types)
		self.db_do( command)

	def create_lp_projects_table(self):
		table_name = 'lp_projects'
		columns_types = [ ('id', 'serial PRIMARY KEY'), ('title', 'text'),  ('author', 'text' ), ('publish_date', 'timestamp'), ('body', 'text'), ('category','text'), ('tags','text') ]
		columns_types = ', '.join( [ '"{}" {}'.format(tc[0], tc[1]) for tc in columns_types])
		command = 'CREATE TABLE IF NOT EXISTS {} ( {} );'.format(table_name,columns_types)
		self.db_do( command)


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


	# Executes command.
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
			return []

	def delete_art_by_id(self, content_id):
		command = '''DELETE FROM lp_articles WHERE id='{}';'''.format(content_id)
		self.db_do(command)
	def delete_proj_by_id(self,content_id):
		command = '''DELETE FROM lp_projects WHERE id='{}';'''.format(content_id)
		self.db_do(command)


	def get_column_values(self, column_name, table_name):
		command =  '''SELECT {} from {} Order By publish_date DESC;'''.format(column_name, table_name)
		existing_articles = self.db_fetch(command)
		return existing_articles

	def get_articles(self):
		command =  '''SELECT * from lp_articles Order By publish_date DESC;'''
		existing_articles = self.db_fetch(command)
		return existing_articles

	def get_projects(self):
		command =  '''SELECT * from lp_projects Order By publish_date DESC;'''
		existing_articles = self.db_fetch(command)
		return existing_articles


	def update_content_by_id(self, table_name, updated_content, content_id):
		updates = '''title='{}', body='{}', category='{}', tags='{}' '''.format(*updated_content)
		command	= '''UPDATE {} SET {} where id={};'''
		command = command.format(table_name, updates, content_id)
		self.db_do(command)


	def db_get_top_id(self):
		try:
			command =  '''SELECT "id" from lp_articles;'''
			existing_ids = self.db_fetch(command)
			max_id = max([d[0] for d in existing_ids])
			return max_id
		except Exception as e:
			print(e)
			return 0

	def db_get_top_project_id(self):
		try:
			command =  '''SELECT "id" from lp_projects;'''
			existing_ids = self.db_fetch(command)
			max_id = max([d[0] for d in existing_ids])
			return max_id
		except Exception as e:
			print(e)
			return 0

	def get_article_titles(self):
		command = '''SELECT "title" from lp_articles;'''
		existing_titles = self.db_fetch(command)
		existing_titles = [t[0] for t in existing_titles]
		return existing_titles
		
	def get_projects_titles(self):
		command = '''SELECT "title" from lp_projects;'''
		existing_titles = self.db_fetch(command)
		existing_titles = [t[0] for t in existing_titles]
		return existing_titles

	def add_article_to_lp_articles(self, article_data_list):
		self.create_lp_articles_table()

		table_name = 'lp_articles'
		columns = ['id', 'title', 'author', 'publish_date', 'body', 'category', 'tags']
		columns = ', '.join([ '"{}"'.format(col) for col in columns]) # set_name, keyword
		values  = ', '.join(["'{}'".format(v) for v in article_data_list])
		command = 'INSERT INTO {} ( {}) VALUES ( {});'.format(table_name, columns, values)
		self.db_do(command)

	def add_project_to_lp_projects(self, project_data_list):
		self.create_lp_projects_table()

		table_name = 'lp_projects'
		columns = ['id', 'title', 'author', 'publish_date', 'body', 'category', 'tags']
		columns = ', '.join([ '"{}"'.format(col) for col in columns]) # set_name, keyword
		values  = ', '.join(["'{}'".format(v) for v in project_data_list])
		command = 'INSERT INTO {} ( {}) VALUES ( {});'.format(table_name, columns, values)
		self.db_do(command)

# credentials = {'dbname':'lp_portfolio_articles', 'dbuser':'luke'}
# PADB = PageArticlesDB(credentials)
# PADB.create_db()
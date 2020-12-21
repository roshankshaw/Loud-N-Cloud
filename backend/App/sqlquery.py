import sqlite3, ast

def getRows(db_path):
	'''
	Returns all the constituencies with current cases and other details
	'''
	conn = sqlite3.connect(db_path) #change path here
	c = conn.cursor()
	c.execute(f'''select * from main;''')
	rows=c.fetchall()
	c.execute(f'''PRAGMA table_info(main);''')
	column_names=[t[1] for t in c.fetchall()]
	c.close()
	return rows, column_names


def getCols(db_path):
	'''
	Returns all the constituencies with current cases and other details
	'''
	conn = sqlite3.connect(db_path) #change path here
	c = conn.cursor()
	c.execute(f'''PRAGMA table_info(main);''')
	column_names=[t[1] for t in c.fetchall()]
	c.close()
	return column_names

# def getCount(db_path):
#     conn = sqlite3.connect(db_path) #change path here
#     c = conn.cursor()
#     c.execute(f'''select confirmed, recovered, deceased from main;''')
#     rows=c.fetchall()
#     column_names=['confirmed', 'recovered', 'deceased']
#     c.close()
#     return rows, column_names
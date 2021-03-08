import sqlite3

db_name = "users.db"

'''
organizations:
primary_key (int autoincrement),orgname (text),admin_email (varchar 100),admin_id,staff_team_id(varchar 255),lobby_id(varchar 255)

staff:
orgid,firstname(text),lastname(text),email(varchar 100 pk),person_id(varchar 255)

students:
orgid,firstname(text),lastname(text),email(varchar 100 pk),room_id(varchar 255), person_id(varchar 255)
'''

ORGANIZATIONS_TABLE = '''
	CREATE TABLE `organizations` (
		`org_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		`org_name` TEXT,
		`admin_email` VARCHAR(100),
		`username` VARCHAR(100) UNIQUE,
		`staff_team_id` VARCHAR(255),
		`lobby_id` VARCHAR(255)
	);'''

STAFF_TABLE = '''
	CREATE TABLE `staff` (
		`org_id` INTEGER NOT NULL,
		`firstname` TEXT,
		`lastname` TEXT,
		`email` VARCHAR(100),
		`person_id` VARCHAR(255),
		 UNIQUE(org_id, email)
	);'''

STUDENTS_TABLE = '''
	CREATE TABLE `students` (
		`org_id` INTEGER NOT NULL,
		`firstname` TEXT,
		`lastname` TEXT,
		`email` VARCHAR(100),
		`person_id` VARCHAR(255),
		`room_id` VARCHAR(255),
		 UNIQUE(org_id, email)
	);'''

'''
execute select query, without exception handling

@param command: prepared query as a string
@return: list of rows that match query
'''
def execute_select(command):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	results = c.execute(command)
	l = []
	for row in results:
		l.append(row)
	conn.close()
	return l

'''
execute list of update commands, with exception handling on each one.

@param command: list of prepared queries as strings
'''
def execute_update(command):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	if(isinstance(command, list)):
		for cmd in command:
			try:
				c.execute(cmd)
			except Exception as e:
				print(str(e))
				print(cmd)
	else:
		c.execute(command)
	conn.commit()
	conn.close()

'''
creates an entry for a new organization in the table.

@param orgname: organization name
@param admin_email: email of the organization adminstrator
@param username: username for the organization account
@param team_id (optional): webex team id for the organization
@param lobby_id (optional): webex room id for the lobby account
'''
def create_organization(orgname, admin_email, username, team_id="",lobby_id=""):
	statement = "INSERT INTO organizations (org_name, admin_email, username, staff_team_id, lobby_id) VALUES ('{}', '{}', '{}', '{}', '{}')"
	statement = statement.format(orgname, admin_email, username, team_id, lobby_id)
	execute_update(statement)
	
'''
retrieves an organization by email, organization id, or username

@param email (optional): organization email
@param org_id (optional): organization id
@param username (optional): organization
@return organization row as tupe, or None
'''
def get_organization(email=None,org_id=None,username=None):
	if(email != None):
		cmd = "SELECT * from organizations WHERE admin_email = '{}'"
		cmd = cmd.format(email)
		print(cmd)
		return execute_select(cmd)
	elif(org_id != None):
		cmd = "SELECT * from organizations WHERE org_id = {}"
		cmd = cmd.format(org_id)
		return execute_select(cmd)
	elif(username != None):
		cmd = "SELECT * from organizations WHERE username = '{}'"
		cmd = cmd.format(username)
		return execute_select(cmd)

'''
returns the value associated with the key in dic, or an empty 
string if the k,v pair is not present

@param dic: dictionary
@param key: name of the key
@return: dic[key] or val
'''
def get_key(dic, key):
	val = dic.get(key)
	if(val == None):
		return ""
	return val

'''
inserts a list of staff members into the organization with the given id.

@param staff_members: list of dictionaries that represent staff members
@param org_id: id of the organization the staff members belong to
'''
def insert_staff(staff_members, org_id):
	cmds = []
	for staff in staff_members:
		email = get_key(staff, "Email")
		fname = get_key(staff, "Firstname")
		lname = get_key(staff, "Lastname")
		person_id = get_key(staff, "id")
		stmt = "INSERT INTO staff (org_id, firstname, lastname, email, person_id) VALUES ({}, '{}', '{}', '{}', '{}')"
		stmt = stmt.format(org_id, fname, lname, email, person_id)
		cmds.append(stmt)
	execute_update(cmds)
	
'''
insert a list of students into the organization with the given id

@param staff_members: list of dictionaries that represent staff members
@param org_id: id of the organization the staff members belong to
'''
def insert_students(students, org_id):
	cmds = []
	for student in students:
		email = get_key(student, "Email")
		fname = get_key(student, "Firstname")
		lname = get_key(student, "Lastname")
		person_id = get_key(student, "id")
		room_id = get_key(student, "staff_room")
		stmt = "INSERT INTO students (org_id, firstname, lastname, email, person_id, room_id) VALUES ({}, '{}', '{}', '{}', '{}', '{}')"
		stmt = stmt.format(org_id, fname, lname, email, person_id, room_id)
		cmds.append(stmt)
	execute_update(cmds)
	
def update_students(students, key, key_name):
	cmds = []
	for student in students:
		key_val = get_key(student, key)
		email = get_key(student, "Email")
		orgid = get_key(student, "org_id")
		stmt = "UPDATE students SET {} = '{}' WHERE email = '{}' AND org_id = '{}'"
		stmt = stmt.format(key_name, key_val, email, orgid)
		print(stmt)
		cmds.append(stmt)
	execute_update(cmds)
	
def update_staff(students, key, key_name):
	cmds = []
	for student in students:
		key_val = get_key(student, key)
		email = get_key(student, "Email")
		orgid = get_key(student, "org_id")
		stmt = "UPDATE staff SET {} = '{}' WHERE email = '{}' and org_id = '{}'"
		stmt = stmt.format(key_name, key_val, email, orgid)
		print(stmt)
		cmds.append(stmt)
	execute_update(cmds)

	
	
def get_student(email=None, org_id=None):
	stmt = "SELECT * FROM students WHERE email = '{}'".format(email)
	if((org_id != None) and (email != None)):
		stmt = "SELECT * FROM students WHERE email = '{}' AND org_id = {}".format(email, org_id)
	students = execute_select(stmt)
	results = []
	for student in students:
		updatedv = {}
		updatedv["org_id"] = student[0]
		updatedv["Firstname"] = student[1]
		updatedv["Lastname"] = student[2]
		updatedv["Email"] = student[3]
		updatedv["id"] = student[4]
		updatedv["staff_room"] = student[5]
		results.append(updatedv)
	if(len(results) == 0):
		return False
	if(org_id == None):
		return results
	return results[0]
def get_staff(email=None, org_id=None):
	stmt = "SELECT * FROM staff WHERE email = '{}'".format(email)
	if((org_id != None) and (email != None)):
		stmt = "SELECT * FROM staff WHERE email = '{}' AND org_id = {}".format(email, org_id)
	students = execute_select(stmt)
	results = []
	for student in students:
		updatedv = {}
		updatedv["org_id"] = student[0]
		updatedv["Firstname"] = student[1]
		updatedv["Lastname"] = student[2]
		updatedv["Email"] = student[3]
		updatedv["id"] = student[4]
		results.append(updatedv)
	if(len(results) == 0):
		return False
	if(org_id == None):
		return results
	return results[0]


def get_all_students(orgid):
	stmt = "SELECT * FROM students WHERE org_id = {}".format(orgid)
	students = execute_select(stmt)
	results = []
	for student in students:
		updatedv = {}
		updatedv["org_id"] = student[0]
		updatedv["Firstname"] = student[1]
		updatedv["Lastname"] = student[2]
		updatedv["Email"] = student[3]
		updatedv["id"] = student[4]
		updatedv["staff_room"] = student[5]
		results.append(updatedv)
	return results


def get_all_staff(orgid):
	stmt = "SELECT * FROM staff WHERE org_id = {}".format(orgid)
	results = []
	staffmems = execute_select(stmt)
	for staff in staffmems:
		updatedv = {}
		updatedv["org_id"] = staff[0]
		updatedv["Firstname"] = staff[1]
		updatedv["Lastname"] = staff[2]
		updatedv["Email"] = staff[3]
		updatedv["id"] = staff[4]
		results.append(updatedv)
	return results

def update_org_teamid(orgid, teamid):
	stmt = "UPDATE organizations SET staff_team_id = '{}' WHERE org_id = {}"
	stmt = stmt.format(teamid, orgid)
	print(stmt)
	execute_update([stmt])

'''

'''	
def create_tables():
	commands = []
	commands.append("DROP TABLE IF EXISTS organizations")
	commands.append("DROP TABLE IF EXISTS staff")
	commands.append("DROP TABLE IF EXISTS students")
	commands.append(ORGANIZATIONS_TABLE)
	commands.append(STAFF_TABLE)
	commands.append(STUDENTS_TABLE)
	execute_update(commands)
	
if __name__ == "__main__":
	create_tables()
#	create_organization("Test", "sachalma@buffalo.edu", "test1")
#	create_organization("Test", "sachalma@buffalo.edu", "test2")
#	print(get_organization(email="sachalma@buffalo.edu"))
#	print(get_organization(email="blahffefe"))
	print("main")
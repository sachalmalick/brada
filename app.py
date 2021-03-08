from flask import Flask, render_template, request,redirect,url_for,session
import utils.db_utils as db
import utils.webex_utils as wu
import utils.preproc_utils as pu
import json

app = Flask(__name__)
app.secret_key = "sachal"


@app.route('/testroute', methods=['GET'])
def testreoute():
	return render_template("staff_1.html")

@app.route('/', methods=['GET'])
def main_page():
	return render_template("index.html")

@app.route('/logout', methods=['GET'])
def logout():
	session["webex_brada_usertype"] = None
	session["webex_brada_userdata"] = None
	session["webex_brada_persondetails"] = None
	return render_template("index.html")

@app.route('/embeddemo', methods=['GET'])
def embded_route():
	access_token = session["webex_brada_accesstoken"].get("access_token")
	space_id = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vMzA1ZWVlYjAtN2M1ZS0xMWViLWJjMTMtZGYxYjJjNDhmOGNj"
	return render_template("widgetdemo.html", access_token=access_token, space_id=space_id)

@app.route('/admin', methods=['GET'])
def admin():
	try:
		email = session["webex_brada_persondetails"].get("emails")[0]
	except:
		return render_template("index.html", message="not properly loggedin")
	organizations = db.get_organization(email=email)
	print(organizations)
	return render_template("admin.html", email=email, orgs=organizations)

@app.route('/organization', methods=['GET'])
def organizations():
	org_id = request.args.get("id")
	email = session["webex_brada_persondetails"].get("emails")[0]
	if(org_id == None):
		organizations = db.get_organization(email=email)
		return render_template("admin.html", email=email, orgs=organizations, message="please specify an org id")
	org = db.get_organization(org_id=org_id)
	students = db.get_all_students(org_id)
	staff = db.get_all_staff(org_id)
	return render_template("organization.html", email=email, org=org[0], students=students, staff=staff)


@app.route('/staff', methods=['GET'])
def staff():
	if(session.get("webex_brada_persondetails") == None):
		return render_template("index.html", message="you must complete the oauth first")
	email = session.get("webex_brada_persondetails").get("emails")[0]
	if(email == None):
		return render_template("index.html", message="email not configured")
	session["webex_brada_userdata"] = db.get_staff(email=email)
	if(session["webex_brada_userdata"] == False):
		return render_template("home.html", message="unrecognized staff")
	print(session["webex_brada_userdata"])
	all_orgs = []
	for org in session["webex_brada_userdata"]:
		org_id = org["org_id"]
		organization = db.get_organization(org_id=org_id)
		print(organization)
		if(len(organization) == 0):
			print("no org")
			continue
		team_id = organization[0][4]
		orgname = organization[0][1]
		lobby = organization[0][5]
		if(team_id == ""):
			print("no team id")
			continue
		wc = wu.WebexConnector(session["webex_brada_accesstoken"].get("access_token"))
		rooms = wc.get_all_rooms(team_id)
		rooms = [(room["id"], room["title"]) for room in rooms]
		all_orgs.append((org_id,orgname,lobby,team_id, rooms))
	access_token = session["webex_brada_accesstoken"].get("access_token")
	return render_template("staff.html", data=session["webex_brada_userdata"], orgs=all_orgs, access_token=access_token)

@app.route('/student', methods=['GET'])
def student():
	if(session.get("webex_brada_persondetails") == None):
		return render_template("index.html", message="you must complete the oauth first")
	email = session.get("webex_brada_persondetails").get("emails")[0]
	if(email == None):
		return render_template("index.html", message="email not configured")
	session["webex_brada_userdata"] = db.get_student(email=email)
	if(session["webex_brada_userdata"] == False):
		return render_template("home.html", message="unrecognized student")
	all_orgs = []
	for studentorg in session["webex_brada_userdata"]:
		room_id = studentorg.get("staff_room")
		org_id = studentorg.get("org_id")
		organization = db.get_organization(org_id=studentorg["org_id"])
		if(len(organization) == 0):
			print("no org")
			continue
		lobby_id = organization[0][5]
		org_name = organization[0][1]
		all_orgs.append((org_id, org_name, room_id, lobby_id))
	print(all_orgs)
	access_token = session["webex_brada_accesstoken"].get("access_token")
	return render_template("student.html", orgs=all_orgs, access_token = access_token)

@app.route('/forms/admin/login', methods=['POST'])
def admin_login():
	email = request.form.get("email")
	password = request.form.get("password")
	rows = db.get_organization(email)
	if(len(rows) == 0):
		return render_template("login.html", message="no such email registered")
	if(rows[0]["admin_password"] != password):
		return render_template("login.html", message="invalid password")
	session["webex_brada_usertype"] = "admin"
	session["webex_brada_userdata"] = rows[0]
	return render_template("admin.html",data=rows[0])

def return_org_template(org_id, message):
	org = db.get_organization(org_id=org_id)
	email = session["webex_brada_persondetails"].get("emails")[0]
	students = db.get_all_students(org_id)
	staff = db.get_all_staff(org_id)
	return render_template("organization.html", email=email, org=org[0], students=students, staff=staff, message=message)

@app.route('/forms/upload_students', methods=['POST'])
def upload_students():
	org_id = request.form.get("org_id")
	org = db.get_organization(org_id=org_id)[0]
	if('file' not in request.files):
		return return_org_template(org_id,message="no file specifed")
	file = request.files['file']
	if(len(file.filename.strip()) == 0):
		return return_org_template(org_id,message="no file specifed")
	file.save("data/" + file.filename)
	access_token = session["webex_brada_accesstoken"].get("access_token")
	wc = wu.WebexConnector(access_token)
	students = pu.read_file("data/" + file.filename)
	for student in students:
		student["org_id"] = org_id
	staff = db.get_all_staff(org_id)
	wc.students = students
	wc.staff = staff
	wc.team_id = org[4]
	lobby_id = org[5]
	if(lobby_id == ""):
		lobby_id = None
	wc.update_student_members(wc.students)
	wc.create_student_rooms(lobby_id=lobby_id)
	db.insert_students(wc.students, org_id)
	db.update_students(wc.students, "staff_room", "room_id")
	db.update_students(wc.students, "id", "person_id")
	return return_org_template(org_id,message="successfully updated")

@app.route('/forms/upload_staff', methods=['POST'])
def upload_staff():
	org_id = request.form.get("org_id")
	org = db.get_organization(org_id=org_id)[0]
	if('file' not in request.files):
		return return_org_template(org_id,message="no file specifed")
	file = request.files['file']
	if(len(file.filename.strip()) == 0):
		return return_org_template(org_id,message="no file specifed")
	file.save("data/" + file.filename)
	access_token = session["webex_brada_accesstoken"].get("access_token")
	wc = wu.WebexConnector(access_token)
	staff = pu.read_file("data/" + file.filename)
	for member in staff:
		member["org_id"] = org_id
	students = db.get_all_students(org_id)
	wc.students = students
	wc.staff = staff
	wc.team_id = org[4]
	wc.lobby_id = org[5]
	wc.update_staff_members(wc.staff)
	wc.add_members_to_team(wc.staff, wc.team_id)
	wc.setup_new_tas(wc.staff)
	print(wc.staff)
	db.insert_staff(wc.staff, org_id)
	db.update_staff(wc.staff, "id", "person_id")
	return return_org_template(org_id,message="successfully updated")


@app.route('/forms/admin/new_organization', methods=['POST'])
def new_org_form():
	orgname = request.form.get("orgname")
	username = request.form.get("username")
	email = session["webex_brada_persondetails"].get("emails")[0]
	if((orgname == "") or (username == "")):
		return render_template("admin.html", createresponse="organization name and username cannot be blank.", orgs=db.get_organization(email=email))
	if(len(db.get_organization(username=username)) > 0):
		return render_template("admin.html", createresponse="An organization with that username already exists.", orgs=db.get_organization(email=email))
	access_token = session["webex_brada_accesstoken"].get("access_token")
	wc = wu.WebexConnector(access_token)
	team_id = wc.create_team("Teaching Staff: " + orgname)
	lobby_id = wc.create_room("Class Forum: " + orgname, team_id=team_id)
	db.create_organization(orgname, email, username, team_id=team_id, lobby_id=lobby_id)
	return render_template("admin.html", message="successful", orgs=db.get_organization(email=email))

def get_persons_name(email):
	staff = db.get_staff(email=email)
	student = db.get_student(email=email)
	if(staff != False):
		print(staff)
		return staff["Firstname"] + " " + staff["Lastname"], "Staff"
	if(student != False):
		print(student)
		return student["Firstname"] + " " + student["Lastname"], "Student"
	return email, ""

@app.route('/api/signup', methods=['POST'])
def driver_signup_api():
	return "post"

@app.route('/api/get_messages', methods=['POST'])
def get_messages():
	room_id = request.form.get("room_id")
	if(room_id == None):
		return "missing room id"
	access_token = session["webex_brada_accesstoken"].get("access_token")
	wc = wu.WebexConnector(access_token)
	messages = wc.list_room_messages(room_id)
	messages = messages.get("items")
	if(messages == None):
		return json.dumps([])
	messages.reverse()
	formated = []
	for message in messages:
		person,role = get_persons_name(message["personEmail"])
		formated.append({"from":person,"text":message["text"], "role":role})
	return json.dumps(formated)

@app.route('/api/send_message', methods=['POST'])
def send_messages():
	room_id = request.form.get("room_id")
	msg = request.form.get("msg")
	if(room_id == None):
		return "missing room id"
	if(msg == None):
		return "missing msg"
	access_token = session["webex_brada_accesstoken"].get("access_token")
	wc = wu.WebexConnector(access_token)
	result = wc.send_message(room_id, msg)
	return json.dumps(result)

@app.route('/webex/auth', methods=['GET'])
def oauth_response():
	authtoken = request.args.get("code")
	if(authtoken != None):
		session["webex_brada_authtoken"] = authtoken
		session["webex_brada_accesstoken"] = wu.get_access_token(authtoken, return_all=True)
		print(session["webex_brada_accesstoken"])
		access_token = session["webex_brada_accesstoken"].get("access_token")
		if(access_token == None):
			return render_template("index.html", message="unable to retrieve access token")
		my_details = wu.WebexConnector(access_token).get_my_details()
		session["webex_brada_persondetails"] = my_details
		print(my_details)
		return render_template("home.html")
	else:
		return "Oauth failed:  please try again. <a href = '{}'>Verify</a>".format(wu.oauth_url)
	return str(authtoken)

if __name__=="__main__":
    app.run("localhost", 8080, debug = True)
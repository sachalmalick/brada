import requests
import json



BASE_URL = ""
client_id = "C1ea993f0bfd0f31911e3d7fa9147f7af02eb31e6cb200d97a19c9ee927581b42"
client_secret = "18555a3faa0ef1f434f753b029995931804bc2fdf6cf425bbc25a91a8e6d789c"
scopes_list = ["spark:all"]
oauth_url = "https://webexapis.com/v1/authorize?client_id=C1ea993f0bfd0f31911e3d7fa9147f7af02eb31e6cb200d97a19c9ee927581b42&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fwebex%2Fauth&scope=meeting%3Arecordings_read%20spark%3Aall%20spark%3Akms%20meeting%3Aadmin_schedule_write%20meeting%3Aschedules_read%20meeting%3Aadmin_recordings_write%20meeting%3Apreferences_write%20meeting%3Arecordings_write%20meeting%3Apreferences_read%20meeting%3Aadmin_recordings_read%20meeting%3Aadmin_schedule_read%20meeting%3Aschedules_write&state=set_state_here"

def post_data(url, data, headers):
	response = requests.post(url, data=data, headers=headers)
	return response

def get_data(url, data, headers):
	response = requests.get(url, data=data, headers=headers)
	return response

def delete_data(url, data, headers):
	response = requests.delete(url, data=data, headers=headers)
	return response


def get_access_token(authcode,return_all=False):
	headers = {"Content-Type":"application/x-www-form-urlencoded"}
	data = {"grant_type":"authorization_code", "client_id" : client_id, "client_secret":client_secret, "code" : authcode, "redirect_uri" : "http://localhost:8080/webex/auth"}
	access_token_url = "https://webexapis.com/v1/access_token"
	response = post_data(access_token_url, data, headers)
	response = json.loads(response.text)
	if(return_all):
		return response
	return response.get("access_token")

class WebexConnector:
	def __init__(self, access_token, staff=[],students=[]):
		self.access_token = access_token
		self.staff = staff
		self.students = []
		self.staff_team_id = None
	def get_headers(self):
		bearer = "Bearer " + self.access_token
		return {"Authorization": bearer, "Accept" : "application/json"}
	def get_my_details(self):
		url = "https://webexapis.com/v1/people/me"
		response = get_data(url, {}, self.get_headers())
		return json.loads(response.text)
	def create_room(self,title, team_id=None):
		url = "https://webexapis.com/v1/rooms"
		data = {"title" : title}
		if(team_id != None):
			data["teamId"] = team_id
		response = post_data(url, data, self.get_headers())
		print(json.loads(response.text))
		return json.loads(response.text).get("id")
	
	def create_team(self,name):
		url = "https://webexapis.com/v1/teams"
		data = {"name" : name}
		response = post_data(url, data, self.get_headers())
		return json.loads(response.text).get("id")
		
	def list_team_members(self,team):
		url = "https://webexapis.com/v1/team/memberships?teamId={}".format(team)
		response = get_data(url, {}, self.get_headers())
		return json.loads(response.text)
	
	def get_all_rooms(self, team_id):
		print(team_id)
		url = "https://webexapis.com/v1/rooms?teamId={}".format(team_id)
		print(url)
		headers = self.get_headers()
		authorization = headers["Authorization"]
		headers = {"Content-Type":"application/json", "Authorization":authorization}
		response = get_data(url, {}, headers)
		print(json.loads(response.text))
		return json.loads(response.text).get("items")
	
	def delete_room(self, room_id):
		url = "https://webexapis.com/v1/rooms/{}".format(room_id)
		response = delete_data(url, {}, self.get_headers())
		return response
		
	def clear_all_rooms(self, team_id):
		print(team_id)
		rooms = self.get_all_rooms(team_id)
		for room in rooms:
			print("Deleting room " + room["id"])
			print(self.delete_room(room["id"]))
	
	def add_member_team(self,team_id, member_id, member_email=None, admin=True):
		url = "https://webexapis.com/v1/team/memberships"
		data = {"teamId" : team_id, "personId" : member_id, "isModerator" : admin}
		if(member_email != None):
			data["personEmail"] = member_email
		headers = self.get_headers()
		authorization = headers["Authorization"]
		headers = {"Content-Type":"application/json", "Authorization":authorization}
		data = json.dumps(data)
		response = post_data(url, data, headers)
		response = json.loads(response.text)
		if("error" in response):
			return response["error"]
		return response.get("id")
	
	def get_person(self,email):
		url = "https://webexapis.com/v1/people?email=" + str(email)
		response = get_data(url, {}, self.get_headers())
		response = json.loads(response.text)
		if("error" in response):
			return response["error"]
		return response.get("items")[0].get("id")
	
	def collect_person_ids(self, members):
		for member in members:
			try:
				member["id"] = self.get_person(member["Email"])
			except Exception as e:
				print()
				print(member)
				print(str(e))
		return members
	
	def update_staff_members(self, members):
		self.staff = self.collect_person_ids(members)
		
	def update_student_members(self, members):
		self.students = self.collect_person_ids(members)
		
	def add_person_to_room(self,room_id,person_id,admin=False,email=None):
		url = "https://webexapis.com/v1/memberships"
		data = {"roomId" : room_id, "personId" : person_id, "isModerator" : admin}
		if(email != None):
			data["personEmail"] = member_email
		headers = self.get_headers()
		authorization = headers["Authorization"]
		headers = {"Content-Type":"application/json", "Authorization":authorization}
		data = json.dumps(data)
		response = post_data(url, data, headers)
		response = json.loads(response.text)
		print(response)
		if("error" in response):
			return response["error"]
		return response.get("id")
	
	def setup_new_tas(self, tas):
		for ta in self.staff:
			for student in self.students:
				if(not "id" in student):
					print("student does not have id yet")
					continue
				if(not "staff_room" in student):
					print("student does not have room_id yet")
					continue
				print("adding to room with " + student["Lastname"])
				membership = self.add_person_to_room(student["staff_room"], ta["id"])
			print("adding to lobby")
			membership = self.add_person_to_room(self.lobby_id, ta["id"])
			
		
	def create_student_rooms(self, lobby_id=None):
		for student in self.students:
			if(not "id" in student):
				print("student does not have id yet")
				continue
			roomid = self.create_room(student["Email"], team_id=self.team_id)
			if(roomid == None):
				print("unsuccessful creating room")
				continue
			student["staff_room"] = roomid
			membership = self.add_person_to_room(roomid, student["id"])
			if(lobby_id != None):
				self.add_person_to_room(lobby_id, student["id"])
			for staff_member in self.staff:
				self.add_person_to_room(roomid, staff_member["id"])
			if(membership == None):
				print("could not add to room")
				continue
			student["staff_room_membership"] = membership
			print(membership)
	def add_members_to_team(self,members,team_id):
		for member in members:
			if(member.get("id") == None):
				print("no id", member["Email"])
				continue
			try:
				member_id = member.get("id")
				result = self.add_member_team(team_id, member_id, member_email=None, admin=True)
				if(result == None):
					print("unsuccessful adding " + str(member["Email"]))
					continue
				if("teams" in member):
					member["teams"][team_id] = result
				else:
					member["teams"] = {team_id : result}
			except Exception as e:
				print()
				print(member)
				print(str(e))
				
	def send_message(self,roomId, text = "", parentId=None,toPersonId=None,toPersonEmail=None,markdown=None,files=None,attachments=None):
		url = "https://webexapis.com/v1/messages"
		data = {"roomId" : roomId, "text" : text}
		if(toPersonId != None):
			data["toPersonId"] = toPersonId
		if(parentId != None):
			data["parentId"] = parentId
		if(toPersonEmail != None):
			data["toPersonEmail"] = toPersonEmail
		if(markdown != None):
			data["markdown"] = markdown
		if(files != None):
			data["files"] = files
		if(attachments != None):
			data["attachments"] = attachments
		headers = self.get_headers()
		authorization = headers["Authorization"]
		headers = {"Content-Type":"application/json", "Authorization":authorization}
		data = json.dumps(data)
		response = post_data(url, data, headers)
		response = json.loads(response.text)
		print(response)
		if("error" in response):
			return response["error"]
		return response.get("id")
	
	def list_room_messages(self,roomId,before=None,beforeMessage=None):
		url = "https://webexapis.com/v1/messages?roomId={}".format(roomId)
		if(before != None):
			url = url + "&before=" + before
		if(beforeMessage != None):
			url = url + "&beforeMessage=" + beforeMessage
		headers = self.get_headers()
		response = get_data(url, {}, headers)
		response = json.loads(response.text)
		return response
		
				


team_id = "Y2lzY29zcGFyazovL3VzL1RFQU0vMGY5Nzk1NjAtNTQ2My0xMWViLWFhMTctMWJlNzAwZTU2MzM2"
my_id = "Y2lzY29zcGFyazovL3VzL1BFT1BMRS8yMTQwY2UwNy0yN2RkLTRiZjItODk2OS0zNjVhNzAxYzNkNjU"

access_token = "OThjN2JhZDktMTM5ZC00MzdhLTk0MDUtYjExYTlkYmZjMWJiNDRhYTE5NTgtOWY0_PF84_d972659e-4833-445a-9202-f6c248b7a0a3"


if __name__ == "__main__":
	authcode = input("Enter an oauth code: ")
	access_token = get_access_token(authcode)["access_token"]
	print(access_token)
#	person_id = get_person(access_token, "arnabdas@buffalo.edu")
#	print(add_member_team(access_token, team_id, person_id))


		
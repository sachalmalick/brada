from utils.webex_utils import *
import utils.preproc_utils as pp
import utils.db_utils as db

oauth_code = "OTdlZmRiZjAtOTcyZi00NDhjLWIyNzktMWFlZGM3YTNjNWE2MTdlMTk5ZmYtZGM4_P0A1_325e7ef8-4dda-415a-b522-e71ff000295b"
#access_token = get_access_token(oauth_code)
access_token = "NGZiYzFjMWEtNzMzMC00YTkwLWFlMjItNWQ5YjlhYTJhYTI0MjNkYmFjNDktODQ3_P0A1_325e7ef8-4dda-415a-b522-e71ff000295b"

#students = pp.read_file("data/test.csv")
#staff = pp.read_file("data/teststaff.csv")

staff = [{'Firstname': 'Asher', 'Lastname': 'Leuker', 'Email': 'asherleuker@gmail.com', 'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jZTMyMTVlOS00ZTVkLTQ2NjktODI0MC1kYjNkM2RjNWM1OWM'}, {'Firstname': 'Sachal', 'Lastname': 'Malick', 'Email': 'malicksachal@gmail.com', 'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS9iMDljZDY4YS1kN2M5LTQ4Y2ItYTg4MS02MjU5YmM3NWE3NDU'}, {'Firstname': 'Fal', 'Lastname': 'Kooty', 'Email': 'falkooty@gmail.com', 'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mYmY5MjJjZC1lMDI1LTRkMjQtOTM0Ny1kNGIwNTMwYzVkOWU'}, {'Firstname': 'Prof', 'Lastname': 'Sachal', 'Email': 'sachaltutoring@gmail.com', 'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xYzYxOTIyYS00YmQ4LTRjMzctYTlmYi05YzVhZmJhZjU1YWM'}]

students = [{'Firstname': 'WebTest', 'Lastname': '101', 'Email': 'webextest101@yopmail.com', 'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xZjQwMGRlZi1hZTFlLTQ4YmMtYTI4Mi1iOWExN2NmYTMwMDI'}, {'Firstname': 'WebTest', 'Lastname': '102', 'Email': 'webextest102@yopmail.com', 'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS85YjBiZWY4NC0xYTkyLTQ1OGMtOWQ4NC1kMzRmMzNhYjQzMjA'}, {'Firstname': 'WebTest', 'Lastname': '103', 'Email': 'webextest103@yopmail.com', 'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wNzE5YmQ0MC00NGE2LTQ2OTEtODAyYi0yMzE1NzMxZGNiNDQ'}, {'Firstname': 'WebTest', 'Lastname': '104', 'Email': 'webextest104@yopmail.com', 'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS8zZWE4NGExNC05NjE5LTQ4MmItYWZhNy01OTgzYzUwOWRkOTA'}, {'Firstname': 'WebTest', 'Lastname': '105', 'Email': 'webextest105@yopmail.com', 'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mYWQ3Y2RkZC02NjhjLTQ5MTctYmY1NC02NzQ5YTAwZWI3ZGM'}, {'Firstname': 'WebTest', 'Lastname': '106', 'Email': 'webextest106@yopmail.com', 'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS83MTRiMjkwNi1mYzRhLTRkNjktYWE0Yi03MDFhZTUyNjVlZWU'}, {'Firstname': 'WebTest', 'Lastname': '107', 'Email': 'webextest107@yopmail.com', 'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mOTE1MzcxZC01M2Q0LTQxMzQtYjFlYi1lN2QwMGExZTZhMGE'}, {'Firstname': 'WebTest', 'Lastname': '108', 'Email': 'webextest108@yopmail.com', 'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xMmVmMGVmMy1iMzU3LTQ2YzctYjE0ZS0xNWU2MmJlZjAwYTM'}, {'Firstname': 'WebTest', 'Lastname': '109', 'Email': 'webetest109@yopmail.com', 'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNzNlNWU1OS0yNWUxLTRhZTQtODIxMy0zZWVlZDY1MmJlYTI'}, {'Firstname': 'WebTest', 'Lastname': '110', 'Email': 'webextest110@yopmail.com', 'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS9iZjExOGQwOS1iNzg1LTQ1MDEtYWI4Zi0wODBjMTdmN2JiZWQ'}, {'Firstname': 'Main', 'Lastname': 'Tester', 'Email': 'webextester99@gmail.com', 'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xNTE2NGYwZS05ZGY2LTRkMmItOWNjZC0yZWY0MjVkMzQ3M2I'}]

connector = WebexConnector(oauth_code, students=students, staff=staff)
access_token = input("Enter an access token: ")
connector.access_token = access_token
print()
print()
#connector.access_token = access_token
#connector.update_staff_members(staff)
#connector.update_student_members(students)

#staff_team = connector.create_team("The Staff")
staff_team = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1RFQU0vNzg3MjQ4ZDAtNTdhOC0xMWViLWFmZjEtOGRkMGM5MGMzYWNk"
#connector.add_members_to_team(staff, staff_team)
connector.staff_team_id = staff_team
#connector.clear_all_rooms(staff_team)
#print(connector.get_my_details())

connector.students = students
#connector.create_student_rooms()
#db.update_students(stud_b, "staff_room", "room_id")

test_room = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vY2Q3NjM0OTAtNTZmZS0xMWViLTk2ZDgtZDFjOWFjODQ4YmUx"
#res = connector.send_message(test_room, text="Hello world")
#print(res)
#print(connector.list_room_messages(test_room))
#db.insert_staff(staff, 1)
#db.insert_students(students, 1)
#print(db.get_all_staff(1))
print(connector.get_all_rooms(staff_team))

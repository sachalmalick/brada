import pandas as pd
'''
student csv schema:
Firstname, Lastname, Email
'''
def read_file(filename):
	if(".xlsx" in filename):
		df = pd.read_excel(filename)
	else:
		df = pd.read_csv(filename)
	return df.to_dict('records')

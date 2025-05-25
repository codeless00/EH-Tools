import requests
import json
import sys

def f_help():
	print("Usage: python censys_query.py -d domain_name -o output_file[Default censys.io.out.txt]")
	exit(1)
count = 1
domain_name = None
output_file = "censys.io.out.txt"
for v in sys.argv[1:]:
	if v == "-h" or v == "--help":
		f_help()
	elif v == "-d":
		domain_name = sys.argv[count + 1]
	elif v == "-o":
		output_file = sys.argv[count + 1]
	count += 1
		
if domain_name is None:
	print("Please provide domain name")
	exit(1)
	
def request_maker(domain_name, prev=None, next=None):
	print(f"Next Token in request_maker {next}")
	if next is None:
		next = ""
	url = f"https://search.censys.io/api/v2/hosts/search?per_page=100&cursor={next}&virtual_hosts=EXCLUDE&q={domain_name}"
	headers = {"Accept":"application/json", "Authorization": "Your API"}

	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		data = response.json()
		return data
		
		
	else:
		print('Request failed with status code: ', response.status_code)
		print(response.json())
		exit(1)
		
def file_writer(file_name, data):
	open_file = open(file_name, 'a')
	open_file.write(data)
	open_file.write("\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
	open_file.close()
	
	
Next_Token = None
Prev_Token = None
count = 0
def loop_(domain_name, output_file):
	while True:
		global Next_Token
		global Prev_Token
		global count
		data = request_maker(domain_name, next=Next_Token)
		#data = response.json()
		name = data['result']['hits']
		print(name)
		for v in name:
			
			actual_name = v['ip']
			file_writer(output_file, str(actual_name))
		print("Writed this Page Succesfully!")
		Next_Token = data['result']['links']['next']
		Prev_Token = data['result']['links']['prev']
		if Next_Token == "":
			Next_Token = None
		if Prev_Token == "":
			Prev_Token = None
		
		#command = input("Wants to Continue: ")
		#if command == "n" or command == "no":
		#	break
		if count != 0 and Next_Token is None:
			break
		count += 1
		print("\nCurrent Page Counting : " + str(count +1 ) + "\n")
loop_(domain_name, output_file)
	



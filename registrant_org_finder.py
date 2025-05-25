import whois
import threading
from queue import Queue
import sys

def f_help():
	print("Usage: python registrant_finder.py [options] filename(domain_list)")
	print("-t	Thread to use Default(5)")
	print("This will find the registrant organisation name of the single domain(including virtual host), ipv4 address, and ipv6 address")
	print("""
	Input:
		google.com
		www.google.com
		ftp.facebook.com
		2404:6800:4002:82e::200e
		142.250.207.206
	Output:
		None => 142.250.207.206
		Google LLC => www.google.com
		Meta Platforms, Inc. => ftp.facebook.com
		Google LLC => google.com
		Google LLC => 2404:6800:4002:82e::200e
		
	* Do not use ipv4 cidr 12.25.2.3/24 or any ipv6 cidr""")
	exit(1)


thread = 5

count = 1
for v in sys.argv[1:]:
	if v == "-h" or v == "--help":
		f_help()
	elif v == "-t":
		thread = int(sys.argv[count+1])
	count += 1
		
domain_list = sys.argv[-1]

def registrant_contact(queue):
	while True:
		domain = queue.get()
		if domain is None:	
			break
			
		#print(domain)
		dictionary = whois.whois(domain)
		print(str(dictionary["org"]) + " => " + domain)
		queue.task_done()

with open(domain_list, 'r') as f:
    domains = f.readlines()
domains = [x.strip() for x in domains if x.strip()]
domain_queue = Queue()

for domain in domains:
    domain_queue.put(domain)
    
print(f"Thread: {str(thread)}\n")    
for _ in range(thread):
	t = threading.Thread(target=registrant_contact, args=(domain_queue,))
	t.start()
	
domain_queue.join()

for _ in range(thread):
	domain_queue.put(None)

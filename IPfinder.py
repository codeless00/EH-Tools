import sys
import socket
from queue import Queue
import threading


def get_ip_address(queue):
	while True:
		
		domain = queue.get()
		result = ""
		if domain is None:	
			break
		try:
			ip_address = socket.gethostbyname(domain)
			print(ip_address)
			if ip_address:
				
				reverse_ip = socket.gethostbyaddr(ip_address)
				print(reverse_ip)
				result = "IP Address: " + str(ip_address) +  "\tReverse IP: " + str(reverse_ip[0:2]) +  "\tDomain Name: " + domain + "\n"
			
			
		except socket.gaierror:
			result = "Domain Name: " + domain + "\n"
		
			
		if result == "":
			result = "Domain Name: " + domain + "\n"	
		with file_lock:
			output_f.write(result)
		queue.task_done()
		
def usage():
	print("Usage: python IPfinder.py -t threads[Default 5] -i InputFile -o OutputFile")
	exit(1)

input_file = None
output_file = None
thread = 5
count = 0

	
for v in sys.argv:
	if v == "-h" or v == "--help":
		usage()
	elif v == "-i":
		input_file = sys.argv[count + 1]
	elif v == "-o":
		output_file = sys.argv[count + 1]
	elif v == "-t":
		thread = int(sys.argv[count + 1])
		
	count += 1
	
print("Input FIle: " + input_file)
print("Output File: " + output_file + "\n")
print("Thread : " + str(thread))

f1 = open(input_file, 'r')
domains = f1.readlines()
domains = [x.strip() for x in domains if x.strip()]
f1.close()

output_f = open(output_file, 'a')
file_lock = threading.Lock()

domain_queue = Queue()


for domain in domains:
    domain_queue.put(domain)
    # get IP address


for _ in range(thread):
	t = threading.Thread(target=get_ip_address, args=(domain_queue,))
	t.start()
	
domain_queue.join()

for _ in range(thread):
	domain_queue.put(None)

output_f.close()
print("Done...")



		

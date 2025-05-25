import socket
import requests
import dns.resolver
from queue import Queue
import threading
import sys


def f_help():
	print(f"Usage: python {sys.argv[0]} [options] filename")
	print("-if	Input File (Domain List without protocol {http or https})")
	print("-of	Output File")
	print("-t	Number of thread to initiate (Default 5)")
	print("\nThis program will give you domain IPv4 address , Status Code, Redirection Url and the actual URL Finally it stops in Redirecting")
	print("""
	Input:
		* It indicates the primary example it is made for
		
		ftp.google.com  *
		8.8.8.8
		facebook.com	*
		instagram.com	*
		hellow.text.com *
		google.co.in	*
		gmail.yahoo.com *
		8.8.4.4
		2409:408a:1486:2135::84""")
	exit(1)
	

inactive_domains = 0
total_domains = 0


thread = 5
input_file = None
output_file = None
count = 1
for v in sys.argv[1:]:
	if v == "-h" or v == "--help":
		f_help()
	
	elif v == "-t":
		thread = int(sys.argv[count + 1])
	elif v == "-if":
		input_file = sys.argv[count + 1]
	elif v == "-of":
		output_file = sys.argv[count + 1]

	count += 1

print("Input_File: " + input_file)
print("Output_File: " + output_file)
print("Thread: "+ str(thread))

		


def process_domain(queue):
	while True:
		domain = queue.get()
		if domain is None:	
			break
		# get IP address
		global total_domains
		total_domains += 1
		result_str = ""
		response_url = None
		try:
			ip = socket.gethostbyname(domain)
		except:
			ip = None
		try:
			response = requests.head("https://" + domain, allow_redirects=True, headers = {
			"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
		        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
		        })
			result_str = "RESPONSE HEADERS:\n\n"
			for k in response.headers:
				result_str = result_str + k + ": " + response.headers[k] + "\n"
				
			if response.content != "":
				result_str = result_str + "\n" + str(response.content)
			
			status_code = response.status_code
			if status_code == 301 or status_code == 302:
				redirect_url = response.headers['Location']	
				
			else:
				redirect_url = None
        
			if(response):
				response_url = response.url
			
			
		except:
			status_code = None
			redirect_url = None
			response_url = None
			
		if response_url is None and ip is not None:
			try:
				response = requests.head("http://" + domain, allow_redirects=True, headers = {
				"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
				"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
				})
				result_str = "RESPONSE HEADERS:\n\n"
				for k,v in response.headers:
					result_str = result_str + k + ": " + response.headers[v] + "\n"
				
				if response.content != "":
					result_str = result_str + "\n" + str(response.content)
		
				status_code = response.status_code
				if status_code == 301 or status_code == 302:
					redirect_url = response.headers['Location']	
					
				else:
					redirect_url = None
		
				if(response):
					response_url = response.url

			except:
				result_str = result_str + "\n" + "Exception Occured!"
				
			
		result_str = result_str + "\n" + 'Domain: ' + str(domain) + "\n" + "IP Address: " + str(ip) + "\n" + "HTTP Status Code: " + str(status_code) + "\n" + "Redirection URL: " + str(redirect_url) + "\n" + "URL: " + str(response_url) + "\n\n" + "---------------------------------------------------------------------------------------------------------------------------------\n"
		
		if ip is None:
			global inactive_domains
			inactive_domains += 1
		
		with file_lock:
			output_f.write(result_str)
		queue.task_done()

		
output_f = open(output_file, 'a')
file_lock = threading.Lock()




with open(input_file) as f:
    domains = f.readlines()
    
# strip whitespace and remove empty lines
domains = [x.strip() for x in domains if x.strip()]

domain_queue = Queue()


for domain in domains:
    domain_queue.put(domain)
    # get IP address


for _ in range(thread):
	t = threading.Thread(target=process_domain, args=(domain_queue,))
	t.start()
	
domain_queue.join()

for _ in range(thread):
	domain_queue.put(None)

output_f.close()
print("Total_Domains: " + str(total_domains))
print("Inactive_Domains: " + str(inactive_domains))
print("Done...")

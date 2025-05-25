import sys
import dns.resolver
from queue import Queue
import threading
import tldextract

def f_help():
	print("Usage: python NSfinder.py [options] domain_file")
	print("-t   : Nuber of Thread to use (Default 5)")
	print("-of  : Output File")
	print("""
	This program will take domain name and find all the assocaited name servers name with that domain name:
		Inuput:
			google.com
			facebook.com
			youtube.com
		
		Output:
		
			Root Domain: youtube.com
			youtube.com name server ns4.google.com.
			youtube.com name server ns2.google.com.
			youtube.com name server ns3.google.com.
			youtube.com name server ns1.google.com.

			Root Domain: facebook.com
			facebook.com name server c.ns.facebook.com.
			facebook.com name server b.ns.facebook.com.
			facebook.com name server a.ns.facebook.com.
			facebook.com name server d.ns.facebook.com.

			Root Domain: google.com
			google.com name server ns3.google.com.
			google.com name server ns2.google.com.
			google.com name server ns4.google.com.
			google.com name server ns1.google.com.

			
	* Note Default Timeout for NS is 20 second. Modify source code to match your needs.""")
	exit(1)
	
count = 1
thread = 5
in_f = sys.argv[-1]
out_f = in_f + "_NSfinder.out.txt"

for v in sys.argv[1:]:
	if v == "-h" or v == "--help":
		f_help()
	elif v == "-t":
		thread = int(sys.argv[count + 1])
	elif v == "-of":
		out_f = sys.argv[count + 1]
	count += 1
		


def find_ns(queue):
	while True:
		domain = queue.get()
		if domain is None:	
			break
		
		tld_extract = tldextract.extract(domain)
		root_domain = tld_extract.domain + "." + tld_extract.suffix 
		
		rst = ""

		try:	
			timeout = 20
			resolo = dns.resolver.Resolver()
			dns.timeout = timeout
			answer = resolo.resolve(root_domain, 'NS')
			name_servers = [str(ns) for ns in answer]
			for server in name_servers:
				rst = rst + domain + " name server " + server + "\n"
		except dns.resolver.NXDOMAIN:
			rst = f"Domain {domain} does not exit.\n"
		except dns.resolver.NoAnswer:
			rst = f"No Name Server found for Domain {domain}\n"
		except dns.resolver.Timeout:
			rst = f"Timeout occured while resolving Domain {domain}\n"
		except Exception as e:
			rst = f"An error occured while resolveing Domain {domain}: {e}\n"
		if(rst != ""):
			
			rst = f"Root Domain: {root_domain}\n" + rst + "\n"
			
		with file_lock:
			output_f.write(rst)
			
		queue.task_done()


print(f"Input File: {in_f}")
print("Thread: " + str(thread))

output_f = open(out_f, 'a')
file_lock = threading.Lock()

with open(in_f) as f:
    domains = f.readlines()
    
# strip whitespace and remove empty lines
domains = [x.strip() for x in domains if x.strip()]

domain_queue = Queue()


for domain in domains:
    domain_queue.put(domain)
    # get IP address


for _ in range(thread):
	t = threading.Thread(target=find_ns, args=(domain_queue,))
	t.start()
	
domain_queue.join()

for _ in range(thread):
	domain_queue.put(None)
	

output_f.close()
print(f"Saving it to {out_f}")
print("Done...")
	

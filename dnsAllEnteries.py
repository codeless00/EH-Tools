import sys
import dns.resolver
from queue import Queue
import threading


def usage():
	print("Python dnsAllEntries.py -t thread[Default 5 TR:89] doaminname")
	print("""
	Enter a domain name it will try to find all the records typically a dns server can serve. There are currently 89 records
	defined in this source code. So max thread should be 89.""")
	exit(1)

thread = 5
count = 0
for v in sys.argv:
	if v == "-h" or v == "--help":
		usage()
	elif v == "-t":
		thread = int(sys.argv[count +1 ])
	count += 1
		
domain_name = sys.argv[-1]

RR = ['A', 'NS', 'MD', 'MF', 'CNAME', 'SOA', 'MB', 'MG', 'MR', 'NULL', 'WKS', 'PTR', 'HINFO', 'MINFO', 'MX', 'TXT', 'RP', 'AFSDB', 'X25', 'ISDN', 'RT', 'NSAP', 'NSAP-PTR', 'SIG', 'KEY', 'PX', 'GPOS', 'AAAA', 'LOC', 'NXT', 'EID', 'NIMLOC', 'SRV', 'ATMA', 'NAPTR', 'KX', 'CERT', 'A6', 'DNAME', 'SINK', 'OPT', 'APL', 'DS', 'SSHFP', 'IPSECKEY', 'RRSIG', 'NSEC', 'DNSKEY', 'DHCID', 'NSEC3', 'NSEC3PARAM', 'TLSA', 'SMIMEA', 'HIP', 'NINFO', 'RKEY', 'TALINK', 'CDS', 'CDNSKEY', 'OPENPGPKEY', 'CSYNC', 'ZONEMD', 'SVCB', 'HTTPS', 'SPF', 'UINFO', 'UID', 'GID', 'UNSPEC', 'NID', 'L32', 'L64', 'LP', 'EUI48', 'EUI64', 'TKEY', 'TSIG', 'IXFR', 'AXFR', 'MAILB', 'MAILA', '*', 'URI', 'CAA', 'AVC', 'DOA', 'AMTRELAY', 'TA', 'DLV']


Found_Result = []
notfound = []


def dns_request(queue):
	global Found_Result
	global notfound
	global domain_name
	while True:
		v = queue.get()
		if v is None:	
			break
		string = None
		try:
			answer = dns.resolver.resolve(domain_name, v)
			name_servers = [str(ns) for ns in answer]
			string = str(name_servers)
		except:
			notfound.append(f"Cann't find result for {v}")
		
		if string is not None:
			string = f"Result for {v}" + string
			Found_Result.append(string)
		
		queue.task_done()



record = Queue()

for r in RR:
    record.put(r)

print("Thread: " + str(thread))
for _ in range(thread):
	t = threading.Thread(target=dns_request, args=(record,))
	t.start()
	
record.join()

for _ in range(thread):
	record.put(None)

for v in Found_Result:
	print(v)
		
		


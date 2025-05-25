import sys
import tldextract

def f_help():
	print("Usage: python root_domain.py Domain_Filename")
	print("This program will find the root domain of the given virtual domain or host. For Example ftp.google.com\nIt will find google.com easily")
	print("Note: Any Type of Input is Allowed Like:\n\nwww.google.com\nftp.sudo.facebook.com\nhttps://www.ftp.ssh.instagram.com\nheelo.ftp.google.co.in\nhttp://192.36.25.35/gmail.com\n")
	print("Answer\n")
	print("""google.com
facebook.com
instagram.com
google.co.in
192.36.25.35.

* Direct ipv6 Address is not supported Like http://[1:B:5::78]""")
	exit()
	
for v in sys.argv:
	if v == "-h" or v == "--help":
		f_help()
in_file = sys.argv[-1]

with open(in_file, 'r') as f:
	cont = f.readlines()
	cont = [x.strip() for x in cont if x.strip()]
	for domain in cont:
		tld_extract = tldextract.extract(domain)
		root_domain = tld_extract.domain + "." + tld_extract.suffix
		print(root_domain)
	

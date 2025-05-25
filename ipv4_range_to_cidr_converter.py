import sys
import ipaddress

def usage():
	print(f"Usage: Python {sys.argv[0]} inputFile(ipRange  192.0.0.0 - 192.255.255.255)")
	print("-s	For singal ipv4 range")
	print('-ld	Flag should be enabled if ipv4 range is in long decimal like "3221225472 - 3238002687"')
	print("""
			Enter input file containg of ipv4 address starting and ending like in this format "192.0.0.0 - 192.255.255.255" one range per Line
			It will try to resolve the these range into ipv4 CIDR notation like this "192.0.0.0/8" """)
			
	exit(1)

direct_ipv4 = None
long_decimal = False
count = 0
for v in sys.argv:
	if v == "-h" or v == "--help":
		usage()
	if v == "-s":
		direct_ipv4 = sys.argv[count + 1]
	if v == "-ld":
		long_decimal = True
	count += 1




def range_to_cidr(ip_range):
	if long_decimal:
		start,end = map(int, ip_range.split(' - '))
	else:
		ss, end = ip_range.split(' - ')
		start = int(ipaddress.ip_address(ss))

		end = int(ipaddress.ip_address(end))
	start_ip = '.'.join(str((start >> (24 - i*8)) & 255) for i in range(4))
	mask = 32 - (end-start).bit_length()
	cidr_notation = f"{start_ip}/{mask}"
	return cidr_notation
	
if direct_ipv4:
	rt= range_to_cidr(direct_ipv4)
	print(rt)
	exit(1)
	
in_f = sys.argv[-1]


tmp = []
with open(in_f) as f:
	for line in f:
		tmp.append(line.strip())

	
for range_ip in tmp:

	first = ""
	second = ""
	flag = True
	for a in range_ip:
		if a == "-":
			flag = False
			continue
		if a != " " and flag:
			first = first + a
			
		elif a != " " and not flag:
			second = second + a
			
	first_ip = int(ipaddress.IPv4Address(first))
	second_ip = int(ipaddress.IPv4Address(second))
	rst = range_to_cidr(str(first_ip) + "-" + str(second_ip))
	print(rst)

	

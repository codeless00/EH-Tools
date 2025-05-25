import ipaddress
import sys

def usage():
	print(f"Python {sys.argv[0]} -f1 file1 -f2 file2")
	print("""
		This Program can be helpful in finding the difference between two files contating IPv4 CIDR, one per line.
		It will try to Find the difference between the number of host which is unique or common to these files.
		It will finally give result in IPv4 CIDR format.
		Give a try man!""")
	exit(1)


file1 = None 
file2 = None

cidr_list1 = []
cidr_list2 = []

count = 0
for v in sys.argv:
	if v == "-h" or v == "--help":
		usage()
	elif v == "-f1":
		file1 = sys.argv[count + 1]
	elif v == "-f2":
		file2 = sys.argv[count + 1]
	count += 1
# Example usage:
if ((file1 is None) or (file2 is None)):
	print("Please Enter Input file!")
	exit(1)
	
with open(file1, 'r') as file:
	for line in file:
		cidr_list1.append(line.strip())
	
with open(file2, 'r') as file:
	for line in file:
		cidr_list2.append(line.strip())
	
	

def compare_cidr(cidr1, cidr2):
	net1 = ipaddress.ip_network(cidr1)
	net2 = ipaddress.ip_network(cidr2)
	
	# if net1.subnet_of(net2):
	# 	return f"{cidr1} is included in {cidr2}"
	# elif net2.subnet_of(net1):
	# 	return f"{cidr2} is included in {cidr1}"
	# elif net1.overlaps(net2):
	# 	common_range = net1.overlap(net2)
	# 	specific_range1 = net1.address_exclude(common_range)
	# 	specific_range2 = net2.address_exclude(common_range)
	# 	return f"common IP range:  {common_range},  Specific to {cidr1} : {specific_range1}, Specific to {cidr2} : {specific_range2}"
		
	# else:
	# 	return "CIDR ranges do not overlap"
		
		
#cidr_list1 = ['104.16.3.0/26','8.8.8.0/24','104.13.0.0/17','64.0.0.0/3', '104.16.0.0/21', '8.8.0.0/16', '77.16.0.0/14', '104.13.0.0/20']
#cidr_list2 = ['104.18.0.0/19', '64.0.0.0/2', '64.2.0.0/15', '77.0.0.0/8', '64.0.0.0/7', '8.2.0.0/15', '9.9.7.0/25', '104.18.0.0/17']

cidr_range_list_file1 = []
cidr_range_list_file2 = []


def range_finder(cidr_list, cidr_range_list_file1, default=True):
	#print("???????????????///")
	#print(cidr_range_list_file1)
	for v in cidr_list:
		if default:
			net1 = ipaddress.ip_network(v)
			starting_range = int(net1.network_address)
			ending_range = int(net1.num_addresses) + starting_range - 1
			total_range = str(starting_range) + "-" + str(ending_range)
		else:
			total_range = v
		
		#print(total_range)
		
		#cidr_range_list_file1.append(total_range)
		range_maker(total_range, cidr_range_list_file1)
		
		

def range_maker(final_range, cidr_range_file):
	if len(cidr_range_file) == 0:
		cidr_range_file.append(final_range)
	else:
		count = 0
		for cidr in cidr_range_file:
			if cidr:
				#print("count: " + str(count))
				#print("CIDR: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
				#print(cidr)
				c_s, c_e = cidr.split("-")
				f_s, f_e = final_range.split("-")
				cidr_s = int(c_s)
				cidr_e = int(c_e)
				current_s = int(f_s)
				current_e = int(f_e)
				
				if current_e >= cidr_s and current_e <= cidr_e and current_s < cidr_s:
					c_g = str(cidr_s) + "-" + str(current_e)
					r_g = str(current_s) + "-" + str(cidr_s - 1)
					final_range = r_g
					#print("1")
					
				elif current_s <= cidr_e and current_s >= cidr_s and current_e > cidr_e:
					c_g = str(current_s) + "-" + str(cidr_e)
					r_g = str(cidr_e + 1) + "-" + str(current_e)
					final_range = r_g
					#print("2")
					
				elif current_s >= cidr_s and current_e <= cidr_e:
					c_g = str(current_s) + "-" + str(cidr_e)
					r_g = None
					#print("3")
					break
				
				elif current_s < cidr_s and current_e > cidr_e:
					del cidr_range_file[count]
					cidr_range_file.insert(count,None)
					r_g = str(current_s) + "-" + str(current_e)
					final_range = r_g
					#print("4")
					#print("r_g")
					#print(r_g)
					#print(cidr_range_file)
					
				else:
					r_g = str(current_s) + "-" + str(current_e)
					final_range = r_g
					#print("5")
			count += 1
			
		
		if r_g is not None:
			cidr_range_file.append(r_g)
	#print("Cidr_range_File")
	#print(cidr_range_file)
			
	
def range_to_cidr(ip_range):
	start,end = map(int, ip_range.split('-'))
	start_ip = '.'.join(str((start >> (24 - i*8)) & 255) for i in range(4))
	mask = 32 - (end-start).bit_length()
	cidr_notation = f"{start_ip}/{mask}"
	return cidr_notation	
		
def compare_cidr(cidr_first, cidr_second):
	#print("\nCall to compare_cidr\n")
	#print("cidr_first")
	#print(cidr_first)
	#print("cidr_second")
	#print(cidr_second)
	specific = []
	common = []
	rst = []
	
	for cidr in cidr_first:
		#print("length of cidr " + str(len(cidr_first)))
		#print("CIDR NO.")
		#print(cidr_first)
		#print(cidr)
		#print('\n')
		
		for cidr_2 in cidr_second:
			cidr_starting, cidr_ending = cidr.split("-")
			current_s = int(cidr_starting)
			current_e = int(cidr_ending)
			
			cidr_2_s, cidr_2_e = cidr_2.split("-")
			cidr_st = int(cidr_2_s)
			cidr_en = int(cidr_2_e)
			
			if current_e >= cidr_st and current_e <= cidr_en and current_s < cidr_st:
				c_g = str(cidr_st) + "-" + str(current_e)
				r_g = str(current_s) + "-" + str(cidr_st - 1)
				cidr = r_g
				common.append(c_g)
				#print("1")
				
			elif current_s <= cidr_en and current_s >= cidr_st and current_e > cidr_en:
				c_g = str(current_s) + "-" + str(cidr_en)
				r_g = str(cidr_en + 1) + "-" + str(current_e)
				cidr = r_g
				common.append(c_g)
				#print("2")
				
			elif current_s >= cidr_st and current_e <= cidr_en:
				c_g = str(current_s) + "-" + str(current_e)
				r_g = None
				common.append(c_g)
				#print("3")
				break
				
			elif current_s < cidr_st and current_e > cidr_en:
				c_g = str(cidr_st) + "-" + str(cidr_en)
				r_g1 = str(current_s) + "-" + str(cidr_st - 1)
				r_g2  = str(cidr_st + 1) + "-" + str(current_e)
				common.append(c_g)
				cidr_first.append(r_g2)
				cidr = r_g1
				#print("4")
				#print('c-g')
				#print(c_g)
				#print(r_g1)
				#print(r_g2)
				
			else:
				r_g = str(current_s) + "-" + str(current_e)
				cidr = r_g
				#print("5")
				
		if r_g:
			specific.append(r_g)
			
	rst.append(specific)
	rst.append(common)
	return rst

		
cidr1 = "8.35.192.240/27"
cidr2 = "8.35.195.192/27"


range_finder(cidr_list1, cidr_range_list_file1)
#print("----------------------------------------------------------")
range_finder(cidr_list2, cidr_range_list_file2)

while None in cidr_range_list_file1:
	cidr_range_list_file1.remove(None)
	
while None in cidr_range_list_file2:
	cidr_range_list_file2.remove(None)
	
#print("===============================	Removing None")
#print(cidr_range_list_file1)
#print(cidr_range_list_file2)
#print("===============================")

cfst=[]
for v in cidr_range_list_file1:
	cfst.append(v)

#print(cfst)
file1_rst = compare_cidr(cidr_range_list_file1, cidr_range_list_file2)
file2_rst = compare_cidr(cidr_range_list_file2, cfst)
#print("C_F")
#print(cfst)

		


#print("---------------")
common = []
both_file = []
for v in file1_rst[1]:
	common.append(v)
for v in file2_rst[1]:
	common.append(v)
	
file1_specific = []
file2_specific = []

range_finder(common, both_file, default=False)
range_finder(file1_rst[0], file1_specific, default=False)
range_finder(file2_rst[0], file2_specific, default= False)

print("\nRESULT:\n")
print("===================================================================================================================================================================================================")
print(f"Specific to File 1 : '{file1}'\n")
#print(file1_specific)
for v in file1_specific:
	if v:
		print(range_to_cidr(v))
print("===================================================================================================================================================================================================")
print(f"\nSpecific to File 2 : '{file2}'\n")
#print(file2_specific)
for v in file2_specific:
	if v:
		print(range_to_cidr(v))
print("===================================================================================================================================================================================================")
print("\nCommon in Both File\n")
#print(both_file)
for v in both_file:
	if v:
		print(range_to_cidr(v))



print("\n\nDone..")

import sys
import requests
import os
import hashlib
import re
import ipaddress
from queue import Queue
import threading

def usage():
	print(f"Usage:    python {sys.argv[0]} [options] (IPv4 | Filename)\n")
	print("\t-update\t\tUpdate database to the latest IANA database")
	print("\t-ip\t\tCheck for single CIDR or IPv4")
	print("\t-if\t\tInput File name containing either CIDR or IPv4")
	print("\t-t\t\tNumber of Threads to Use Default[15]")
	print("""
		This program will determin which ipv4 or CIDR is ressemble to which RIR BLOCK:
		 APAC
		 APNIC
		 AFRINIC
		 RIPE
		 LACNIC
		IT will also find the assocaited country where this block is assigned.
		
		* Note you can also update the database to get accurate details if the database is too old using -update options. :)
		""")
			
	exit(1)

update = None
ip_check = None
input_file = None
thread = 15

count = 0

for v in sys.argv:
	if v == "-h" or v == "--help":
		usage()
	elif v == "-update":
		update = True
	elif v == "-ip":
		ip_check = sys.argv[count + 1]
	elif v == "-if":
		input_file = sys.argv[count + 1]
	elif v == "-t":
		thread = int(sys.argv[count + 1])
		
	count += 1

def update_data(update_dir="DB"):
	print("Logs:	Updating whois database to the latest version")
	apnic = os.path.join(update_dir,"delegated-apnic-latest")
	print("\nLogs:\tUpdating Apnic Region:")
	if not os.path.exists(apnic):
		apnic_req = requests.get("http://ftp.apnic.net/stats/apnic/delegated-apnic-latest")
		apnic_body = apnic_req.text
		with open(apnic, 'w') as f:
			f.write(apnic_body)
	else:
		old_md5 = calculate_md5(apnic)
		apnic_md5 = requests.get("http://ftp.apnic.net/stats/apnic/delegated-apnic-latest.md5")
		web_md5_list = apnic_md5.text.split(" ")
		current_md5 = web_md5_list[-1].replace("\n","")
		
		if current_md5 == old_md5:
			print("Logs:\tApnic db is already upto the Latest Version.")
		elif current_md5 != old_md5:
			bak_apnic = open(apnic+".bak", "w")
			act_apnic = open(apnic, "r")
			act_content = act_apnic.read()
			act_apnic.close()
			act_apnic = open(apnic, "w")
			bak_apnic.write(act_content)
			bak_apnic.close()
			a_req = requests.get("http://ftp.apnic.net/stats/apnic/delegated-apnic-latest")
			apnic_body = a_req.text
			act_apnic.write(apnic_body)
			act_apnic.close()
			print("Logs:\tApnic db has been updated to the Latest Version.")
			
		
		print(f"\tFile Actual Md5: {old_md5}")
		print(f"\tFile Md5 on web: {current_md5}")
		
		print("")
		
	arin = os.path.join(update_dir,"delegated-arin-extended-latest")
	print("\nLogs:\tUpdating Arin Region:")
	if not os.path.exists(arin):
		arin_req = requests.get("http://ftp.apnic.net/stats/arin/delegated-arin-extended-latest")
		arin_body = arin_req.text
		with open(arin, 'w') as f:
			f.write(arin_body)
	else:
		old_md5 = calculate_md5(arin)
		arin_md5 = requests.get("http://ftp.apnic.net/stats/arin/delegated-arin-extended-latest.md5")
		web_md5_list = arin_md5.text.split(" ")
		current_md5 = web_md5_list[0].replace("\n","")
		
		if current_md5 == old_md5:
			print("Logs:\tArin db is already upto the Latest Version.")
		elif current_md5 != old_md5:
			bak_arin = open(arin+".bak", "w")
			act_arin = open(arin, "r")
			act_content = act_arin.read()
			act_arin.close()
			act_arin = open(arin, "w")
			bak_arin.write(act_content)
			bak_arin.close()
			a_req = requests.get("http://ftp.apnic.net/stats/arin/delegated-arin-extended-latest")
			arin_body = a_req.text
			print(arin_body)
			act_arin.write(arin_body)
			act_arin.close()
			print("Logs:\tArin db has been updated to the Latest Version.")
			
		
		print(f"\tFile Actual Md5: {old_md5}")
		print(f"\tFile Md5 on web: {current_md5}")
		
		print("")
		
	afrinic = os.path.join(update_dir,"delegated-afrinic-latest")
	print("\nLogs:\tUpdating Afrinic Region:")
	if not os.path.exists(afrinic):
		afrinic_req = requests.get("http://ftp.apnic.net/stats/afrinic/delegated-afrinic-latest")
		afrinic_body = afrinic_req.text
		with open(afrinic, 'w') as f:
			f.write(afrinic_body)
	else:
		old_md5 = calculate_md5(afrinic)
		afrinic_md5 = requests.get("http://ftp.apnic.net/stats/afrinic/delegated-afrinic-latest.md5")
		web_md5_list = afrinic_md5.text.split(" ")
		current_md5 = web_md5_list[-1].replace("\n","")
		
		if current_md5 == old_md5:
			print("Logs:\tAfrinic db is already upto the Latest Version.")
		elif current_md5 != old_md5:
			bak_afrinic = open(afrinic+".bak", "w")
			act_afrinic = open(afrinic, "r")
			act_content = act_afrinic.read()
			act_afrinic.close()
			act_afrinic = open(afrinic, "w")
			bak_afrinic.write(act_content)
			bak_afrinic.close()
			a_req = requests.get("http://ftp.apnic.net/stats/afrinic/delegated-afrinic-latest")
			afrinic_body = a_req.text
			act_afrinic.write(afrinic_body)
			act_afrinic.close()
			print("Logs:\tAfrinic db has been updated to the Latest Version.")
			
		
		print(f"\tFile Actual Md5: {old_md5}")
		print(f"\tFile Md5 on web: {current_md5}")
		print("")
		
	lacnic = os.path.join(update_dir,"delegated-lacnic-latest")
	print("\nLogs:\tUpdating Lacnic Region:")
	if not os.path.exists(lacnic):
		lacnic_req = requests.get("http://ftp.apnic.net/stats/lacnic/delegated-lacnic-latest")
		lacnic_body = lacnic_req.text
		with open(lacnic, 'w') as f:
			f.write(lacnic_body)
	else:
		old_md5 = calculate_md5(lacnic)
		lacnic_md5 = requests.get("http://ftp.apnic.net/stats/lacnic/delegated-lacnic-latest.md5")
		web_md5_list = lacnic_md5.text.split(" ")
		current_md5 = web_md5_list[-1].replace("\n","")
		
		if current_md5 == old_md5:
			print("Logs:\tLacnic db is already upto the Latest Version.")
		elif current_md5 != old_md5:
			bak_lacnic = open(lacnic+".bak", "w")
			act_lacnic = open(lacnic, "r")
			act_content = act_lacnic.read()
			act_lacnic.close()
			act_lacnic = open(lacnic, "w")
			bak_lacnic.write(act_content)
			bak_lacnic.close()
			a_req = requests.get("http://ftp.apnic.net/stats/lacnic/delegated-lacnic-latest")
			lacnic_body = a_req.text
			act_lacnic.write(lacnic_body)
			act_lacnic.close()
			print("Logs:\tLacnic db has been updated to the Latest Version.")
			
		
		print(f"\tFile Actual Md5: {old_md5}")
		print(f"\tFile Md5 on web: {current_md5}")
		print("")
		
	ripencc = os.path.join(update_dir,"delegated-ripencc-latest")
	print("\nLogs:\tUpdating Ripencc Region:")
	if not os.path.exists(ripencc):
		ripencc_req = requests.get("http://ftp.apnic.net/stats/ripe-ncc/delegated-ripencc-latest")
		ripencc_body = ripencc_req.text
		with open(ripencc, 'w') as f:
			f.write(ripencc_body)
	else:
		old_md5 = calculate_md5(ripencc)
		ripencc_md5 = requests.get("http://ftp.apnic.net/stats/ripe-ncc/delegated-ripencc-latest.md5")
		web_md5_list = ripencc_md5.text.split(" ")
		current_md5 = web_md5_list[-1].replace("\n","")
		
		if current_md5 == old_md5:
			print("Logs:\tRipencc db is already upto the Latest Version.")
		elif current_md5 != old_md5:
			bak_ripencc = open(ripencc+".bak", "w")
			act_ripencc = open(ripencc, "r")
			act_content = act_ripencc.read()
			act_ripencc.close()
			act_ripencc = open(ripencc, "w")
			bak_ripencc.write(act_content)
			bak_ripencc.close()
			a_req = requests.get("http://ftp.apnic.net/stats/ripe-ncc/delegated-ripencc-latest")
			ripencc_body = a_req.text
			act_ripencc.write(ripencc_body)
			act_ripencc.close()
			print("Logs:\tRipencc db has been updated to the Latest Version.")
			
		
		print(f"\tFile Actual Md5: {old_md5}")
		print(f"\tFile Md5 on web: {current_md5}")
	
	print("\nFinshed Updating Regions!")
	exit(1)
	
def calculate_md5(file_path):
	md5_hash = hashlib.md5()
	with open(file_path, 'rb') as f:
		while True:
			chunk = f.read(4096)
			if not chunk:
				break
			md5_hash.update(chunk)
		
	return md5_hash.hexdigest()



if update is None and ip_check is None and input_file is None:
	usage()
	
if update:
	update_data()
	
	
apnic = {'AF': 'AFGHANISTAN', 'AS': 'AMERICAN SAMOA', 'AU': 'AUSTRALIA', 'BD': 'BANGLADESH', 'BT': 'BHUTAN', 'IO': 'BRITISH INDIAN OCEAN TERRITORY', 'BN': 'BRUNEI DARUSSALAM', 'KH': 'CAMBODIA', 'CN': 'CHINA', 'CX': 'CHRISTMAS ISLAND', 'CC': 'COCOS (KEELING) ISLANDS', 'CK': 'COOK ISLANDS', 'FJ': 'FIJI', 'PF': 'FRENCH POLYNESIA', 'TF': 'FRENCH SOUTHERN TERRITORIES', 'GU': 'GUAM', 'HK': 'HONG KONG', 'IN': 'INDIA', 'ID': 'INDONESIA', 'JP': 'JAPAN', 'KI': 'KIRIBATI', 'KP': "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF", 'KR': 'KOREA, REPUBLIC OF', 'LA': "LAO PEOPLE'S DEMOCRATIC REPUBLIC", 'MO': 'MACAO', 'MY': 'MALAYSIA', 'MV': 'MALDIVES', 'MH': 'MARSHALL ISLANDS', 'FM': 'MICRONESIA, FEDERATED STATES OF', 'MN': 'MONGOLIA', 'MM': 'MYANMAR', 'NR': 'NAURU', 'NP': 'NEPAL', 'NC': 'NEW CALEDONIA', 'NZ': 'NEW ZEALAND', 'NU': 'NIUE', 'NF': 'NORFOLK ISLAND', 'MP': 'NORTHERN MARIANA ISLANDS', 'PK': 'PAKISTAN', 'PW': 'PALAU', 'PG': 'PAPUA NEW GUINEA', 'PH': 'PHILIPPINES', 'PN': 'PITCAIRN', 'WS': 'SAMOA', 'SG': 'SINGAPORE', 'SB': 'SOLOMON ISLANDS', 'LK': 'SRI LANKA', 'TW': 'TAIWAN, PROVINCE OF CHINA', 'TH': 'THAILAND', 'TL': 'TIMOR-LESTE', 'TK': 'TOKELAU', 'TO': 'TONGA', 'TV': 'TUVALU', 'VU': 'VANUATU', 'VN': 'VIET NAM', 'WF': 'WALLIS AND FUTUNA ISLANDS'}

arin = {'AI': 'ANGUILLA', 'AQ': 'ANTARCTICA', 'AG': 'ANTIGUA AND BARBUDA', 'BS': 'BAHAMAS', 'BB': 'BARBADOS', 'BM': 'BERMUDA', 'BV': 'BOUVET ISLAND', 'CA': 'CANADA', 'KY': 'CAYMAN ISLANDS', 'DM': 'DOMINICA', 'GD': 'GRENADA', 'GP': 'GUADELOUPE', 'HM': 'HEARD AND MC DONALD ISLANDS', 'JM': 'JAMAICA', 'MQ': 'MARTINIQUE', 'MS': 'MONTSERRAT', 'PR': 'PUERTO RICO', 'SH': 'SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA', 'BL': 'SAINT BARTHÉLEMY', 'KN': 'SAINT KITTS AND NEVIS', 'LC': 'SAINT LUCIA', 'PM': 'SAINT PIERRE AND MIQUELON', 'MF': 'SAINT MARTIN (FRENCH PART)', 'VC': 'SAINT VINCENT AND THE GRENADINES', 'TC': 'TURKS AND CAICOS ISLANDS', 'US': 'UNITED STATES OF AMERICA', 'UM': 'UNITED STATES MINOR OUTLYING ISLANDS', 'VG': 'VIRGIN ISLANDS (BRITISH)', 'VI': 'VIRGIN ISLANDS (U.S.)'}

afrinic = {'DZ': 'ALGERIA', 'AO': 'ANGOLA', 'BJ': 'BENIN', 'BW': 'BOTSWANA', 'BF': 'BURKINA FASO', 'BI': 'BURUNDI', 'CM': 'CAMEROON', 'CV': 'CAPE VERDE', 'CF': 'CENTRAL AFRICAN REPUBLIC', 'TD': 'CHAD', 'KM': 'COMOROS', 'CG': 'CONGO', 'CD': 'CONGO, THE DEMOCRATIC REPUBLIC OF THE', 'CI': "CÔTE D'IVOIRE", 'DJ': 'DJIBOUTI', 'EG': 'EGYPT', 'GQ': 'EQUATORIAL GUINEA', 'ER': 'ERITREA', 'ET': 'ETHIOPIA', 'GA': 'GABON', 'GM': 'GAMBIA', 'GH': 'GHANA', 'GN': 'GUINEA', 'GW': 'GUINEA-BISSAU', 'KE': 'KENYA', 'LS': 'LESOTHO', 'LR': 'LIBERIA', 'LY': 'LIBYA', 'MG': 'MADAGASCAR', 'MW': 'MALAWI', 'ML': 'MALI', 'MR': 'MAURITANIA', 'MU': 'MAURITIUS', 'YT': 'MAYOTTE', 'MA': 'MOROCCO', 'MZ': 'MOZAMBIQUE', 'NA': 'NAMIBIA', 'NE': 'NIGER', 'NG': 'NIGERIA', 'RE': 'REUNION', 'RW': 'RWANDA', 'ST': 'SAO TOME AND PRINCIPE', 'SN': 'SENEGAL', 'SC': 'SEYCHELLES', 'SL': 'SIERRA LEONE', 'SO': 'SOMALIA', 'ZA': 'SOUTH AFRICA', 'SS': 'SOUTH SUDAN', 'SD': 'SUDAN', 'SZ': 'SWAZILAND', 'TZ': 'TANZANIA, UNITED REPUBLIC OF', 'TG': 'TOGO', 'TN': 'TUNISIA', 'UG': 'UGANDA', 'EH': 'WESTERN SAHARA', 'ZM': 'ZAMBIA', 'ZW': 'ZIMBABWE'}

ripe = {'AL': 'ALBANIA', 'AD': 'ANDORRA', 'AM': 'ARMENIA', 'AT': 'AUSTRIA', 'AZ': 'AZERBAIJAN', 'BH': 'BAHRAIN', 'BY': 'BELARUS', 'BE': 'BELGIUM', 'BA': 'BOSNIA AND HERZEGOWINA', 'BG': 'BULGARIA', 'HR': 'CROATIA (local name: Hrvatska)', 'CY': 'CYPRUS', 'CZ': 'CZECHIA', 'DK': 'DENMARK', 'EE': 'ESTONIA', 'FO': 'FAROE ISLANDS', 'FI': 'FINLAND', 'FR': 'FRANCE', 'GE': 'GEORGIA', 'DE': 'GERMANY', 'GI': 'GIBRALTAR', 'GR': 'GREECE', 'GL': 'GREENLAND', 'GG': 'GUERNSEY', 'VA': 'HOLY SEE', 'HU': 'HUNGARY', 'IS': 'ICELAND', 'IR': 'IRAN (ISLAMIC REPUBLIC OF)', 'IQ': 'IRAQ', 'IE': 'IRELAND', 'IM': 'ISLE OF MAN', 'IL': 'ISRAEL', 'IT': 'ITALY', 'JE': 'JERSEY', 'JO': 'JORDAN', 'KZ': 'KAZAKHSTAN', 'KW': 'KUWAIT', 'KG': 'KYRGYZSTAN', 'LV': 'LATVIA', 'LB': 'LEBANON', 'LI': 'LIECHTENSTEIN', 'LT': 'LITHUANIA', 'LU': 'LUXEMBOURG', 'MT': 'MALTA', 'MD': 'MOLDOVA, REPUBLIC OF', 'MC': 'MONACO', 'ME': 'MONTENEGRO', 'NL': 'NETHERLANDS, KINGDOM OF THE', 'MK': 'NORTH MACEDONIA, REPUBLIC OF', 'NO': 'NORWAY', 'OM': 'OMAN', 'PS': 'PALESTINE, STATE OF', 'PL': 'POLAND', 'PT': 'PORTUGAL', 'QA': 'QATAR', 'RO': 'ROMANIA', 'RU': 'RUSSIAN FEDERATION', 'SM': 'SAN MARINO', 'SA': 'SAUDI ARABIA', 'RS': 'SERBIA', 'SK': 'SLOVAKIA', 'SI': 'SLOVENIA', 'ES': 'SPAIN', 'SJ': 'SVALBARD AND JAN MAYEN ISLANDS', 'SE': 'SWEDEN', 'CH': 'SWITZERLAND', 'SY': 'SYRIAN ARAB REPUBLIC', 'TJ': 'TAJIKISTAN', 'TR': 'TÜRKİYE', 'TM': 'TURKMENISTAN', 'UA': 'UKRAINE', 'AE': 'UNITED ARAB EMIRATES', 'GB': 'UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND*', 'UZ': 'UZBEKISTAN', 'YE': 'YEMEN'}

lacnic = {'AR': 'ARGENTINA', 'AW': 'ARUBA', 'BZ': 'BELIZE', 'BO': 'BOLIVIA, PLURINATIONAL STATE OF', 'BQ': 'BONAIRE, SINT EUSTATIUS AND SABA', 'BR': 'BRAZIL', 'CL': 'CHILE', 'CO': 'COLOMBIA', 'CR': 'COSTA RICA', 'CU': 'CUBA', 'CW': 'CURAÇAO', 'DO': 'DOMINICAN REPUBLIC', 'EC': 'ECUADOR', 'SV': 'EL SALVADOR', 'FK': 'FALKLAND ISLANDS (MALVINAS)', 'GF': 'FRENCH GUIANA', 'GT': 'GUATEMALA', 'GY': 'GUYANA', 'HT': 'HAITI', 'HN': 'HONDURAS', 'MX': 'MEXICO', 'NI': 'NICARAGUA', 'PA': 'PANAMA', 'PY': 'PARAGUAY', 'PE': 'PERU', 'SX': 'SINT MAARTEN (DUTCH PART)', 'GS': 'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS', 'SR': 'SURINAME', 'TT': 'TRINIDAD AND TOBAGO', 'UY': 'URUGUAY', 'VE': 'VENEZUELA, BOLIVARIAN REPUBLIC OF'}


def embeder_checker(syntax, matching_list, ip):
	ipa = int(ipaddress.ip_address(ip))
	count = 0
	region = None
	country = None
	ipv4 = None
	ipv4Address = None
	ranges = None
	for v in syntax:
		if v == "region":
			region = count
		elif v == "country":
			country = count
		elif v == "ipv4":
			ipv4 = count
		elif v == "ipv4Address":
			ipv4Address = count
		elif v == "ranges":
			ranges = count
		else:
			print(f"Log:\tUnresolved embeder checker Syntax: {v}")
		count += 1
	
	match_found=[]
	count = 0	
	for v in matching_list:
		one_line = v.split("|")
		starting = int(ipaddress.ip_address(one_line[ipv4Address]))
		ending = starting + int(one_line[ranges]) - 1
		
		if (ipa >= starting) and (ipa <= ending):
			match_found.append(v)
			
	return match_found

arin_match = {}
apnic_match = {}
afrinic_match = {}
lacnic_match = {}
ripe_match = {}




def geo_finder(ip_cidr):
	global arin_match
	global apnic_match
	global afrinic_match
	global lacnic_match
	global ripe_match
	
	ip_l = ip_cidr.split('/')	
	ip_cidr_flag = False
	if '/' in ip_cidr:
		ip_cidr_flag = True
		try:
			aa = ipaddress.ip_network(ip_cidr)
		except Exception as e:
			print(f"Check Your Cidr: {ip_cidr}")
			print(str(e))
			print("\nExiting!")
			exit(1)
			
	else:
		try:
			aa = ipaddress.ip_address(ip_l[0])
		except Exception as e:
			print(f"Check Your IPv4: {ip_l[0]}")
			print(str(e))
			print("\nExiting!")
			exit(1)
	
	ip_add = ip_l[0]
	ipa = ipaddress.ip_address(ip_add)
	arin = "DB/delegated-arin-extended-latest"
	apnic = "DB/delegated-apnic-latest"
	afrinic = "DB/delegated-afrinic-latest"
	lacnic = "DB/delegated-lacnic-latest"
	ripe = "DB/delegated-ripencc-latest"
	
	ip_split = ip_add.split(".")
	
	with open(arin,'r') as f:
		matching_lines = []
		reg_pat = r'ipv4\|' + ip_split[0] + r'.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
		for line in f:
			if re.search(reg_pat, line):
				if line not in matching_lines:
					matching_lines.append(line.rstrip())
					
		embeder_syntax = ["region", "country", "ipv4", "ipv4Address", "ranges"]		
		arin_m = embeder_checker(embeder_syntax, matching_lines, ip_add)
		
	with open(apnic,'r') as f:
		matching_lines = []
		reg_pat = r'ipv4\|' + ip_split[0] + r'.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
		for line in f:
			if re.search(reg_pat, line):
				if line not in matching_lines:
					matching_lines.append(line.rstrip())
					
		embeder_syntax = ["region", "country", "ipv4", "ipv4Address", "ranges"]		
		apnic_m = embeder_checker(embeder_syntax, matching_lines, ip_add)
		
	with open(afrinic,'r') as f:
		matching_lines = []
		reg_pat = r'ipv4\|' + ip_split[0] + r'.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
		for line in f:
			if re.search(reg_pat, line):
				if line not in matching_lines:
					matching_lines.append(line.rstrip())
					
		embeder_syntax = ["region", "country", "ipv4", "ipv4Address", "ranges"]		
		afrinic_m = embeder_checker(embeder_syntax, matching_lines, ip_add)
		
	with open(lacnic,'r') as f:
		matching_lines = []
		reg_pat = r'ipv4\|' + ip_split[0] + r'.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
		for line in f:
			if re.search(reg_pat, line):
				if line not in matching_lines:
					matching_lines.append(line.rstrip())
					
		embeder_syntax = ["region", "country", "ipv4", "ipv4Address", "ranges"]		
		lacnic_m = embeder_checker(embeder_syntax, matching_lines, ip_add)
		
	with open(ripe,'r') as f:
		matching_lines = []
		reg_pat = r'ipv4\|' + ip_split[0] + r'.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
		for line in f:
			if re.search(reg_pat, line):
				if line not in matching_lines:
					matching_lines.append(line.rstrip())
					
		embeder_syntax = ["region", "country", "ipv4", "ipv4Address", "ranges"]		
		ripe_m = embeder_checker(embeder_syntax, matching_lines, ip_add)
		
		
	if arin_m != []:
		arin_match[ip_cidr] = arin_m
	if apnic_m != []:
		apnic_match[ip_cidr] = apnic_m
	if afrinic_m != []:
		afrinic_match[ip_cidr] = afrinic_m
	if lacnic_m != []:
		lacnic_match[ip_cidr] = lacnic_m
	if ripe_m != []:
		ripe_match[ip_cidr] = ripe_m
		
	if arin_m == [] and apnic_m == [] and afrinic_m == [] and lacnic_m == [] and ripe_m == []:
		print(f"Log:\tCan't find data for {ip_cidr}")

	



def preety_printer(host):
	global arin_match
	global afrinic_match
	global apnic_match
	global lacnic_match
	global ripe_match
	print(f"\nTotal Host Input: {len(host)}")
	print(f"Total Result Found: {len(arin_match) + len(afrinic_match) + len(apnic_match) + len(lacnic_match) + len(ripe_match)}\n")
	print("-------------------------------------------------------------------------------------------------------------------------------")
	print("Arin Match:\n")
	sorted_printer(arin_match)
	print("")
	print("-------------------------------------------------------------------------------------------------------------------------------")
	print("Afrinic Match\n")
	sorted_printer(afrinic_match)
	print("")
	print("-------------------------------------------------------------------------------------------------------------------------------")
	print("Apnic Match:\n")
	sorted_printer(apnic_match)
	print("")
	print("-------------------------------------------------------------------------------------------------------------------------------")
	print("Lacnic Match:\n")
	sorted_printer(lacnic_match)
	print("")
	print("-------------------------------------------------------------------------------------------------------------------------------")
	print("Ripe Match:\n")
	sorted_printer(ripe_match)


def check_ip(queue):
	while True:
		ip = queue.get()
		if ip is None:	
			break
		geo_finder(ip)
		queue.task_done()
			



if ip_check is None and input_file is None:
	usage()
	
	
if input_file is not None:
	with open(input_file) as f:
    		domains = f.readlines()
    		
elif ip_check is not None:
	pattern = r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(?:/[0-9]{1,2})?'
	host = re.findall(pattern, ip_check)
	domains = host
    
# strip whitespace and remove empty lines
domains = [x.strip() for x in domains if x.strip()]


domain_queue = Queue()


for domain in domains:
    domain_queue.put(domain)
    # get IP address

print(f"Thread: {str(thread)}")
for _ in range(thread):
	t = threading.Thread(target=check_ip, args=(domain_queue,))
	t.start()
	
domain_queue.join()

for _ in range(thread):
	domain_queue.put(None)
	
		
print("------------------------------------------------------------------------Threading End----------------------------------------------------------------------------------------")

def range_to_cidr(ip_range):
	start,end = map(int, ip_range.split('-'))
	start_ip = '.'.join(str((start >> (24 - i*8)) & 255) for i in range(4))
	mask = 32 - (end-start).bit_length()
	cidr_notation = f"{start_ip}/{mask}"
	return cidr_notation


def sorted_printer(db):
	global apnic
	global arin
	global afrinic
	global ripe
	global lacnic
	sorted_db = {}
	for v in db:
		ip_data = db[v]
		data_list = ip_data[0].split("|")
		country = data_list[1]
		if country in sorted_db:
			sorted_db[country].append(v)
		elif country not in sorted_db:
			sorted_db[country] = [v]
			
	count = 0
	for v in sorted_db:
		ip_list = sorted_db[v]
		for data in ip_list:
			data_to_print = db[data]
			for list_data in data_to_print:
				string_data = list_data.split("|")
				region = string_data[0]
				country = string_data[1]
				ip_start = int(ipaddress.ip_address(string_data[3]))
				
				ranges = string_data[4]
				ip_end = ip_start + int(ranges) - 1
				date = string_data[5]
				formated_date = f"{date[:4]}|{date[4:6]}|{date[6:]}"
				status = string_data[6]
				cidr = str(ip_start) + "-" + str(ip_end)
				ip_cidr = range_to_cidr(cidr)
				long_country = None
				
				if region == "apnic":
					try:
						long_country = apnic[country]
					except Exception as e:
						print(f"Log:\tCountry Code '{country}' Not Found in apnic region")
						long_country = country
						
				elif region == "arin":
					try:
						long_country = arin[country]
					except Exception as e:
						print(f"Log:\tCountry Code '{country}' Not Found in arin region")
						long_country = country
						
				elif region == "afrinic":
					try:
						long_country = afrinic[country]
					except Exception as e:
						print(f"Log:\tCountry Code '{country}' Not Found in afrinic region")
						long_country = country
						
				elif region == "lacnic":
					try:
						long_country = lacnic[country]
					except Exception as e:
						print(f"Log:\tCountry Code '{country}' Not Found in lacnic region")
						long_country = country
						
				elif region == "ripencc":
					try:
						long_country = ripe[country]
					except Exception as e:
						print(f"Log:\tCountry Code '{country}' Not Found in ripencc region\n")
						long_country = country
						
				else:
					print(f"Log:\tUnknown Country or Region {country}")
				
				extra = ""	
				if(data == str(ip_cidr)):
					extra = "*"
				
				print(f"{data:<20}{str(ip_cidr):<20}{str(ranges):<20}{str(status):<20}{formated_date:<20}{str(long_country):<20}{extra}")
				count += 1
	print(f"Total Count: {str(count)}")
			

preety_printer(domains)

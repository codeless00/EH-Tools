import sys

def f_help():
	print("Usage: python difference.py file1 file2")
	print("""
	It will tell exactly the differenc between to file.
	Which line is Common and which line is specific to which file""")
	exit(1)
	
file1 = None
file2 = None

for value in sys.argv:
	if value == "-h" or value == "--help":
		f_help()

file1 = sys.argv[1]
file2 = sys.argv[2]

common_content = []
onlyin_file1 = []
onlyin_file2 = []

file1_open = open(file1, 'r')
file2_open = open(file2, 'r')
file10_content = file1_open.readlines()
file20_content = file2_open.readlines()
file1_content = []
file2_content = []
for value in file10_content:
	if value not in file1_content:
		file1_content.append(value)
for value in file20_content:
	if value not in file2_content:
		file2_content.append(value)


file1_open.close()
file2_open.close()

for value in file1_content:
	if value in file2_content:
		common_content.append(value)
	elif value not in onlyin_file1:
		onlyin_file1.append(value)

for value in file2_content:
	if value in file1_content:
		common_content.append(value)
	elif value not in onlyin_file2:
		onlyin_file2.append(value)
print("-----------------------------------------------------------------------------------------------------------")
print(f'\nOnly in ({file1}) => \n')

if onlyin_file1 == []:
	print("None")
else:
	
	for value in onlyin_file1:
		print(value.rstrip("\n"))
	print("\nLength: " + str(len(onlyin_file1)))
print("-----------------------------------------------------------------------------------------------------------")

	
print(f'\nOnly in ({file2}) => \n')
if onlyin_file2 == []:
	print("None")
else:	
	
	for value in onlyin_file2:
		print(value.rstrip("\n"))
	print("\nLength: " + str(len(onlyin_file2)))
print("------------------------------------------------------------------------------------------------------------")	
print("\nIn Both Files:\n")

if common_content == []:
	print("None")
else:
	tmp = []
	
	for value in common_content:
		if value not in tmp:
			tmp.append(value)
	
	for value in tmp:
		print(value.rstrip("\n"))
	print("\nLength: " + str(len(tmp)))


import sys

def f_help():
	print(f"Usage: python {sys.argv[0]} filename")
	print("It will print unique Line in the file. If the line is repeated it will ignore it")
	print("""
	For example:
	
	hellow
	sys
	hellow
	app
	
	Result:
	
	hellow
	sys
	app""")
	exit(1)
	
for v in sys.argv:
	if v == "-h" or v == "--help":
		f_help()
tmp = []
input_file = sys.argv[1]
with open(input_file, 'r') as f:
	text = f.readlines()
	#print("")
	
	for v in text:
		if v not in tmp:
			tmp.append(v)
			print(v.rstrip())
	
	#print(f"\n\nTotal Input: {len(text)}")
	#print(f"Total Output:{len(tmp)}\n")
	#print("Done...")

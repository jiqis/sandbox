def read_command(line):
	l=line.split(' ')
	cmd=l[0]
	l.pop
	args=l
	return (cmd,args)

dict = {}

while True:
	
	line=raw_input("> ")
	
	if cmd=="quit" :
		break
	else:
		print("%s" % (cmd))

print("QUIT")
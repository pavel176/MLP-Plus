from rich import print

def log(text):
	print(text)

def log_script(script: list[list[str]]):
	print("="*50)
	print("Script:")
	for i in range(len(script)):
		print(f"{i}: {script[i]}")
	print("="*50)
	
def log_aov(root):
	print(
		f"{root.name} {root.announcement}:{root.start}-{root.end}"
	)
	if len(root.variables) > 0 or len(root.functions) > 0:
		print("<")
		for func in root.functions:
			print(f"  f: {func}")
		for var in root.variables:
			print(f"  v: {var}")
		print(">")
	else:
		print("<>")
	for i in root.child:
		print(f"|- {i.name} {i.announcement}:{i.start}-{i.end}", sep="")
		if len(i.variables) > 0 or len(i.functions) > 0:
			print("   <")
			for func in i.functions:
				print(f"     f: {func}")
			for var in i.variables:
				print(f"     v: {var}")
			print("   >")
		else:
			print("<>")
		log_aov_recurse(i, 1)

def log_aov_recurse(s, tab):
	for i in s.child:
		print(
			"   " * tab, f"|- {i.name} {i.announcement}:{i.start}-{i.end}", sep=""
		)

		if len(i.variables) > 0 or len(i.functions) > 0:
			print("   " * tab, "   <", sep="")
			for func in i.functions:
				print("   " * tab, f"     f: {func}", sep="")
			for var in i.variables:
				print("   " * tab, f"     v: {var}", sep="")
			print("   " * tab, "   >", sep="")
		else:
			print("   " * tab, "   <>", sep="")
		log_aov_recurse(i, tab + 1)

def warning(text):
	print(f"[yellow]{text}[/yellow]")

def error(text):
	print(f"[bold red]{text}[/bold red]")
	exit()

def help():
	print(
	'''
	mlp <path> - компилирует скрипт
	'''
	)
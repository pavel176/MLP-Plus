script_path = "new_main.mlp"

import utils


class AOV:
	child:    list
	start:    int
	end:      int
	variable: list[list[str, int]]

	def __init__(self, start=0, end=0):
		self.start = start
		self.end = end
		self.child = []
		self.variable = []

	def add_var(self, var):
		self.variable.append(var)
		for child in self.child:
			child.add_var(var)

	def var_is_create(self, variable_name) -> bool:
		for variable in self.variable:
			if variable[0] == variable_name:
				return True
		return False


def get_aov_path(line_id: int, node) -> list[AOV]:
	for child_node in node.child:
		if child_node.start <= line_id <= child_node.end:
			return [node] + get_aov_path(line_id, child_node)
	return [node]

def generate_aov(script: list[list[str]], parent: AOV, tab=0):
	in_structure = False
	start_structure = 0

	for code_stroke_id in range(parent.end - parent.start + 1):
		code_stroke = parent.start + code_stroke_id

		if not in_structure:
			if tab < script[code_stroke].count("\t"):
				in_structure = True
				start_structure = code_stroke

		if in_structure:
			if tab >= script[code_stroke].count("\t"):
				end_structure = code_stroke - 1

				parent.child.append(AOV(
					start_structure,
					end_structure
				))

				in_structure = False
				start_structure = 0
			elif code_stroke == len(script)-1:
				end_structure = code_stroke

				parent.child.append(AOV(
					start_structure,
					end_structure
				))

				in_structure = False
				start_structure = 0


	for child in parent.child:
		generate_aov(script, child, tab+1)

def join_link_jump(script: list[str]) -> list[str]:
	result = []
	links = [] #jump, link
	for line in script:
		if line.split()[0] == "jump":
			jump = script.index(line)
			link = script.index(f"link {line.split()[1]}")

			margin_jump = 0
			margin_link = 0

			if jump < link:
				for i in range(jump):
					if script[i].split()[0] == "link":
						margin_jump += 1
				margin_link = margin_jump
				for i in range(link - jump - 1):
					ii = jump + i + 1
					if script[ii].split()[0] == "link":
						margin_link += 1
			else:
				for i in range(link):
					if script[i].split()[0] == "link":
						margin_link += 1
				margin_jump = margin_link
				margin_jump += 1
				for i in range(jump - link - 1):
					ii = link + i + 1
					if script[ii].split()[0] == "link":
						margin_jump += 1
			links.append([
				jump - margin_jump,
				link - margin_link
			])
	result = list(filter(lambda x: x.split()[0] != "link", script))
	for i in range(len(result)):
		line = result[i]
		if line.split()[0] == "jump":
			link_line = 0
			for link in links:
				if link[0] == i:
					link_line = link[1]
			result[i] = " ".join(["jump", str(link_line), line.split()[2], line.split()[3], line.split()[4]])
	return result

with open(script_path, "r") as script_file:
	script = script_file.read().split("\n")
	result_source = []
	code_info = {}

	#region script filter and generate aov
	script = list(filter(lambda x: len(x) > 0 and x[0] != "#", script))
	script = [utils.split_save_text(" \t\n=<>:.", "\"\'", i) for i in script]
	script = [list(filter(lambda x: x != " ", i)) for i in script]
	root = AOV(end=len(script)-1)
	generate_aov(script, root)
	script = [list(filter(lambda x: x != "\t", i)) for i in script]
	#endregion

	# region generate script
	for line_id in range(len(script)):
		line = script[line_id]
		aov = get_aov_path(line_id, root)

		if len(line) == 2 and line[0] == "print":
			if "printflush" not in code_info.keys():
				code_info["printflush"] = "message1"
			if line[1][0] in "\"\'0123456789":
				result_source.append(f"print {line[1]}")
			else:
				result_source.append(f"print v_{line[1]}")
				if not aov[-1].var_is_create(f"v_{line[1]}"):
					print(f"ERROR {line_id}")
					exit()
			result_source.append(f"printflush {code_info['printflush']}")

		if len(line) == 2 and line[0] == "wait":
			if line[1][0] in "0123456789":
				result_source.append(f"wait {line[1]}")
			else:
				if not aov[-1].var_is_create(f"v_{line[1]}"):
					print(f"ERROR {line_id}")
					exit()
				result_source.append(f"wait v_{line[1]}")

		if len(line) == 2 and line[0] == "printflush":
			if "printflush" not in code_info.keys():
				code_info["printflush"] = line[1]

		if len(line) >= 3 and line[1] == "=":
			if not aov[-1].var_is_create(f"v_{line[0]}"):
				aov[-1].add_var([f"v_{line[0]}", line_id])

			elif len(line) == 5 and line[3] == "+":
				result_source.append(f"op add v_{line[0]} {line[2]} {line[4]}")
			elif len(line) == 5 and line[3] == "-":
				result_source.append(f"op sub v_{line[0]} {line[2]} {line[4]}")
			elif len(line) == 5 and line[3] == "*":
				result_source.append(f"op mul v_{line[0]} {line[2]} {line[4]}")
			elif len(line) == 5 and line[3] == "/":
				result_source.append(f"op div v_{line[0]} {line[2]} {line[4]}")

			if len(line) == 4 and line[2] == "getlink":
				result_source.append(f"getlink v_{line[0]} {line[3]}")
			elif len(line) == 5 and line[2] == "read":
				result_source.append(f"read v_{line[0]} {line[3]} {line[4]}")
			elif len(line) == 7 and line[2] == "RGBA":
				result_source.append(f"packcolor v_{line[0]} {line[3]} {line[4]} {line[5]} {line[6]}")
			elif len(line) == 5 and line[2] == "sensor":
				result_source.append(f"sensor v_{line[0]} {line[3]} {line[4]}")
			elif len(line) == 9 and line[2] == "radar":
				result_source.append(f"radar {line[3]} {line[4]} {line[5]} {line[6]} {line[7]} {line[8]} v_{line[0]}")
			elif len(line) == 9 and line[2] == "uradar":
				result_source.append(f"uradar {line[3]} {line[4]} {line[5]} {line[6]} {line[7]} {line[8]} v_{line[0]}")
			elif len(line) == 7 and line[3] == "ulocate" and (line[4] == "ore" or line[4] == "spawn" or line[4] == "damaged"):
				if line[6] == "x":
					result_source.append(f"ulocate {line[4]} core true {line[5]} v_{line[0]} sv_a sv_a sv_a")
				if line[6] == "y":
					result_source.append(f"ulocate {line[4]} core true {line[5]} sv_a v_{line[0]} sv_a sv_a")
				if line[6] == "found":
					result_source.append(f"ulocate {line[4]} core true {line[5]} sv_a sv_a v_{line[0]} sv_a")
				if line[6] == "building":
					result_source.append(f"ulocate {line[4]} core true {line[5]} sv_a sv_a sv_a v_{line[0]}")
			elif len(line) == 8 and line[3] == "ulocate" and line[4] == "building":
				if line[7] == "x":
					result_source.append(f"ulocate building {line[5]} {line[6]} @copper v_{line[0]} sv_a sv_a sv_a")
				if line[7] == "y":
					result_source.append(f"ulocate building {line[5]} {line[6]} @copper sv_a v_{line[0]} sv_a sv_a")
				if line[7] == "found":
					result_source.append(f"ulocate building {line[5]} {line[6]} @copper sv_a sv_a v_{line[0]} sv_a")
				if line[7] == "building":
					result_source.append(f"ulocate building {line[5]} {line[6]} @copper sv_a sv_a sv_a v_{line[0]}")

			else:
				result_source.append(f"set v_{line[0]} {line[2]}")

		if len(line) == 4 and line[0] == "write":
			if line[1][0] in "\"\'0123456789":
				result_source.append(f"write {line[1]} {line[2]} {line[3]}")
			else:
				if not aov[-1].var_is_create(f"v_{line[1]}"):
					print(f"ERROR {line_id}")
					exit()
				result_source.append(f"write v_{line[1]} {line[2]} {line[3]}")

		if len(line) >= 2 and line[0] == "if":
			if len(script)-1 > line_id:
				if aov[-1] != get_aov_path(line_id + 1, root)[-1]:
					jump_aov = get_aov_path(line_id + 1, root)
				else:
					print(f"ERROR {line_id}")
					exit()
			else:
				print(f"ERROR {line_id}")
				exit()
			jump_line_id = f"{jump_aov[-1].start}-{jump_aov[-1].end}"
			# if aov[0].end == len(script) - 1:
			# 	jump_line_id += 1
			# 	if not aov[-1].var_is_create(f"v_{line[1]}"):
			# 		print(f"ERROR {line_id}")
			# 		exit()
			var_a = ""
			var_b = ""
			if len(line) == 2:
				if line[2][0] in "\"\'0123456789":
					var_a = line[2]
				else:
					var_a = f"v_{line[2]}"
			if len(line) == 3:
				if line[2][0] in "\"\'0123456789":
					var_a = line[2]
				else:
					var_a = f"v_{line[2]}"
			if len(line) == 4:
				if line[1][0] in "\"\'0123456789":
					var_a = line[1]
				else:
					var_a = f"v_{line[1]}"

				if line[3][0] in "\"\'0123456789":
					var_b = line[3]
				else:
					var_b = f"v_{line[3]}"

			if len(line) == 5:
				if line[1][0] in "\"\'0123456789":
					var_a = line[1]
				else:
					var_a = f"v_{line[1]}"

				if line[4][0] in "\"\'0123456789":
					var_b = line[4]
				else:
					var_b = f"v_{line[4]}"

			if var_a[:2] == "v_":
				if not aov[-1].var_is_create(var_a):
					print(f"ERROR {line_id}")
					exit()
			if var_b[:2] == "v_":
				if not aov[-1].var_is_create(var_b):
					print(f"ERROR {line_id}")
					exit()

			if len(line) == 2:
				result_source.append(f"jump {jump_line_id} equal {var_a} false")
			if len(line) == 3 and line[1] == "not":
				result_source.append(f"jump {jump_line_id} equal {var_a} true")
			if len(line) == 4 and line[2] == "<":
				result_source.append(f"jump {jump_line_id} greaterThanEq {var_a} {var_b}")
			if len(line) == 4 and line[2] == ">":
				result_source.append(f"jump {jump_line_id} lessThanEq {var_a} {var_b}")
			if len(line) == 4 and line[2] == "not":
				result_source.append(f"jump {jump_line_id} equal {var_a} {var_b}")
			if len(line) == 5 and line[2:4] == ["<", "="]:
				result_source.append(f"jump {jump_line_id} greaterThan {var_a} {var_b}")
			if len(line) == 5 and line[2:4] == [">", "="]:
				result_source.append(f"jump {jump_line_id} lessThan {var_a} {var_b}")
			if len(line) == 5 and line[2:4] == ["=", "="]:
				result_source.append(f"jump {jump_line_id} notEqual {var_a} {var_b}")

		if len(line) >= 2 and line[0] == "while":
			if len(script)-1 > line_id:
				if aov[-1] != get_aov_path(line_id + 1, root)[-1]:
					jump_aov = get_aov_path(line_id + 1, root)
				else:
					print(f"ERROR {line_id}")
					exit()
			else:
				print(f"ERROR {line_id}")
				exit()
			jump_line_id = f"{jump_aov[-1].start}-{jump_aov[-1].end}"

			result_source.append(f"link {jump_aov[-1].start}-{jump_aov[-1].end}-back")
			var_a = ""
			var_b = ""
			if len(line) == 2:
				if line[2][0] in "\"\'0123456789":
					var_a = line[2]
				else:
					var_a = f"v_{line[2]}"
			if len(line) == 3:
				if line[2][0] in "\"\'0123456789":
					var_a = line[2]
				else:
					var_a = f"v_{line[2]}"
			if len(line) == 4:
				if line[1][0] in "\"\'0123456789":
					var_a = line[1]
				else:
					var_a = f"v_{line[1]}"

				if line[3][0] in "\"\'0123456789":
					var_b = line[3]
				else:
					var_b = f"v_{line[3]}"
			if len(line) == 5:
				if line[1][0] in "\"\'0123456789":
					var_a = line[1]
				else:
					var_a = f"v_{line[1]}"

				if line[4][0] in "\"\'0123456789":
					var_b = line[4]
				else:
					var_b = f"v_{line[4]}"

			if var_a[:2] == "v_":
				if not aov[-1].var_is_create(var_a):
					print(f"ERROR {line_id}")
					exit()
			if var_b[:2] == "v_":
				if not aov[-1].var_is_create(var_b):
					print(f"ERROR {line_id}")
					exit()

			if len(line) == 2:
				result_source.append(f"jump {jump_line_id} equal {var_a} false")
			if len(line) == 3 and line[1] == "not":
				result_source.append(f"jump {jump_line_id} equal {var_a} true")
			if len(line) == 4 and line[2] == "<":
				result_source.append(f"jump {jump_line_id} greaterThanEq {var_a} {var_b}")
			if len(line) == 4 and line[2] == ">":
				result_source.append(f"jump {jump_line_id} lessThanEq {var_a} {var_b}")
			if len(line) == 4 and line[2] == "not":
				result_source.append(f"jump {jump_line_id} equal {var_a} {var_b}")
			if len(line) == 5 and line[2:4] == ["<", "="]:
				result_source.append(f"jump {jump_line_id} greaterThan {var_a} {var_b}")
			if len(line) == 5 and line[2:4] == [">", "="]:
				result_source.append(f"jump {jump_line_id} lessThan {var_a} {var_b}")
			if len(line) == 5 and line[2:4] == ["=", "="]:
				result_source.append(f"jump {jump_line_id} notEqual {var_a} {var_b}")

		# region draw
		if len(line) >= 2 and line[0] == "draw":
		# endregion

		if line_id == aov[-1].end:
			if aov[-1].start != 0:
				if script[aov[-1].start - 1][0] == "while":
					result_source.append(f"jump {aov[-1].start}-{aov[-1].end}-back always 0 0")
					result_source.append(f"link {aov[-1].start}-{aov[-1].end}")
				if script[aov[-1].start - 1][0] == "if":
					result_source.append(f"link {aov[-1].start}-{aov[-1].end}")
	result_source.append(f"end")
	# endregion

	# region post-processing of the script
	processed_script = []
	for line in result_source:
		if line.find("\n") == -1:
			processed_script.append(line)
		else:
			subline = line.split("\n")
			for i in subline:
				processed_script.append(i)
	result_script = join_link_jump(processed_script)
	# endregion

	# region print script
	for a in range(len(script)):
		print(f"[{a}] ", end="\t")
		for b in script[a]:
			print(f" {b}", end="")
		print("")
	# endregion

	print("=" * 10)

	#region print result source
	print(f"len = {len(processed_script)}")
	for a in processed_script:
		print(a)
	#endregion

	print("="*10)

	#region print result script
	print(f"len = {len(result_script)}")
	for a in range(len(result_script)):
		print(f"[{a}] \t{result_script[a]}")
	#endregion
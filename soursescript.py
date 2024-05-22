import os
import utils


class SourseScript:
	script_path = ""
	script = []  # Список строк в которых записаны  списки блоков для более удобной работы с скриптами

	def __init__(self, input_path):
		if len(input_path) >= 2 and input_path[1] != ":":
			self.script_path = os.path.join(os.getcwd(), input_path)
		else:
			self.script_path = input_path

		with open(self.script_path, 'r') as file:
			script = [line.strip(" ") for line in file]
			raw_script = list(map(lambda line: utils.split_save_text(" \t\n()[]{}:,#!-", "\"\'", line), script))
			if len(raw_script) > 0 and raw_script[-1][-1] != '\n':
				raw_script[-1].append("\n")
			for line in range(len(raw_script)):
				# todo Add support for spaces
				raw_script[line] = list(filter(lambda text: text != " ", raw_script[line]))
			self.script = self.form_monolithic_line(raw_script)
			# self.found_variables_form_AOV()

	def form_monolithic_line(self, raw_script):
		result = []
		open_bodies = []
		last_line = []
		for line in raw_script:
			for block in line:
				if block == "\n":
					if len(open_bodies) > 0:
						last_line += line
					else:
						result.append(last_line + line)
						last_line = []
				if block in "([{":
					open_bodies.append(block)
				if block in ")]}":
					if len(open_bodies) > 0:
						if block == ")" and open_bodies[-1] == "(":
							open_bodies.pop(-1)
						elif block == "]" and open_bodies[-1] == "[":
							open_bodies.pop(-1)
						elif block == "}" and open_bodies[-1] == "{":
							open_bodies.pop(-1)
						else:
							# todo Add normal raise
							raise Exception("Error")
		for line in range(len(result)):
			# todo Rename variable
			tabs_end = False
			result_line = []
			for block in result[line]:
				if block != "\t":
					result_line.append(block)
					if not tabs_end:
						tabs_end = True
				else:
					if not tabs_end:
						result_line.append(block)
			result_line = list(filter(lambda text: text != "\n", result_line))
			result[line] = result_line
		# result[line] = result_line + ['\n']
		result = list(filter(lambda arr: len(arr) > 0, result))
		result_filtered = []
		for index in range(len(result)):
			line = result[index]
			if len(line) > 0:
				if len(line) == len(list(filter(lambda arr: not ("#" in arr), line))):
					result_filtered.append(line)
		return result_filtered

def get_sourse_script(path):
	return SourseScript(path).script  # Заменить на адекватную реализацию
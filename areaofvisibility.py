import utils


class AOV:
	name:         str
	variables:    list[dict]  # name announcement type
	functions:    list[dict]  # name announcement input[type type ...] output_type
	child:        list
	announcement: int
	start:        int
	end:          int

	def __init__(self, name="root", announcement=-1, start=0, end=0, variables=None, functions=None):
		self.name = name
		self.announcement = announcement
		self.start = start
		self.end = end
		self.child = []

		if variables is not None:
			self.variables = variables + []
		else:
			self.variables = []

		if functions is not None:
			self.functions = functions + []
		else:
			self.functions = []

	@staticmethod
	def get_aov_path(line_id: int, node) -> list:
		for child_node in node.child:
			if child_node.start <= line_id <= child_node.end:
				return [node] + AOV.get_aov_path(line_id, child_node)
		return [node]

	def add_variable(self, data: list[str]):
		self.variables.append(data)
		for child in self.child:
			child.add_variable(data)

	def add_function(self, data: list[str]):
		self.functions.append(data)
		for child in self.child:
			child.add_function(data)


def generate_aov(script: list[list[str]], parent: AOV, tab=0, last_noname_id = 0):
	in_structure = False
	start_structure = 0
	end_structure = 0
	announcement_structure = -1
	name_structure = ""

	for code_stroke_id in range(parent.end - parent.start + 1):
		code_stroke = parent.start + code_stroke_id

		if not in_structure:
			if tab < script[code_stroke].count("\t"):

				in_structure = True
				start_structure = code_stroke
				1
				if code_stroke > 0:
					if utils.no_tab(script[code_stroke-1])[0] in ["for", "while", "if", "elif", "else", "def"]:

						announcement_structure = code_stroke-1

						if utils.no_tab(script[code_stroke-1])[0] == "def":
							name_structure = utils.no_tab(script[code_stroke-1])[1]  #todo Добавить проверку нличия имени
						else:
							name_structure = f"{utils.no_tab(script[code_stroke - 1])[0]}_{last_noname_id}"
							last_noname_id += 1

		else:
			if tab >= script[code_stroke].count("\t") or code_stroke == len(script)-1:
				end_structure = code_stroke

				parent.child.append(AOV(
					name_structure,
					announcement_structure,
					start_structure,
					end_structure,
					parent.variables,
					parent.functions
				))

				in_structure = False
				start_structure = 0
				end_structure = 0
				announcement_structure = -1
				name_structure = ""

	for child in parent.child:
		generate_aov(script, child, tab+1, last_noname_id)

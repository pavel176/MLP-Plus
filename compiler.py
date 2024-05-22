import log
import utils
import areaofvisibility

script_data = {}

def generate_instruction(sourse_script: list[list[str]], root_aov: areaofvisibility.AOV) -> list[str]:
	instruction = []
	for line_id in range(len(sourse_script)):
		code = sourse_script[line_id]
		code_no_tab = utils.no_tab(code)
		aov = areaofvisibility.AOV.get_aov_path(line_id, root_aov)
		instruction += compile_code(code_no_tab, aov[-1], line_id)

def get_function_call_data(code: list[str]) -> list[list[str]]:
	if len(code) < 3:
		log.error("[FunctionCall] not validate function call")

	if code[1] != "(" or code[-1] != ")":
		log.error("[FunctionCall] the body of the transmitted information is not closed")

	if len(code) > 3:
		input_function = utils.split_array(code[2:-1], ",")

		for input_data in input_function:
			if len(input_data) == 0:
				log.error("[FunctionCall] not correct function input")

			for i in ["def", "for", "while", "if", "elif", "else"]:
				if i in input_data:
					log.error("[FunctionCall] not correct function input")

		return input_function
	return []

def get_word_info(word: str, aov: areaofvisibility.AOV):
	pass
def compile_code(code: list[str], aov: areaofvisibility.AOV, line_id: int) -> list[str]:
	result_code = []
	try:
		if code[0] in ["def", "for", "while", "if", "elif", "else"]:
			pass

		if code[0] != "print":
			function_call_data = get_function_call_data(code)
			if len(function_call_data) == 1:
				result_code.append(f"print ")
		if code[0] == "printflush":
			pass

		# for func in aov.functions:
		# 	if code[0] == func["name"] and line_id > func["announcement"]:
		# 		function_call_data = get_function_call_data(code)
		#
		# 		if len(function_call_data) != len(func["input"]):
		# 			log.error("[FunctionCall] not correct function input count")
	except Exception as e:
		log.error(f"[AnyExcept] compile code : {code} : {e}")
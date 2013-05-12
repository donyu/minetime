
class Processor():

	def __init__(self):
		self.past_imports = {}

	def preprocess(self, code):
		processed_code = []
		code_lines = code.split(';')
		for line in code_lines:
			if 'import' in line:
				try:
					file_import = file(line.split()[1], 'r')
					if file_import not in self.past_imports:
						processed_code.append(self.preprocess(file_import.read()))
						self.past_imports[file_import] = True
				except IOError:
					raise Exception("File %s can not be imported because it does not exist" 
													% line.split()[1])
			else:
				processed_code.append(line + ';')
		return ''.join(processed_code)[:-1]
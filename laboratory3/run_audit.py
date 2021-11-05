import os
import re
import json

def check_audit():
	file = open('output.json',)
	audit = json.load(file)

	with open('audit_result.txt', 'w') as to_save:
		for custom_item in audit:

			cmd = 'cd ~ && ' + custom_item['cmd'][1:-1]
			output = os.popen(cmd).read()

			pattern = custom_item['expect'][1:-1]

			is_present = re.search(pattern, output)

			to_save.write(custom_item['description'][1:-1] + '\t\t\t\t\t\t')
			if is_present:
				to_save.write('Correct' + '\n\n')
			else:
				to_save.write('Invalid' + '\n')
				to_save.write('Expected : ' + custom_item['expect'][1:-1] + '\n')
				to_save.write('Found : ' + output + '\n\n')
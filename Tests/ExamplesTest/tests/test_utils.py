import platform
import os
from itertools import filterfalse
import subprocess
import tempfile

DEFAULT_EXAMPLE_DIR = os.path.abspath('../../Dist/examples/')

def run_example(example_name, args, timeout=10, expected_return_code=0, requires_root=False):
	command_to_run = (['sudo'] if requires_root and (platform.system() == 'Linux' or platform.system() == 'Darwin') else []) + [os.path.join(DEFAULT_EXAMPLE_DIR, example_name)]
	for flag, val in args.items():
		if flag:
			command_to_run.append(flag)
		if val:
			command_to_run.append(val)
	print('command_to_run', command_to_run)
	completed_process = subprocess.run(command_to_run, capture_output=True, text=True, timeout=timeout)
	print('stdout', completed_process.stdout)
	assert completed_process.returncode == expected_return_code
	return completed_process

def text_file_contains(file_path, expected_content):
	if not os.path.exists(file_path):
		return False

	with open(file_path) as f:
		return expected_content in f.read()

def compare_files_ignore_newline(filename1, filename2):
	with open(filename1, 'r') as f1:
		with open(filename2, 'r') as f2:
			return all(line_f1 == line_f2 for line_f1, line_f2 in zip(f1, f2))

def compare_stdout_with_file(stdout, file_path, skip_line_predicate):
	assert os.path.exists(file_path)
	
	with open(file_path, 'r') as f:
		for line_f, line_stdout in zip(filterfalse(skip_line_predicate, f), filterfalse(skip_line_predicate, stdout.splitlines())):
				assert line_f.rstrip('\n') == line_stdout

class ExampleTest(object):

	def run_example(self, args, timeout=10, expected_return_code=0, requires_root=False):
		return run_example(example_name=self.__class__.__name__[4:], args=args, timeout=timeout, expected_return_code=expected_return_code, requires_root=requires_root)
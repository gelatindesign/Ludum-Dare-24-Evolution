from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

file_root = "G:\\Code\\Local\\Ludum-Dare-24-Evolution\\"

DATA_FILES = []
for files in os.listdir(file_root + 'sprites/enemies/'):
	f1 = file_root + 'sprites/enemies/' + files
	if os.path.isfile(f1):
		f2 = 'sprites/enemies', [f1]
		DATA_FILES.append(f2)

for files in os.listdir(file_root + 'sprites/friendlies/'):
	f1 = file_root + 'sprites/friendlies/' + files
	if os.path.isfile(f1):
		f2 = 'sprites/friendlies', [f1]
		DATA_FILES.append(f2)

for files in os.listdir(file_root + 'sprites/player/'):
	f1 = file_root + 'sprites/player/' + files
	if os.path.isfile(f1):
		f2 = 'sprites/player', [f1]
		DATA_FILES.append(f2)

for files in os.listdir(file_root + 'sounds/'):
	f1 = file_root + 'sounds/' + files
	if os.path.isfile(f1):
		f2 = 'sounds', [f1]
		DATA_FILES.append(f2)

for files in os.listdir(file_root + 'fonts/'):
	f1 = file_root + 'fonts/' + files
	if os.path.isfile(f1):
		f2 = 'fonts', [f1]
		DATA_FILES.append(f2)

DATA_FILES.append(file_root + "preferences.txt")

setup(
	options = {'py2exe': {'bundle_files': 1}},
	windows = [{'script': "NeonSpores.py"}],
	zipfile = None,
	data_files = DATA_FILES
)
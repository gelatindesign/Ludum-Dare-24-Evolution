from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

file_root = "G:\\Code\\Local\\Ludum-Dare-24-Evolution\\"

filesb = []
for files in os.listdir(file_root + 'sprites\\'):
	f1 = file_root + 'sprites\\' + files
	if os.path.isfile(f1):
		f2 = 'sprites', [f1]
		filesb.append(f2)

for files in os.listdir(file_root + 'sounds\\'):
	f1 = file_root + 'sounds\\' + files
	if os.path.isfile(f1):
		f2 = 'sounds', [f1]
		filesb.append(f2)

filesb.append(file_root + "preferences.txt")
filesb.append(file_root + "icon.png")

setup(
	options = {'py2exe': {'bundle_files': 1}},
	windows = [{'script': "main.py"}],
	zipfile = None,
	data_files = filesb
)
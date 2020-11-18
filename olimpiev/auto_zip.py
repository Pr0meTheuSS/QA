import sys
import os

dir_name = 'selenium'
filename_with_version = 'gradle.properties'
str_with_version_for_parse = 'pkg.version='

if len(sys.argv) == 2 and sys.argv[1] == '--help':
	print('Script for archiving a folder indicating the version of the package.\n') 
	print('By default, the version is read from a file gradle.properties,\n')
	print('a folder named selenium is archived \n')
	print('(the file and folder must be in the same directory with the script).\n')
	print('The script accepts two values as command line arguments - \n')
	print('the name of the archive folder and the name of the version file.c\n')
	print('example : python3.8 auto_zip.py name_folder file_with_version\n')
	os.exit()

if len(sys.argv) == 3:
	dir_name = sys.argv[1]
	filename_with_version = sys.argv[2]
	
try:
	file_with_version = open(filename_with_version, 'r')
except:
	print('Cannot open this file, sorry...')
	os.exit()
	
version_str = ""

for line in file_with_version:
	if line.find(str_with_version_for_parse, 0) != -1:
		version_str = line.replace(str_with_version_for_parse, '')

file_with_version.close()

version_str = version_str.rstrip('\n')

os.system('zip -r -0' + ' ' + dir_name + '_' + version_str + '.zip' + ' ' + dir_name + '/' + '*')


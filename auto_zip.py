import sys
import os

dir_name = 'selenium'
filename_with_version = 'gradle.properties'

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
	
version_list = []

while True:
	letter  = file_with_version.read(1)
	if letter != '\n' and letter != '\r' and letter != '\0':
		version_list.append(letter)
	else:
		break
file_with_version.close()

os.system('zip -r -0' + ' ' + dir_name + ''.join(version_list) + '.zip' + ' ' + dir_name + '/' + '*')


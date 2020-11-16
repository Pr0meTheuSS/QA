import sys
import os
dir_name = 'selenium'
filename_with_version = 'properties'

if len(sys.argv) == 2 and sys.argv[1] == '--help':
	print('Documentation')

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


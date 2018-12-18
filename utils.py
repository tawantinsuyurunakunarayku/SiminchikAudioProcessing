# -*- coding: utf-8 -*- 
import os
import os.path as path

def get_name_with_ext_file(file):
	return os.path.basename(file)

def get_name_without_ext_file(file):
	return os.path.splitext(os.path.basename(file))[0]

def get_path(file):
	return os.path.dirname(os.path.abspath(file))+"/"

def create_audio_folder(path,name):
	if os.path.isdir(path+name) == False:
		os.system("mkdir "+path+name)
	return path+name+"/"

def delete_files(files):
	for file in files:
		os.remove(file)

def delete_file(file):
	os.remove(file)


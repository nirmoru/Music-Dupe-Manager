import hashlib
import audio_metadata as am
import pathlib
import os
import json


def hash_gen(x: str) -> str:										# generate sha256sum
	sha255_hash = hashlib.sha256()
	with open(x, "rb") as f:
		for byte_block in iter(lambda: f.read(4096), b""):
			sha255_hash.update(byte_block)
		return sha255_hash.hexdigest()


def metadata_extract(x: str) -> dict:
	metadata = am.load(x)											# loading metadata
	tag_dict = {}
	for i in metadata.tags:
		if ' ' in i:
			print(f"{x} | {i} | Contains Whitespace")
		else:
			tags = eval(f'metadata.tags.{i}')
			tag_dict[i] = tags[0]
	
	tag_dict['sha256sum'] = hash_gen(x)
	
	return tag_dict
	

def list_files(directory: str) -> list:								# create list of files
	file_list = []
	for file in pathlib.Path(directory).glob('**/*'):
		if file.is_file():
			file_list.append(file.absolute())
	
	return file_list


def mkdir() -> None:												# create directories
	init_dir = os.getcwd()
	try:
		os.mkdir("output")
	except FileExistsError:
		pass
	output_dir = os.path.join(init_dir, "output")
	os.chdir(output_dir)
	folder_var_name = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
	for i in folder_var_name:
		os.mkdir(i)
		os.chdir(i)
		for j in folder_var_name:
			os.mkdir(i + j)
		os.chdir(output_dir)
	
	os.chdir(init_dir)
	return None


def create_json() -> None:
	with open("tempStorage.json", "w") as f:
		data = {"tags": []}
		json.dump(data, f, indent=4)
	
	return None


def read_json(jsonFile="tempStorage.json") -> dict:
	with open(jsonFile, "r") as f:
		f_load = json.load(f)
		return f_load


def write_json(file) -> None:
	try:
		with open("tempStorage.json", 'r') as file1:
			f_read = json.load(file1)
		with open("tempStorage.json", "w") as f:
			json.dump(append_dict(f_read, metadata_extract(file)), f, indent=4)
	except FileNotFoundError:
		create_json()
	
	return None


def append_dict(prevData, newData) -> dict:
	prev_keys = prevData["tags"]
	prev_keys.append(newData)
	return prevData

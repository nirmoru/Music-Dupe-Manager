import hashlib
import audio_metadata as am
import pathlib
import os
import json
import re


def hash_gen(x: str) -> str:										# generate sha256sum
	sha255_hash = hashlib.sha256()
	with open(x, "rb") as f:
		for byte_block in iter(lambda: f.read(4096), b""):
			sha255_hash.update(byte_block)
		return sha255_hash.hexdigest()


def metadata_extract(x: str) -> dict:											# loading metadata
	metadata = am.load(x)
	tag_dict = {}
	ext_regex = r'(mp3|flac|aiff|wav|ogg|opus)'
	if os.name == 'posix':
		file_name = x.split('/')[-1]
		ext = re.findall(ext_regex, file_name)[0]
	elif os.name == 'nt':
		file_name = x.split('\\')[-1]
		ext = re.findall(ext_regex,file_name)[0]
	else:
		print("Comment out line from 19 to 29")
	tag_dict['File Name'] = file_name
	tag_dict['extension'] = ext
	tag_list = ['tracknumber', 'artist', 'title', 'album', 'date', 'genre', 'albumartist']
	for tag in tag_list:
		try:
			tags = eval(f'metadata.tags.{tag}')
			if tag == "date":
				regex = r"\d{4}"
				match = re.findall(regex, tags[0])
				try:
					tag_dict[tag.capitalize()] = match[0]
				except IndexError:
					tag_dict[tag.capitalize()] = tags[0]
			else:
				tag_dict[tag.capitalize()] = tags[0]
		except AttributeError:
			error = f"{tag} doesn't exist for {x}"
			print(error)
			store_logs(error)
		
	tag_dict['sha256sum'] = hash_gen(x)
	
	return tag_dict
	

def list_files(directory: str) -> list:								# create list of files
	file_list = []
	for file in pathlib.Path(directory).glob('**/*.mp3'):
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


def read_json(jsonfile="tempStorage.json") -> dict:
	with open(jsonfile, "r") as f:
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


def append_dict(prev_data, new_data) -> dict:
	prev_keys = prev_data["tags"]
	prev_keys.append(new_data)
	return prev_data


def store_logs(logs, logfile='tempfile.txt'):
	try:
		with open(logfile, 'a') as f:
			f.write(f'{logs}\n')
	except FileNotFoundError:
		with open(logfile, 'w') as f:
			f.write(f'{logs}\n')

	return None


def export_metadata(directory) -> None:
	files_list = list_files(directory)
	for i in files_list:
		write_json(i)
	
	return None

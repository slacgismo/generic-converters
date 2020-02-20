import json
import os
import sys
import getopt
import glob


def clock_glm(data, filename_out):
	header_str = '\n' + 'clock {'
	tmzone_str = '\n' + '\t' + 'timezone ' + data['globals']['timezone_locale']['value'] + ';'
	start_str = '\n' + '\t' + 'starttime' + ' \"' + data['globals']['starttime']['value'] + '\";'
	stop_str = '\n' + '\t' + 'stoptime' + ' \"' + data['globals']['stoptime']['value'] + '\";'
	end_str = '\n' + '}'
	with open(filename_out, "a") as fw:
		fw.write('\n // CLOCK')
		fw.write(header_str)
		fw.write(tmzone_str)
		fw.write(start_str)
		fw.write(stop_str)
		fw.write(end_str)
	return data, filename_out


def classes_glm(data, filename_out):
	with open(filename_out, "a") as fw:
		fw.write('\n // CLASSES')
		for p_id, p_info in data['classes'].items():
			header_str = ''
			val_str = ''
			for v_id, v_info in data['classes'][p_id].items():
				if 'flags' in v_info and 'EXTENDED' in v_info['flags']:
					header_str = '\n' + 'class ' + p_id + ' {'
					val_str = val_str + "\n" + "\t" + v_info['type'] + " " + v_id + ';'
			if header_str:
				fw.write(header_str)
				fw.write(val_str)
				fw.write("\n}")
	return data, filename_out


def globals_glm(data, filename_out):
	with open(filename_out, "a") as fw:
		fw.write('\n // GLOBALS')
		for p_id, p_info in data['globals'].items():
			if p_info['access'] == "PUBLIC" and p_info['value'] and 'infourl' not in p_id and "::" not in p_id:
				ifndef_str = '\n' + '#ifndef ' + p_id
				if 'int' in p_info['type'] or 'double' in p_info['type'] or 'bool' in p_info['type'] or \
				'enumeration' in p_info['type'] or p_info['value'] == 'NONE' or 'set' in p_info['type'] \
				or 'complex' in p_info['type']:
					tmp_str = '\n' + 'global ' + p_info['type'] + ' ' + p_id + ' ' + p_info['value'] + ';'
					set_str = '\n' + '#set ' + p_id + '=' + p_info['value']
				else:
					tmp_str = '\n' + 'global ' + p_info['type'] + ' ' + p_id + ' \"' + p_info['value'] + '\";'
					set_str = '\n' + '#set ' + p_id + '=\"' + p_info['value'] + '\"'
				else_str = '\n' + '#else'
				endif_str = '\n' + '#endif //' + p_id
				fw.write(ifndef_str)
				fw.write(tmp_str+else_str+set_str)
				fw.write(endif_str)
			else:
				val_str = '\n' + '// ' + p_id + ' is set to ' + p_info['value']
				fw.write(val_str)
	return data, filename_out


def modules_glm(data, filename_out):
	with open(filename_out, "a") as fw:
		fw.write('\n // MODULES')
		for p_id, p_info in data['modules'].items():
			tmp_str = '\n' + 'module ' + p_id + '{'
			fw.write(tmp_str)
			for f_id, f_info in data['globals'].items():
				if p_id in f_id and '::' in f_id and f_info['access'] == "PUBLIC" and f_info['value']:
					mod_var = f_id.split('::')
					val_str = '\n\t' + mod_var[1] + ' ' + f_info['value'] + ';'
					fw.write(val_str)
			fw.write('\n}')
	return data, filename_out


def objects_glm(data, filename_out):
	obj_id = []
	with open(filename_out, "a") as fw:
		fw.write('\n // OBJECTS')
		for p_id, p_info in data['objects'].items():
			obj_id.append([int(p_info['id']),p_id])
			obj_id_sorted = sorted(obj_id, key=lambda tup: tup[0])
			id_list,ordered_obj_list= zip(*obj_id_sorted)
		try:
			for obj_id_sorted in ordered_obj_list:
				header_str = '\n' + 'object ' + data['objects'][obj_id_sorted]["class"] + '{'
				fw.write(header_str)
				if ':' in obj_id_sorted:
					new_name = data['objects'][obj_id_sorted]['class']+'_'+data['objects'][obj_id_sorted]['id']
				else:
					new_name = obj_id_sorted
				name_str = '\n' + '\t' + "name \"" + new_name + '\";'
				fw.write(name_str)
				for v_id, v_info in data['objects'][obj_id_sorted].items():
					if v_id not in objects_ignore and v_info:
						if "\n" in v_info:
							val_str = "\n"+ "\t" + v_id+ " " + '\"\"\"' + v_info.replace('"', '\\\"') + '\"\"\";'
						else:
							val_str = "\n"+"\t" + v_id + " " + "\"" + v_info.replace('"', '\\\"') + "\";"
						fw.write(val_str)
				fw.write('\n}' )
		except NameError:
			return data, filename_out
	return data, filename_out


def schedules_glm(data, filename_out):
	with open(filename_out, "a") as fw:
		fw.write('\n // SCHEDULES')
		for p_id, p_info in data['schedules'].items():
			header_str = '\n' + 'schedule ' + p_id + '{'
			fw.write(header_str)
			fw.write(p_info)
			fw.write('\n}')
	return data, filename_out


def json2glm(file_in):
	filename_in = file_in[0]
	filename_out = filename_in.replace("json", "glm")

	if os.path.exists(filename_out):
		os.remove(filename_out)
	data = {}
	objects_ignore = ["id", "class", "rank", "clock", "schedule_skew", \
	"rng_state", "heartbeat", "guid", "flags"]
	globals_ignore = ['clock', 'timezone_locale', 'starttime', 'stoptime', 'glm_save_options']
	classkeys_ignore = ['object_size', 'trl', 'profiler.numobjs', 'profiler.clocks', 'profiler.count', 'parent']

	with open(filename_in, 'r') as fr:
		data = json.load(fr)
		assert(data['application'] == 'gridlabd')
		assert(data['version'] >= '4.0.0')


	with open(filename_out, "a") as fw:
		fw.write("// JSON to GLM Converter Output")
	data, filename_out = clock_glm(data, filename_out)
	data, filename_out = modules_glm(data, filename_out)
	data, filename_out = globals_glm(data, filename_out)
	data, filename_out = classes_glm(data, filename_out)

	data, filename_out = schedules_glm(data, filename_out)
	data, filename_out = objects_glm(data, filename_out)

	fw.close()

import json
import os
import sys, getopt
import hashlib
import importlib, copy
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


def find(objects,property,value):
	result = []
	for name,values in objects.items():
		if property in values.keys() and values[property] == value:
			result.append(name)
	return result


def get_string(values,prop):
	return values[prop]


def get_complex(values,prop):
	return complex(get_string(values,prop).split(" ")[0].replace('i','j'))


def get_real(values,prop):
	return get_complex(values,prop).real


def get_voltages(values):
	ph = get_string(values,"phases")
	vn = abs(get_complex(values,"nominal_voltage"))
	va = abs(get_complex(values,"voltage_A"))/vn
	vb = abs(get_complex(values,"voltage_B"))/vn
	vc = abs(get_complex(values,"voltage_C"))/vn
	return ph,vn,va,vb,vc


def profile(objects,root,pos=0):
	fromdata = objects[root]
	ph0,vn0,va0,vb0,vc0 = get_voltages(fromdata)

	count = 0
	for link in find(objects,"from",root):
		linkdata = objects[link]
		linktype = "-"
		if "length" in linkdata.keys():
			linklen = get_real(linkdata,"length")/5280
		else:
			linklen = 0.0
		if not "line" in get_string(linkdata,"class"):
			linktype = "--o"
		if "to" in linkdata.keys():
			to = linkdata["to"]
			todata = objects[to]
			ph1,vn1,va1,vb1,vc1 = get_voltages(todata)
			profile(objects,to,pos+linklen)
			count += 1
			if "A" in ph0 and "A" in ph1: plt.plot([pos,pos+linklen],[va0,va1],"%sk"%linktype)
			if "B" in ph0 and "B" in ph1: plt.plot([pos,pos+linklen],[vb0,vb1],"%sr"%linktype)
			if "C" in ph0 and "C" in ph1: plt.plot([pos,pos+linklen],[vc0,vc1],"%sb"%linktype)
			if limit:
				if va1>1+limit or vb1>1+limit or vc1>1+limit :
					print("json2png.py WARNING: node %s voltage is high (%g, %g, %g), phases = '%s', nominal voltage=%g" % (to,va1*vn1,vb1*vn1,vc1*vn1,ph1,vn1));
				if (va1>0 and va1<1-limit) or (vb1>0 and vb1<1-limit) or (vc1>0 and vc1<1-limit) :
					print("json2png.py WARNING: node %s voltage is low (%g, %g, %g), phases = '%s', nominal voltage=%g" % (to,va1*vn1,vb1*vn1,vc1*vn1,ph1,vn1));
	if count > 1 and with_nodes:
		plt.plot([pos,pos,pos],[va0,vb0,vc0],':*',color='grey',linewidth=1)
		plt.text(pos,min([va0,vb0,vc0]),"[%s]  "%root,color='grey',size=6,rotation=90,verticalalignment='top',horizontalalignment='center')


def json2png(kwargs):
	file_in = kwargs["file_in"]
	size = kwargs["size"]
	output_type = kwargs["output_type"]
	resolution = kwargs["resolution"]
	limit = kwargs["limit"]
	with_nodes = kwargs["with_nodes"]
	filename_json = file_in[0]
	filename_png = filename_json.replace("json", "png")
	basename = ''

	with open(filename_json,"r") as f :
		data = json.load(f)
		assert(data['application']=='gridlabd')
		assert(data['version'] >= '4.2.0')

	if output_type == 'summary':
		filename = data["globals"]["modelname"]["value"]
		sz = size.split("x")
		sx = int(sz[0])
		sy = int(sz[1])
		img = Image.new(mode="RGB",size=(sx,sy),color="white")
		draw = ImageDraw.Draw(img)

		def node(draw,x,y,text,vmargin=1,hmargin=1,fnt=ImageFont.load_default()):
			sz = draw.multiline_textsize(text,font=fnt)
			draw.rectangle([x-sz[0]/2-hmargin,y-sz[1]/2-vmargin,x+sz[0]/2+hmargin,y+sz[1]/2+vmargin],outline="black",fill="white")
			draw.multiline_text((x-sz[0]/2,y-sz[1]/2),text,font=fnt,fill="black")

		md5 = hashlib.md5()
		with open(filename_json,"r") as f:
			md5.update(f.read().encode())
		node(draw,x=sx/2,y=sy/2,text="""Name..... %s
	Digest... %s
	Date..... %s""" % (filename,md5.hexdigest(),datetime.now().strftime("%y-%m-%d %H:%M:%S")),vmargin=2,hmargin=3)
		img.save(filename_png)

	elif output_type == 'profile':
		plt.figure(1);
		for obj in find(objects=data["objects"],property="bustype",value="SWING"):
			profile(objects=data["objects"],root=obj)
		plt.xlabel('Distance (miles)')
		plt.ylabel('Voltage (pu)')
		plt.title(data["globals"]["modelname"]["value"])
		plt.grid()
		if limit:
			plt.ylim([1-limit,1+limit])
		plt.savefig(filename_png, dpi=int(resolution))
	else:
		modname = sys.argv[0].replace("json2png.py","json2png-%s.py"%output_type)
		if os.path.exists(modname):
			modspec = importlib.util.spec_from_file_location(output_type, modname)
			mod = importlib.import_module("json2png-%s"%output_type)
			argv = copy.deepcopy(sys.argv)
			argv[0] = modname
			mod.main(argv)
		else:
			raise TypeError("type '%s' is not valid" % output_type)

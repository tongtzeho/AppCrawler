# -*- coding:utf-8 -*-

import os, re, hashlib, codecs, zipfile, chardet, shutil

#def decode_apk(market, apkfile):
#	os.system("apktool d -f "+apkfile+" > ~"+market+"apktoollog")
#	return apkfile[:-4]

def unzip_apk(apkfile):
	try:
		if apkfile.lower().endswith('.apk'):
			path = apkfile[:-4]
			if not os.path.exists(path):
				os.makedirs(path)			
			file_zip = zipfile.ZipFile(apkfile, 'r')
			for file in file_zip.namelist():
				if re.match("(META-INF\/.+)|(AndroidManifest\.xml)|(resources\.arsc)|(classes[0-9]*\.dex)", file, re.I):
					file_zip.extract(file, path)
			file_zip.close()
			return path
		else:
			return ""
	except:
		return ""

def binxml2strxml(manifest_file):
	try:
		if not os.path.isfile(manifest_file):
			return ""
		os.rename(manifest_file, manifest_file+".xml")
		os.system("java -jar AXMLPrinter2.jar "+manifest_file+".xml > "+manifest_file)
		os.remove(manifest_file+".xml")
		return manifest_file
	except:
		return ""
		
def get_apk_package_name(manifest_file):
	if not os.path.isfile(manifest_file):
		return ""
	try:
		fin = open(manifest_file, 'rb')
		fencoding = chardet.detect(fin.read())
		fin.close()
		fin = codecs.open(manifest_file, "r", fencoding['encoding'])
		data = fin.read()
		fin.close()
		matcher = re.findall("package=\".*?\"", data)
		if len(matcher): return matcher[0].replace("package=\"", "").replace('"', "")
		else: return ""
	except:
		return ""

def get_apk_md5(apkfile):
	try:
		myhash = hashlib.md5()
		f = open(apkfile, 'rb')
		while True:
			b = f.read(8096)
			if not b :
				break
			myhash.update(b)
		f.close()
		return myhash.hexdigest()
	except:
		return ""
		
def get_apk_sha256(apkfile):
	try:
		myhash = hashlib.sha256()
		f = open(apkfile, 'rb')
		while True:
			b = f.read(8096)
			if not b :
				break
			myhash.update(b)
		f.close()
		return myhash.hexdigest()
	except:
		return ""
	
def get_apk_key(market, apkfile, manifest_file):
	if not os.path.isfile(apkfile):
		return ()
	else:
		try:
			package_name = get_apk_package_name(manifest_file)
			if len(package_name):
				md5_str = get_apk_md5(apkfile)
				sha256_str = get_apk_sha256(apkfile)
				if len(md5_str) > 0 and len(sha256_str) > 0:
					return (market, package_name, md5_str, sha256_str)
			return ()
		except:
			return ()
			
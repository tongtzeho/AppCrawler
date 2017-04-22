import os, shutil, zipfile

def zip_dir(dirname, zipfilename):
	filelist = []
	if os.path.isfile(dirname):
		filelist.append(dirname)
	else :
		for root, dirs, files in os.walk(dirname):
			for name in files:
				filelist.append(os.path.join(root, name))
	zf = zipfile.ZipFile(zipfilename, "w", zipfile.ZIP_DEFLATED)
	for eachfile in filelist:
		arcname = eachfile[len(dirname):]
		zf.write(eachfile, arcname)
	zf.close()

def upload_local(src_dir, apk_key, apkfile, config):
	try:
		root = config['LOCAL_ROOT']
		if root == None: return False
		market = apk_key[0]
		pkg = apk_key[1]
		md5 = apk_key[2]
		sha256 = apk_key[3]
		if not os.path.isdir(root+'apk/'+market):
			try:
				os.makedirs(root+'apk/'+market)
			except:
				pass
		if not os.path.isdir(root+'apk/'+market+'/'+pkg):
			try:
				os.makedirs(root+'apk/'+market+'/'+pkg)
			except:
				pass
		shutil.move(apkfile, root+'apk/'+market+'/'+pkg+'/'+md5+'-'+sha256+".apk")
		zip_dir(src_dir, src_dir+'.zip')
		if not os.path.isdir(root+'zip/'+market):
			try:
				os.makedirs(root+'zip/'+market)
			except:
				pass
		if not os.path.isdir(root+'zip/'+market+'/'+pkg):
			try:
				os.makedirs(root+'zip/'+market+'/'+pkg)
			except:
				pass
		shutil.move(src_dir+'.zip', root+'zip/'+market+'/'+pkg+'/'+md5+'-'+sha256+".zip")
		return True
	except:
		return False
		
def upload_oss(src_dir, apk_key, apkfile, config):
	try:
		return False
	except:
		return False
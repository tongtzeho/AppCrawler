import os, shutil, zipfile, requests, base64, hashlib

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

def content_md5(file):
	try:
		myhash = hashlib.md5()
		f = open(file, 'rb')
		while True:
			b = f.read(8096)
			if not b :
				break
			myhash.update(b)
		f.close()
		return base64.b64encode(myhash.digest())
	except:
		return ""
		
def upload_oss(src_dir, apk_key, apkfile, config):
	try:
		autho = config['AUTHORIZATION']
		if autho == None: return False
		market = apk_key[0]
		pkg = apk_key[1]
		md5 = apk_key[2]
		sha256 = apk_key[3]
		url = "[aliyun]"+"/"+market+'/'+pkg+'/'+md5+'-'+sha256+".apk"
		files = {'file': open(apkfile, 'rb')}
		headers = {
			'Host': '[apk-bucket]',
			'Cache-control': 'no-cache',
			'Content-Disposition': 'attachment;filename='+pkg+".apk",
			'Content-MD5': content_md5(apkfile),
			'Content-Type': 'application/vnd.android.package-archive',
			'Content-Length': str(os.path.getsize(apkfile)),
			'Authorization': autho
		}
		success = False
		for i in range(10):
			try:
				r = requests.put(url, files=files, timeout=30, headers=headers)
				if r.status_code == 200:
					success = True
					break
				continue
			except:
				continue
		if not success: return False
		url = "[aliyun]"+"/"+market+'/'+pkg+'/'+md5+'-'+sha256+".zip"
		zip_dir(src_dir, src_dir+'.zip')
		files = {'file': open(src_dir+'.zip', 'rb')}
		headers = {
			'Host': '[zip-bucket]',
			'Cache-control': 'no-cache',
			'Content-Disposition': 'attachment;filename='+pkg+".zip",
			'Content-MD5': content_md5(src_dir+'.zip'),
			'Content-Type': 'application/zip',
			'Content-Length': str(os.path.getsize(src_dir+'.zip')),
			'Authorization': autho
		}
		for i in range(10):
			try:
				r = requests.put(url, files=files, timeout=30, headers=headers)
				if r.status_code == 200:
					return True
				continue
			except:
				continue
		return False
	except:
		return False
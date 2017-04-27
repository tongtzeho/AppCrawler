import os, shutil, zipfile, requests, base64, hashlib
import oss2 # Aliyun

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
		key_id = config['ACCESS_KEY_ID']
		key_secret = config['ACCESS_KEY_SECRET']
		endpoint = config['ENDPOINT']
		market = apk_key[0]
		pkg = apk_key[1]
		md5 = apk_key[2]
		sha256 = apk_key[3]
		success = False
		auth = oss2.Auth(key_id, key_secret)
		bucket = oss2.Bucket(auth, endpoint, 'lxapk')
		for i in range(10):
			try:
				r = bucket.put_object_from_file(market+'/'+pkg+'/'+md5+'-'+sha256+".apk", apkfile)
				if r.status == 200:
					success = True
					break
			except:
				continue
		if not success: return False
		zip_dir(src_dir, src_dir+'.zip')
		bucket = oss2.Bucket(auth, endpoint, 'lxzip')
		for i in range(10):
			try:
				r = bucket.put_object_from_file(market+'/'+pkg+'/'+md5+'-'+sha256+".zip", src_dir+'.zip')
				if r.status == 200:
					return True
			except:
				continue
		return False
	except:
		return False
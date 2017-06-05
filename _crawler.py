# -*- coding:utf-8 -*-
# export QT_QPA_PLATFORM=offscreen
# sudo nohup bash _crawler.sh >_crawler.log 2>&1 &
# 安装python3，安装pip3，用pip3安装selenium, google, protobuf，安装phantomjs并设置路径，安装Java，下载AXMLPrinter2.jar放在当前目录中
# 如果在阿里云安装不了Java和phantomjs，输入apt-get update
# 如果使用阿里云，安装oss2, redis

from urllib import request
from selenium import webdriver
import multiprocessing, threading, random, requests, urllib, time, os, codecs, shutil, sys, json, redis

from _downloader import *
from _decoder import *
from _parser import *
from _extender import *
from _checker import *
from _uploader import *

#phantom_js目录

#Windows
#phantomjs_path = 'phantomjs/bin/phantomjs.exe'

#Linux
phantomjs_path = 'phantomjs'

#Header的User Agent
#user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'

url_prefix = {
	'yingyongbao': 'http://sj.qq.com/myapp/detail.htm?apkName=',
	'baidu': 'http://shouji.baidu.com/software/',
	'360': 'http://zhushou.360.cn/detail/index/soft_id/',
	'googleplay': 'https://play.google.com/store/apps/details?id=',
	'huawei': 'http://appstore.huawei.com/app/',
	'xiaomi': 'http://app.mi.com/details?id=',
	'wandoujia': 'http://www.wandoujia.com/apps/',
	'hiapk': 'http://apk.hiapk.com/appinfo/',
	'anzhi': 'http://www.anzhi.com/',
	'91': 'http://apk.91.com/Soft/Android/',
	'oppo': 'http://store.oppomobile.com/product/',
	'pp': 'http://www.25pp.com/android/',
	'sogou': 'http://zhushou.sogou.com/apps/detail/',
	'gfan': 'http://apk.gfan.com/Product/',
	'meizu': 'http://app.meizu.com/apps/public/detail?package_name=',
	'sina': 'http://app.sina.com.cn/appdetail.php?appID=',
	'dcn': 'http://android.d.cn/',
	'liqucn': 'http://os-android.liqucn.com/',
	'appchina': 'http://www.appchina.com/app/',
	'10086': 'http://mm.10086.cn/android/info/',
	'lenovo': 'http://www.lenovomm.com/appdetail/',
	'zol': 'http://sj.zol.com.cn/',
	'nduo': 'http://www.nduo.cn/Home/WebDetail/',
	'cnmo': 'http://app.cnmo.com/android/',
	'pconline': 'http://dl.pconline.com.cn/download/',
	'appcool': 'http://www.mgyapp.com/apps/'
}
	
def open_url(market, url):
	for i in range(10):
		if market == 'googleplay' or market == 'baidu' or market == 'huawei' or market == 'xiaomi' or market == 'wandoujia' or market == '91' or market == 'oppo' or market == 'pp' or market == 'sogou' or market == 'gfan' or market == 'sina' or market == 'liqucn' or market == 'appchina' or market == '10086' or market == 'nduo' or market == 'cnmo' or market == 'appcool':
			try:
				if market == 'xiaomi' and i % 3 == 2: req = request.Request(url+"&type=pad")
				elif market == 'googleplay': req = request.Request(url+"&hl=zh")
				else: req = request.Request(url)
				req.add_header('User-Agent', user_agent)
				web = request.urlopen(req, timeout=30)
				charset = str(web.headers.get_content_charset())
				if charset == "None": charset = "utf-8"
				data = web.read().decode(charset)
			except:
				data = ""
		else:
			try:
				driver = webdriver.PhantomJS(executable_path=phantomjs_path)
				driver.set_page_load_timeout(45)
				driver.get(url)
				time.sleep(0.5)
				data = driver.page_source
				driver.quit()
			except:
				try:
					driver.quit()
				except:
					pass
				data = ""
		info_dict = get_app_basic_info(market, data)
		permission_list = get_app_permission(market, data)
		description = get_app_description(market, data)
		release_note = get_app_release_note(market, data)
		download_link = get_apk_download_link(market, data, url)
		extend_urls = get_extend_urls(market, data, url_prefix[market])
		similar_apps = get_similar_apps(market, data, url_prefix[market])
		icon_link = get_icon_download_link(market, data)
		result = (info_dict, permission_list, description, release_note, download_link, extend_urls, similar_apps, icon_link)
		if check_response(market, result):
			break
		elif page_invalid(market, data) and i >= 3:
			return ()
		else:
			continue
	if market == 'googleplay':
		for i in range(10):
			try:
				req = request.Request(url+"&hl=en")
				req.add_header('User-Agent', user_agent)
				web = request.urlopen(req, timeout=30)
				charset = str(web.headers.get_content_charset())
				if charset == "None": charset = "utf-8"
				data = web.read().decode(charset)
			except:
				data = ""
			info_dict_en = get_app_basic_info(market, data)
			permission_list_en = get_app_permission(market, data)
			description_en = get_app_description(market, data)
			release_note_en = get_app_release_note(market, data)
			resulten = (info_dict_en, permission_list_en, description_en, release_note_en)
			if check_response(market, resulten):
				break
			elif page_invalid(market, data) and i >= 3:
				return ()
			else:
				continue
		result += resulten
	return result

def read_url(root, market):
	result = set()
	if os.path.isfile(root+market+"_~url_list.txt"):
		shutil.move(root+market+"_~url_list.txt", root+market+"_url_list.txt")
	elif os.path.isfile(root+market+"_url_list.txt"):
		pass
	else:
		return result
	fin = codecs.open(root+market+"_url_list.txt", "r", "utf-8")
	for line in fin:
		result.add(line.replace('\r', "").replace('\n', ""))
	fin.close()
	return result
	
def read_log(root, market):
	result = {}
	visit_url = set()
	if os.path.isfile(root+'__log__/'+market+'.log'):
		fin = codecs.open(root+'__log__/'+market+'.log', "r", "utf-8")
		for line in fin:
			line = line.replace("\r", "").replace("\n", "")
			splitspace = line.split(" ")
			if len(splitspace) >= 7 and splitspace[1] == 'success':
				pkgname = splitspace[3]
				md5str = splitspace[4]
				sha256str = splitspace[5]
				if pkgname in result:
					result[pkgname].add(md5str+'-'+sha256str)
				else:
					result[pkgname] = set()
					result[pkgname].add(md5str+'-'+sha256str)
			if len(splitspace) >= 3:
				visit_url.add(splitspace[2])
		fin.close()
		return (result, visit_url)
	else:
		return (result, visit_url)

def read_config():
	result = {}
	result['ANDROID_ID'] = ""
	result['GOOGLE_LOGIN'] = ""
	result['GOOGLE_PASSWORD'] = ""
	result['LOCAL_ROOT'] = None
	result['ACCESS_KEY_ID'] = None
	result['ACCESS_KEY_SECRET'] = None
	result['ENDPOINT'] = None
	result['REDIS_HOST'] = ""
	result['REDIS_PASSWORD'] = ""
	try:
		if os.path.isfile("config.json"):
			with open("config.json") as jsonfile:
				config_dict = json.load(jsonfile)
			for key in result.keys():
				if key in config_dict:
					result[key] = config_dict[key]
			return result
		else:
			return None
	except:
		return None
	
def write_text_information(dir, response):
	fout = codecs.open(dir+"Information.txt", "w", "utf-8")
	for key, value in response[0].items():
		if len(value): fout.write(key+"\n\t"+value+"\n")
	if len(response[6]):
		fout.write("Similar_Apps\n")
		for urls in response[6]:
			fout.write("\t"+urls+"\n")
	fout.close()
	if len(response[1]):
		fout = codecs.open(dir+"Permission.txt", "w", "utf-8")
		for permission in response[1]:
			fout.write(permission+"\n")
		fout.close()
	if len(response[2]):
		fout = codecs.open(dir+"Description.txt", "w", "utf-8")
		fout.write(response[2])
		fout.close()
	if len(response[3]):
		fout = codecs.open(dir+"Release_Note.txt", "w", "utf-8")
		fout.write(response[3])
		fout.close()
	if len(response) == 12:
		fout = codecs.open(dir+"Information(eng).txt", "w", "utf-8")
		for key, value in response[8].items():
			if len(value): fout.write(key+"\n\t"+value+"\n")
		if len(response[6]):
			fout.write("Similar_Apps\n")
			for urls in response[6]:
				fout.write("\t"+urls+"\n")
		fout.close()
		if len(response[9]):
			fout = codecs.open(dir+"Permission(eng).txt", "w", "utf-8")
			for permission in response[9]:
				fout.write(permission+"\n")
			fout.close()
		if len(response[10]):
			fout = codecs.open(dir+"Description(eng).txt", "w", "utf-8")
			fout.write(response[10])
			fout.close()
		if len(response[11]):
			fout = codecs.open(dir+"Release_Note(eng).txt", "w", "utf-8")
			fout.write(response[11])
			fout.close()
	
def main_loop(threadidstr, market, root, thread_num, rate_per_iteration, lock_pool, name_pool, lock_set, url_set, lock_log, need_extend, set_maxsize, config, lock_dict, app_dict, visit_url):
	iteration = 0
	update = 0
	hold_lock_pool = False
	hold_lock_set = False
	hold_lock_log = False
	hold_lock_dict = False
	while len(url_set):
		iteration += 1
		lock_set.acquire()
		hold_lock_set = True
		url_list = list(url_set)
		lock_set.release()
		hold_lock_set = False
		random.shuffle(url_list)
		for short_url in url_list:
			try:
				if update >= thread_num*10:
					update = 0
					lock_set.acquire()
					hold_lock_set = True
					os.rename(root+market+"_url_list.txt", root+market+"_~url_list.txt")
					fout = codecs.open(root+market+"_url_list.txt", "w", "utf-8")
					for temp_url in url_set:
						fout.write(temp_url+"\n")
					fout.close()
					os.remove(root+market+"_~url_list.txt")
					lock_set.release()
					hold_lock_set = False
					print (market+threadidstr+"：更新链接列表")
				skip = False
				lock_dict.acquire()
				hold_lock_dict = True
				if short_url in visit_url:
					if random.random() >= rate_per_iteration:
						skip = True
				lock_dict.release()
				hold_lock_dict = False
				if skip:
					continue
				try:
					if os.path.exists("~"+market+"tmp"+threadidstr): shutil.rmtree("~"+market+"tmp"+threadidstr, ignore_errors=True)
					if os.path.isfile("~"+market+"tmp"+threadidstr+".apk"): os.remove("~"+market+"tmp"+threadidstr+".apk")
					if os.path.isfile("~"+market+"tmp"+threadidstr+".zip"): os.remove("~"+market+"tmp"+threadidstr+".zip")
					if os.path.isfile("~"+market+"tmp"+threadidstr+".png"): os.remove("~"+market+"tmp"+threadidstr+".png")
					if os.path.isfile("~"+market+"tmp"+threadidstr+".webp"): os.remove("~"+market+"tmp"+threadidstr+".webp")
				except:
					pass
				if os.path.isfile('exit'):
					print (market+threadidstr+"：结束")
					return
				url = url_prefix[market]+short_url
				print (market+threadidstr+"：开始连接（"+url+"）")
				response = open_url(market, url)
				if not len(response):
					print (market+threadidstr+"：无效的链接（"+url+"）")
					lock_set.acquire()
					hold_lock_set = True
					url_set.discard(short_url)
					lock_set.release()
					hold_lock_set = False
					update += 1
					lock_log.acquire()
					hold_lock_log = True
					cur_time = str(int(time.time()))
					flog = open(root+'__log__/'+market+'.log', 'a')
					flog.write(cur_time+' invalid '+short_url+'\n')
					flog.close()
					lock_log.release()
					hold_lock_log = False
					lock_dict.acquire()
					hold_lock_dict = True
					visit_url.add(short_url)
					lock_dict.release()
					hold_lock_dict = False
					continue
				if not len(response[0]):
					print (market+threadidstr+"：访问链接失败（"+url+"）")
					time.sleep(1)
					continue
				print (market+threadidstr+"：准备下载APK（"+response[4]+"）")
				if os.path.isfile('exit'):
					print (market+threadidstr+"：结束")
					return				
				if not download_apk(market, response[4], "~"+market+"tmp"+threadidstr+".apk", config):
					print (market+threadidstr+"：下载APK失败（"+url+"）")
					continue
				extract_dir = unzip_apk("~"+market+"tmp"+threadidstr+".apk")
				if len(extract_dir):
					manifest_file = binxml2strxml(extract_dir+"/AndroidManifest.xml")
					if len(manifest_file):
						apk_key = get_apk_key(market, "~"+market+"tmp"+threadidstr+".apk", manifest_file)
						bytestr = str(os.path.getsize("~"+market+"tmp"+threadidstr+".apk"))
						if len(apk_key) == 4:					
							lock_pool.acquire()
							hold_lock_pool = True
							if apk_key[1] in name_pool:
								lock_pool.release()
								hold_lock_pool = False
								continue
							else:
								name_pool.add(apk_key[1])
								lock_pool.release()
								hold_lock_pool = False
							exist_pkg = False
							exist_md5sha256 = False
							lock_dict.acquire()
							hold_lock_dict = True
							visit_url.add(short_url)
							if apk_key[1] in app_dict:
								exist_pkg = True
								if apk_key[2]+'-'+apk_key[3] in app_dict[apk_key[1]]:
									exist_md5sha256 = True
								else:
									app_dict[apk_key[1]].add(apk_key[2]+'-'+apk_key[3])
							else:
								app_dict[apk_key[1]] = set()
								app_dict[apk_key[1]].add(apk_key[2]+'-'+apk_key[3])
							lock_dict.release()
							hold_lock_dict = False
							if not os.path.exists(root+market+"/"+apk_key[1]): os.makedirs(root+market+"/"+apk_key[1])
							if exist_pkg:
								if not exist_md5sha256: state = 1 # 之前有这个应用，但是没有这个版本
								else: state = 2 # 之前有这个应用，也有这个版本
							else: state = 3 # 之前没有这个应用
							if state == 1 or state == 3:
								download_icon(market, response[7], "~"+market+"tmp"+threadidstr+".png")
								cur_time = str(int(time.time()))
								fout = codecs.open(extract_dir+"/Index.txt", "w", "utf-8")
								fout.write("Market\n\t"+apk_key[0]+"\nPackage_Name\n\t"+apk_key[1]+"\nMD5\n\t"+apk_key[2]+"\nSHA256\n\t"+apk_key[3]+"\nTime\n\t"+cur_time+"\nLink\n\t"+url+"\nDownload_Link\n\t"+response[4]+"\n")
								fout.close()
								if os.path.isfile("~"+market+"tmp"+threadidstr+".png"):
									if market != 'googleplay': shutil.move("~"+market+"tmp"+threadidstr+".png", extract_dir+"/icon.png")
									else: shutil.move("~"+market+"tmp"+threadidstr+".png", extract_dir+"/icon.webp")
								if not upload_oss(extract_dir, apk_key, "~"+market+"tmp"+threadidstr+".apk", config):
									state = -1
							else:
								cur_time = str(int(time.time()))
							if state != -1:
								if not os.path.exists(root+market+"/"+apk_key[1]+"/["+cur_time+"]"):
									os.makedirs(root+market+"/"+apk_key[1]+"/["+cur_time+"]")
								lock_log.acquire()
								hold_lock_log = True
								flog = codecs.open(root+'__log__/'+market+'.log', 'a', 'utf-8')
								flog.write(cur_time+' success '+short_url+' '+apk_key[1]+' '+apk_key[2]+' '+apk_key[3]+' '+bytestr+' '+response[4].replace(' ', '%20')+'\n')
								flog.close()
								lock_log.release()
								hold_lock_log = False
								if not os.path.isfile(root+market+"/"+apk_key[1]+"/["+cur_time+"]/end"):
									write_text_information(root+market+"/"+apk_key[1]+"/["+cur_time+"]/", response)
									fout = codecs.open(root+market+"/"+apk_key[1]+"/["+cur_time+"]/Index.txt", "w", "utf-8")
									fout.write("Market\n\t"+apk_key[0]+"\nPackage_Name\n\t"+apk_key[1]+"\nMD5\n\t"+apk_key[2]+"\nSHA256\n\t"+apk_key[3]+"\nTime\n\t"+cur_time+"\nLink\n\t"+url+"\nDownload_Link\n\t"+response[4]+"\n")
									fout.close()
									open(root+market+"/"+apk_key[1]+"/["+cur_time+"]/end", "w").close()								
								if state == 1: print (apk_key[0]+threadidstr+"：更新"+apk_key[1]+"版本和信息")
								elif state == 2: print (apk_key[0]+threadidstr+"：更新"+apk_key[1]+"信息。无版本更新")
								elif state == 3: print (apk_key[0]+threadidstr+"：新增"+apk_key[1])
								try:
									conn = redis.StrictRedis(host=config['REDIS_HOST'], password=config['REDIS_PASSWORD'])
									state_str = {1: "UpdateVersion", 2: "UpdateMetadata", 3: "New"}
									conn.lpush("apk_queue", state_str[state]+" "+market+" "+apk_key[1]+" "+apk_key[2]+" "+apk_key[3])
								except:
									print (apk_key[0]+threadidstr+"：消息队列错误"+apk_key[1])
							else:
								print (apk_key[0]+threadidstr+"：上传失败"+apk_key[1])
							lock_pool.acquire()
							hold_lock_pool = True
							name_pool.remove(apk_key[1])
							lock_pool.release()
							hold_lock_pool = False
							if need_extend:	
								lock_set.acquire()
								hold_lock_set = True
								for extend_url in response[5]:
									if len(url_set) >= set_maxsize: break
									url_set.add(extend_url)
								lock_set.release()
								hold_lock_set = False
							update += 1
						else:
							print (market+threadidstr+"：解析XML失败（"+url+"）")
					else:
						print (market+threadidstr+"：读取二进制XML失败（"+url+"）")
				else:
					print (market+threadidstr+"：解压缩APK失败（"+url+"）")
			except:
				print (market+threadidstr+"：未知错误（"+url+"）")
				if hold_lock_pool: lock_pool.release()
				if hold_lock_set: lock_set.release()
				if hold_lock_log: lock_log.release()
				if hold_lock_dict: lock_dict.release()
				hold_lock_pool = False
				hold_lock_set = False
				hold_lock_log = False
				hold_lock_dict = False

def initialization(param):
	market = param[0]
	root = param[1]
	if len(root) > 0 and not os.path.exists(root): return
	if not os.path.exists(root+"__log__"):
		try:
			os.makedirs(root+"__log__")
		except:
			pass
	thread_num = param[2]
	rate_per_iteration = param[3]
	need_extend = param[4]
	set_maxsize = param[5]
	print ("初始化进程：("+market+", "+str(thread_num)+", "+str(rate_per_iteration)+")")
	lock_pool = threading.Lock()
	name_pool = set()
	lock_set = threading.Lock()
	url_set = read_url(root, market)
	app_dict, visit_url = read_log(root, market)
	lock_log = threading.Lock()
	lock_dict = threading.Lock()
	config = read_config()
	if config == None:
		print ("进程"+market+"退出：Config错误")
		return
	if not os.path.exists(root+market): os.makedirs(root+market)
	threads = []
	for i in range(1, thread_num):
		threads.append(threading.Thread(target=main_loop, args=(str(i), market, root, thread_num, rate_per_iteration, lock_pool, name_pool, lock_set, url_set, lock_log, need_extend, set_maxsize, config, lock_dict, app_dict, visit_url)))
	for t in threads:
		t.start()
	main_loop('0', market, root, thread_num, rate_per_iteration, lock_pool, name_pool, lock_set, url_set, lock_log, need_extend, set_maxsize, config, lock_dict, app_dict, visit_url)
	for t in threads:
		t.join()
	print ("进程"+market+"退出")
	
if __name__ == '__main__':
	if not os.path.isfile(phantomjs_path) or not os.path.isfile("settings.txt"): exit()
	if os.path.isfile('exit'): os.remove('exit')
	fin_settings = open("settings.txt", "r")
	param_list = []
	market_set = set()
	for line in fin_settings:
		if line.startswith('#') or len(line.split(" ")) < 4: continue
		market = line.split(" ")[0].lower()
		root = line.split(" ")[1][:]
		thread_num = int(line.split(" ")[2])
		rate_per_iteration = float(line.split(" ")[3])
		if len(line.split(" ")) <= 4 or int(line.split(" ")[4]) <= 0:
			need_extend = False
			set_maxsize = 0
		else:
			need_extend = True
			set_maxsize = int(line.split(" ")[4])
		if market in market_set: exit()
		if thread_num <= 0 or thread_num > 50: exit()
		if rate_per_iteration <= 0 or rate_per_iteration > 1: exit()
		param_list.append((market, root, thread_num, rate_per_iteration, need_extend, set_maxsize))
		market_set.add(market)
	fin_settings.close()
	processes = []
	for param in param_list:
		if param == param_list[0]: continue
		processes.append(multiprocessing.Process(target = initialization, args = (param,)))
	for p in processes:
		p.start()
	initialization(param_list[0])
	for p in processes:
		p.join()
	print ("正常退出")

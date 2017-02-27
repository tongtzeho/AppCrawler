# -*- coding:utf-8 -*-

# 需要安装chardet, selenium, google, protobuf，安装phantomjs并设置路径，下载AXMLPrinter2.jar放在当前目录中

from urllib import request
from selenium import webdriver
import multiprocessing, threading, random, requests, urllib, time, os, codecs, shutil, sys

from _downloader import *
from _decoder import *
from _parser import *
from _extender import *
from _checker import *

#phantom_js目录

#Windows
#phantomjs_path = 'phantomjs/bin/phantomjs.exe'
#root = 'E:/Android/'

#Linux
phantomjs_path = '/usr/bin/phantomjs'
root = '../Android/'

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
	'pp': 'http://www.25pp.com/android/'
}
	
def open_url(market, url):
	for i in range(10):
		if market == 'baidu' or market == 'huawei' or market == 'xiaomi' or market == 'wandoujia' or market == '91' or market == 'oppo' or market == 'pp':
			try:
				if market == 'xiaomi' and i % 3 == 2: req = request.Request(url+"&type=pad")
				else: req = request.Request(url)
				req.add_header('User-Agent', user_agent);
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
				if market == 'googleplay':
					driver.get(url+"&hl=zh")
					try:
						driver.find_element_by_xpath("//button[@class='content id-view-permissions-details fake-link']").click()
						time.sleep(3)
					except:
						pass
				else:
					driver.get(url)
					time.sleep(0.5)
				data = driver.page_source
				driver.quit()
			except:
				data = ""
				driver.quit()
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
				driver = webdriver.PhantomJS(executable_path=phantomjs_path)
				driver.set_page_load_timeout(45)
				driver.get(url+"&hl=en")
				try:
					driver.find_element_by_xpath("//button[@class='content id-view-permissions-details fake-link']").click()
					time.sleep(3)
				except:
					pass
				data = driver.page_source
				driver.quit()
			except:
				data = ""
				driver.quit()
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

def read_url(market):
	result = set()
	if os.path.isfile(root+market+"_~url_list.txt"):
		shutil.move(root+market+"_~url_list.txt", root+market+"_url_list.txt")
	elif os.path.isfile(root+market+"_url_list.txt"):
		pass
	else:
		return result
	fin = open(root+market+"_url_list.txt", "r")
	for line in fin:
		result.add(line.replace('\r', "").replace('\n', ""))
	fin.close()
	return result

def read_config():
	result = {}
	if os.path.isfile("config.txt"):
		fin = open("config.txt", "r")
		data = fin.read().replace("\r", "").split("\n")
		result['ANDROID_ID'] = data[0]
		result['GOOGLE_LOGIN'] = data[1]
		result['GOOGLE_PASSWORD'] = data[2]
	return result
	
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
	
def main_loop(threadidstr, market, thread_num, rate_per_iteration, lock_pool, name_pool, lock_set, url_set, lock_log, need_extend, set_maxsize, config):
	iteration = 0
	update = 0
	hold_lock_pool = False
	hold_lock_set = False
	hold_lock_log = False
	while len(url_set):
		iteration += 1
		lock_set.acquire()
		hold_lock_set = True
		url_list = random.sample(url_set, (int)(len(url_set)*rate_per_iteration))
		lock_set.release()
		hold_lock_set = False
		random.shuffle(url_list)
		for short_url in url_list:
			try:
				if update >= thread_num*5:
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
				if os.path.exists("~"+market+"tmp"+threadidstr): shutil.rmtree("~"+market+"tmp"+threadidstr, ignore_errors=True)				
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
					continue
				if not len(response[0]):
					print (market+threadidstr+"：访问链接失败（"+url+"）")
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
						if len(apk_key) == 3:					
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
							if os.path.exists(root+market+"/"+apk_key[1]):
								if not os.path.exists(root+market+"/"+apk_key[1]+"/{"+apk_key[2]+"}"): # 之前有这个应用，但是没有这个版本
									state = 1 
								else: # 之前有这个应用，也有这个版本
									state = 2 
									if not os.path.isfile(root+market+"/"+apk_key[1]+"/{"+apk_key[2]+"}/end"): # 之前这个版本的应用信息不完整，相当于没有
										shutil.rmtree(root+market+"/"+apk_key[1]+"/{"+apk_key[2]+"}", ignore_errors=True)
										state = 4
							else: # 之前没有这个应用
								os.makedirs(root+market+"/"+apk_key[1])
								state = 3
							if state == 1 or state == 3 or state == 4:
								download_icon(market, response[7], "~"+market+"tmp"+threadidstr+".png")
								cur_time = str(int(time.time()))
								fout = codecs.open(extract_dir+"/Index.txt", "w", "utf-8")
								fout.write("Market\n\t"+apk_key[0]+"\nPackage_Name\n\t"+apk_key[1]+"\nMD5\n\t"+apk_key[2]+"\nTime\n\t"+cur_time+"\nLink\n\t"+url+"\nDownload_Link\n\t"+response[4]+"\n")
								fout.close()
								shutil.move("~"+market+"tmp"+threadidstr+".apk", extract_dir+"/"+apk_key[1]+".apk")
								if os.path.isfile("~"+market+"tmp"+threadidstr+".png"):
									if market != 'googleplay': shutil.move("~"+market+"tmp"+threadidstr+".png", extract_dir+"/icon.png")
									else: shutil.move("~"+market+"tmp"+threadidstr+".png", extract_dir+"/icon.webp")
								shutil.copytree(extract_dir, root+market+"/"+apk_key[1]+"/{"+apk_key[2]+"}", symlinks=True)
							else:
								cur_time = str(int(time.time()))
							if not os.path.exists(root+market+"/"+apk_key[1]+"/["+cur_time+"]"):
								os.makedirs(root+market+"/"+apk_key[1]+"/["+cur_time+"]")
							lock_log.acquire()
							hold_lock_log = True
							flog = open(root+'__log__/'+market+'.log', 'a')
							flog.write(cur_time+' success '+short_url+' '+apk_key[1]+' '+apk_key[2]+'\n')
							flog.close()
							lock_log.release()
							hold_lock_log = False
							if not os.path.isfile(root+market+"/"+apk_key[1]+"/["+cur_time+"]/end"):
								write_text_information(root+market+"/"+apk_key[1]+"/["+cur_time+"]/", response)
								fout = codecs.open(root+market+"/"+apk_key[1]+"/["+cur_time+"]/Index.txt", "w", "utf-8")
								fout.write("Market\n\t"+apk_key[0]+"\nPackage_Name\n\t"+apk_key[1]+"\nMD5\n\t"+apk_key[2]+"\nTime\n\t"+cur_time+"\nLink\n\t"+url+"\nDownload_Link\n\t"+response[4]+"\n")
								fout.close()
								open(root+market+"/"+apk_key[1]+"/["+cur_time+"]/end", "w").close()								
							if state == 1 or state == 3 or state == 4:
								open(root+market+"/"+apk_key[1]+"/{"+apk_key[2]+"}/end", "w").close()
							if state == 1: print (apk_key[0]+threadidstr+"：更新"+apk_key[1]+"版本和信息")
							elif state == 2: print (apk_key[0]+threadidstr+"：更新"+apk_key[1]+"信息。无版本更新")
							elif state == 3: print (apk_key[0]+threadidstr+"：新增"+apk_key[1])
							elif state == 4: print (apk_key[0]+threadidstr+"：修复"+apk_key[1])
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

def initialization(param):
	market = param[0]
	thread_num = param[1]
	rate_per_iteration = param[2]
	need_extend = param[3]
	set_maxsize = param[4]
	print ("初始化进程：("+market+", "+str(thread_num)+", "+str(rate_per_iteration)+")")
	lock_pool = threading.Lock()
	name_pool = set()
	lock_set = threading.Lock()
	url_set = read_url(market)
	lock_log = threading.Lock()
	if market == 'googleplay': config = read_config()
	else: config = {}
	if not os.path.exists(root+market): os.makedirs(root+market)
	threads = []
	for i in range(1, thread_num):
		threads.append(threading.Thread(target=main_loop, args=(str(i), market, thread_num, rate_per_iteration, lock_pool, name_pool, lock_set, url_set, lock_log, need_extend, set_maxsize, config)))
	for t in threads:
		t.start()
	main_loop('0', market, thread_num, rate_per_iteration, lock_pool, name_pool, lock_set, url_set, lock_log, need_extend, set_maxsize, config)
	for t in threads:
		t.join()
	print ("进程"+market+"退出")

if False:
	market = 'pp'
	myurl = 'http://www.25pp.com/android/detail_37577/'
	response = open_url(market, myurl)
	for key, val in response[0].items():
		print (key+": "+val)
	print ("-----------")
	for permission in response[1]:
		print (permission)
	print ("-----------")
	print (response[2])
	print ("-----------")
	print (response[3])
	print ("-----------")
	print (response[4])
	print ("-----------")
	for newurl in response[5]:
		print (newurl)
	print ("-----------")
	for newurl in response[6]:
		print (newurl)
	print ("-----------")
	print (response[7])
	exit()
	download_apk('pp', response[4], '~pptmp0.apk', {})
	download_icon('pp', response[7], '~pptmp0.png')	
	exit()
	
if __name__ == '__main__':
	if not os.path.isfile(phantomjs_path) or (not os.path.exists(root) and len(root) > 0) or not os.path.isfile("settings.txt"): exit()
	if not os.path.exists(root+"__log__"): os.makedirs(root+"__log__")
	if os.path.isfile('exit'): os.remove('exit')
	fin_settings = open("settings.txt", "r")
	param_list = []
	market_set = set()
	for line in fin_settings:
		if line.startswith('#') or len(line) <= 3: continue
		market = line.split(" ")[0].lower()
		thread_num = int(line.split(" ")[1])
		rate_per_iteration = float(line.split(" ")[2])
		if len(line.split(" ")) <= 3 or int(line.split(" ")[3]) <= 0:
			need_extend = False
			set_maxsize = 0
		else:
			need_extend = True
			set_maxsize = int(line.split(" ")[3])
		if market in market_set: exit()
		if thread_num <= 0 or thread_num > 50: exit()
		if rate_per_iteration <= 0 or rate_per_iteration > 1: exit()
		param_list.append((market, thread_num, rate_per_iteration, need_extend, set_maxsize))
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

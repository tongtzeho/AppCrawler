# -*- coding:utf-8 -*-

from selenium import webdriver
from urllib import request
import re, urllib, time

def get_extend_urls(market, data, prefix):
	urls = set()
	if market == 'yingyongbao':
		matcher = re.findall('<a href="../myapp/detail.htm\?apkName=.*?"', data)
		for url in matcher:
			full_url = 'http://sj.qq.com'+re.subn('\&(.+)', "", url.replace('"', "").replace('<a href=..', ""))[0]
			if full_url.startswith(prefix): urls.add(full_url.replace(prefix, ""))
		matcher = re.findall('<a href="detail.htm\?apkName=.*?"', data)
		for url in matcher:
			full_url = 'http://sj.qq.com/myapp/'+re.subn('\&(.+)', "", url.replace('"', "").replace('<a href=', ""))[0]
			if full_url.startswith(prefix): urls.add(full_url.replace(prefix, ""))
			
	elif market == 'baidu':
		matcher = re.findall('href="\/[a-z]+\/[0-9]+.html"', data)
		for url in matcher:
			full_url = 'http://shouji.baidu.com'+url.replace('href="', "").replace('"', "").replace('game', 'software')
			if full_url.startswith(prefix): urls.add(full_url.replace(prefix, ""))
			
	elif market == '360':
		matcher = re.findall('href="/detail/index/soft_id/[0-9]+', data)
		for url in matcher:
			full_url = 'http://zhushou.360.cn'+url.replace('href="', "")
			if full_url.startswith(prefix): urls.add(full_url.replace(prefix, ""))
			
	elif market == 'googleplay':
		matcher = re.findall('href="/store/apps/details\?id=.*?"', data)
		for url in matcher:
			full_url = 'https://play.google.com'+url.replace('href="', "").replace('"', "")
			if '&' in full_url: full_url = full_url[:full_url.index('&')]
			if full_url.startswith(prefix): urls.add(full_url.replace(prefix, ""))
			
	elif market == 'huawei':
		matcher = re.findall('<a href=".*?">', data)
		for url in matcher:
			full_url = url.replace('<a href="', "").replace('">', "").replace(':80', "")
			if full_url.startswith(prefix): urls.add(full_url.replace(prefix, ""))
			
	elif market == 'xiaomi':
		matcher = re.findall('<a href="/details\?id=.*?">', data)
		for url in matcher:
			full_url = 'http://app.mi.com'+url.replace('<a href="', "").replace('">', "")
			if full_url.startswith(prefix): urls.add(full_url.replace(prefix, ""))
			
	elif market == 'wandoujia':
		matcher = re.findall('<a href="http://www.wandoujia.com/apps/.*?"', data)
		for url in matcher:
			full_url = url.replace('<a href="', "").replace('/download"', "").replace('"', "")
			if full_url.startswith(prefix): urls.add(full_url.replace(prefix, ""))
		matcher = re.findall('<a href="/apps/.*?"', data)
		for url in matcher:
			full_url = 'http://www.wandoujia.com'+url.replace('<a href="', "").replace('/download"', "").replace('"', "")
			if full_url.startswith(prefix): urls.add(full_url.replace(prefix, ""))
			
	elif market == 'hiapk':
		matcher = re.findall('<a href="/appinfo/.*?">.*?<', data)
		for url in matcher:
			urls.add(re.subn('/.+', "", re.subn('".+', "", url.replace('<a href="/appinfo/', ""))[0])[0])
			
	return urls
	
def get_similar_apps(market, data, prefix):
	urls = set()
	if market == 'yingyongbao':
		matcher = re.findall('<ul class="det-about-applist">.*?</ul>', data, re.S)
		if len(matcher):
			matcher = re.findall('<a href="../myapp/detail.htm\?apkName=.*?"', matcher[0])
			for url in matcher:
				full_url = 'http://sj.qq.com'+re.subn('\&(.+)', "", url.replace('"', "").replace('<a href=..', ""))[0]
				if full_url.startswith(prefix): urls.add(full_url.replace(prefix, "")) 
				
	elif market == '360':
		matcher = re.findall('<h2>本类热门应用</h2>.*?<script', data, re.S)
		if len(matcher):
			matcher = re.findall('href="/detail/index/soft_id/[0-9]+', matcher[0])
			for url in matcher:
				full_url = 'http://zhushou.360.cn'+url.replace('href="', "")
				if full_url.startswith(prefix): urls.add(full_url.replace(prefix, ""))
				
	elif market == 'googleplay':
		matcher = re.findall('secondary-content"> *<div.*?</div> *</div> *</div> *</div>', data, re.S)
		if len(matcher):
			matcher = re.findall('href="/store/apps/details\?id=.*?"', matcher[0])
			for url in matcher:
				full_url = 'https://play.google.com'+url.replace('href="', "").replace('"', "")
				if '&' in full_url: full_url = full_url[:full_url.index('&')]
				if full_url.startswith(prefix): urls.add(full_url.replace(prefix, ""))	

	elif market == 'huawei':
		matcher = re.findall('<span class="title flt ft-yh">相关推荐</span>.+<span class="title flt ft-yh">.*?排行<', data, re.S)
		if len(matcher):
			matcher = re.findall('<a href=".*?"><', matcher[0])
			for url in matcher:
				full_url = url.replace('<a href="', "").replace('"><', "").replace(':80', "")
				if full_url.startswith(prefix): urls.add(full_url.replace(prefix, ""))
		else:
			matcher = re.findall('<span class="title flt ft-yh">相关推荐</span>.+', data, re.S)
			if len(matcher):
				matcher = re.findall('<a href=".*?"><', matcher[0])
				for url in matcher:
					full_url = url.replace('<a href="', "").replace('"><', "").replace(':80', "")
					if full_url.startswith(prefix): urls.add(full_url.replace(prefix, ""))
					
	elif market == 'xiaomi':
		matcher = re.findall('<h3 class="special-h3">相关应用</h3>.+', data, re.S)
		if len(matcher):
			matcher = re.findall('<a href="/details\?id=.*?">', matcher[0])
			for url in matcher:
				full_url = 'http://app.mi.com'+url.replace('<a href="', "").replace('">', "")
				if full_url.startswith(prefix): urls.add(full_url.replace(prefix, ""))
				
	elif market == 'hiapk':
		matcher = re.findall('<a href="/appinfo/.*?">.*?<', data)
		for url in matcher:
			urls.add(re.subn('/.+', "", re.subn('".+', "", url.replace('<a href="/appinfo/', ""))[0])[0])				
	
	return urls

def generate_url(market):
	result = []
	if market == 'yingyongbao':
		result.append('http://sj.qq.com/myapp/category.htm?orgame=1')
		result.append('http://sj.qq.com/myapp/category.htm?orgame=2')
		categoryid = ('-10', '122', '102', '110', '103', '108', '115', '106', '101', '119', '104', '114', '117', '107', '112', '118', '111', '109', '105', '100', '113', '116')
		for c in categoryid:
			result.append('http://sj.qq.com/myapp/category.htm?orgame=1&categoryId='+c)
		categoryid = ('147', '121', '149', '144', '151', '148', '153', '146')
		for c in categoryid:
			result.append('http://sj.qq.com/myapp/category.htm?orgame=2&categoryId='+c)
			
	elif market == 'baidu':
		for i in range(501, 511):
			for j in range(1, 9):
				result.append("http://shouji.baidu.com/software/"+str(i)+"/list_"+str(j)+".html")
		for i in range(401, 409):
			for j in range(1, 9):
				result.append("http://shouji.baidu.com/game/"+str(i)+"/list_"+str(j)+".html")
				
	elif market == '360':
		for i in range(1, 3):
			for j in range(1, 51):
				result.append("http://zhushou.360.cn/list/index/cid/"+str(i)+"/order/download/?page="+str(j))
				
	elif market == 'googleplay':
		result = [
		'https://play.google.com/store/apps/category/ANDROID_WEAR',
		'https://play.google.com/store/apps/category/ART_AND_DESIGN/collection/topselling_free',
		'https://play.google.com/store/apps/category/AUTO_AND_VEHICLES/collection/topselling_free', 
		'https://play.google.com/store/apps/category/BEAUTY/collection/topselling_free', 
		'https://play.google.com/store/apps/category/BOOKS_AND_REFERENCE/collection/topselling_free', 
		'https://play.google.com/store/apps/category/BUSINESS/collection/topselling_free', 
		'https://play.google.com/store/apps/category/COMICS/collection/topselling_free', 
		'https://play.google.com/store/apps/category/COMMUNICATION/collection/topselling_free', 
		'https://play.google.com/store/apps/category/DATING/collection/topselling_free', 
		'https://play.google.com/store/apps/category/EDUCATION/collection/topselling_free', 
		'https://play.google.com/store/apps/category/ENTERTAINMENT/collection/topselling_free', 
		'https://play.google.com/store/apps/category/EVENTS/collection/topselling_free', 
		'https://play.google.com/store/apps/category/FINANCE/collection/topselling_free', 
		'https://play.google.com/store/apps/category/FOOD_AND_DRINK/collection/topselling_free', 
		'https://play.google.com/store/apps/category/HEALTH_AND_FITNESS/collection/topselling_free', 
		'https://play.google.com/store/apps/category/HOUSE_AND_HOME/collection/topselling_free', 
		'https://play.google.com/store/apps/category/LIBRARIES_AND_DEMO/collection/topselling_free', 
		'https://play.google.com/store/apps/category/LIFESTYLE/collection/topselling_free', 
		'https://play.google.com/store/apps/category/MAPS_AND_NAVIGATION/collection/topselling_free', 
		'https://play.google.com/store/apps/category/MEDICAL/collection/topselling_free', 
		'https://play.google.com/store/apps/category/MUSIC_AND_AUDIO/collection/topselling_free', 
		'https://play.google.com/store/apps/category/NEWS_AND_MAGAZINES/collection/topselling_free', 
		'https://play.google.com/store/apps/category/PARENTING/collection/topselling_free', 
		'https://play.google.com/store/apps/category/PERSONALIZATION/collection/topselling_free', 
		'https://play.google.com/store/apps/category/PHOTOGRAPHY/collection/topselling_free', 
		'https://play.google.com/store/apps/category/PRODUCTIVITY/collection/topselling_free', 
		'https://play.google.com/store/apps/category/SHOPPING/collection/topselling_free', 
		'https://play.google.com/store/apps/category/SOCIAL/collection/topselling_free', 
		'https://play.google.com/store/apps/category/SPORTS/collection/topselling_free', 
		'https://play.google.com/store/apps/category/TOOLS/collection/topselling_free', 
		'https://play.google.com/store/apps/category/TRAVEL_AND_LOCAL/collection/topselling_free', 
		'https://play.google.com/store/apps/category/VIDEO_PLAYERS/collection/topselling_free', 
		'https://play.google.com/store/apps/category/WEATHER/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_ACTION/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_ADVENTURE/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_ARCADE/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_BOARD/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_CARD/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_CASINO/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_CASUAL/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_EDUCATIONAL/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_MUSIC/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_PUZZLE/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_RACING/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_ROLE_PLAYING/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_SIMULATION/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_SPORTS/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_STRATEGY/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_TRIVIA/collection/topselling_free', 
		'https://play.google.com/store/apps/category/GAME_WORD/collection/topselling_free'
		]
	
	elif market == 'huawei':
		listid = ('23', '24', '26', '30', '345', '33', '358', '28', '25', '31', '27', '29')
		for l in listid:
			for i in range(1, 10):
				result.append("http://appstore.huawei.com/soft/list_"+l+"_2_"+str(i))
		listid = ('15', '16', '22', '21', '18', '20')
		for l in listid:
			for i in range(1, 10):
				result.append("http://appstore.huawei.com/game/list_"+l+"_2_"+str(i))

	elif market == 'xiaomi':
		for i in range(1, 30):
			result.append("http://app.mi.com/category/"+str(i))
			
	elif market == 'wandoujia':
		category_size = {'384':38, '257':38, '386':41, '388':42, '390':42, '392':42, '394':42, '396':42, '398':42, '400':29, '402':42, '404':26, '406':42, '408':40, '410':42, '412':42, '414':42, '416':42, '237':10, '239':10, '241':42, '243':41, '245':30, '247':41, '249':41, '251':41, '253':41, '382':42, '255':20}
		for key, val in category_size.items():
			for i in range(1, val+1):
				result.append("http://www.wandoujia.com/category/"+key+"_"+str(i))
				
	elif market == 'hiapk':
		category_name = ("/apps/MediaAndVideo", "/apps/DailyLife", "/apps/Social", "/apps/Finance", "/apps/Tools", "/apps/TravelAndLocal", "/apps/Communication", "/apps/Shopping", "/apps/Reading", "/apps/Education", "/apps/NewsAndMagazines", "/apps/HealthAndFitness", "/apps/AntiVirus", "/apps/Browser", "/apps/Productivity", "/apps/Personalization", "/apps/Input", "/apps/Photography", "/games/OnlineGames", "/games/Casual", "/games/RolePlaying", "/games/BrainAndPuzzle", "/games/Shooting", "/games/Sports", "/games/Children", "/games/Chess", "/games/Strategy", "/games/Simulation", "/games/Racing")
		for c in category_name:
			for i in [5, 8, 9]:
				for p in range(1, 51):
					result.append("http://apk.hiapk.com"+c+"?sort="+str(i)+"&pi="+str(p))
	
	return tuple(result)
	
if __name__ == '__main__':
	
	phantomjs_path = 'phantomjs/bin/phantomjs.exe'
	
	url_prefix = {
	'yingyongbao': 'http://sj.qq.com/myapp/detail.htm?apkName=',
	'baidu': 'http://shouji.baidu.com/software/',
	'360': 'http://zhushou.360.cn/detail/index/soft_id/',
	'googleplay': 'https://play.google.com/store/apps/details?id=',
	'huawei': 'http://appstore.huawei.com/app/',
	'xiaomi': 'http://app.mi.com/details?id=',
	'wandoujia': 'http://www.wandoujia.com/apps/',
	'hiapk': 'http://apk.hiapk.com/appinfo/'
	}
	
	for key in url_prefix:
		#if key != 'hiapk': continue
		url_set = set()
		url_tuple = generate_url(key)
		for root_url in url_tuple:
			while True:
				try:				
					driver = webdriver.PhantomJS(executable_path=phantomjs_path)
					driver.set_page_load_timeout(20)
					driver.get(root_url)
					time.sleep(0.5)
					data = driver.page_source
					driver.quit()				
					#web = request.urlopen(root_url, timeout=20)
					#charset = str(web.headers.get_content_charset())
					#if charset == "None": charset = "utf-8"
					#data = web.read().decode(charset)					
					url_set.update(get_extend_urls(key, data, url_prefix[key]))
					print ("完成："+root_url)
					break
				except:
					continue
		fout = open(key+"_url_list.txt", "w")
		for url in url_set:
			fout.write(url+"\n")
		fout.close()
		print ("完成："+key)
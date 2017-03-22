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
			
	elif market == 'anzhi':
		matcher = re.findall('<a href="/soft_[0-9]+.html" class="recommend', data)
		for url in matcher:
			urls.add(url.replace('<a href="/', "").replace('" class="recommend', ""))
		matcher = re.findall('<a href="/soft_[0-9]+.html">', data)
		for url in matcher:
			urls.add(url.replace('<a href="/', "").replace('">', ""))
			
	elif market == '91':
		matcher = re.findall('a target="_blank" href="/Soft/Android/.*?.html"', data)
		for url in matcher:
			urls.add(re.subn('-.*?\.html', ".html", url.replace('a target="_blank" href="/Soft/Android/', "").replace('"', ""))[0])
		matcher = re.findall('<a class="down_btn" href="/Soft/Android/.*?.html">', data)
		for url in matcher:
			urls.add(re.subn('-.*?\.html', ".html", url.replace('<a class="down_btn" href="/Soft/Android/', "").replace('">', ""))[0])

	elif market == 'oppo':
		matcher = re.findall('<a href="http://store.oppomobile.com/product/.*?\?from=.*?">', data)
		for url in matcher:
			full_url = re.subn('\?from=.+', "", url.replace('<a href="', ""))[0]
			if full_url.startswith(prefix):
				full_url = re.subn('_[0-9]+', "_0", full_url)[0]
				urls.add(full_url.replace(prefix, ""))

	elif market == 'pp':
		matcher = re.findall('<a href="/android/detail_[0-9]+/"', data)
		for url in matcher:
			full_url = prefix+url.replace('<a href="/android/', "").replace('"', "")
			urls.add(full_url.replace(prefix, ""))

	elif market == 'sogou':
		matcher = re.findall('<a href="http://zhushou.sogou.com/apps/detail/.*?\.html">', data)
		for url in matcher:
			full_url = url.replace('<a href="', "").replace('">', "")
			urls.add(full_url.replace(prefix, ""))
		matcher = re.findall('<a href="http://zhushou.sogou.com/apps/detail/.*?\.html" title=".*?">', data)
		for url in matcher:
			urls.add(url.split('"')[-4].replace(prefix, ""))

	elif market == 'gfan':
		matcher = re.findall('<a href="/Product/.*?\.html"', data)
		for url in matcher:
			full_url = 'http://apk.gfan.com'+url.replace('<a href="', "").replace('"', "")
			urls.add(full_url.replace(prefix, ""))

	elif market == 'meizu':
		matcher = re.findall('<a href="/apps/public/detail\?package_name=.*?"', data)
		for url in matcher:
			full_url = 'http://app.meizu.com'+url.replace('<a href="', "").replace('"', "")
			urls.add(full_url.replace(prefix, ""))
		matcher = re.findall('<a href="/games/public/detail\?package_name=.*?"', data)
		for url in matcher:
			full_url = 'http://app.meizu.com/apps'+url.replace('<a href="/games', "").replace('"', "")
			urls.add(full_url.replace(prefix, ""))

	elif market == 'sina':
		matcher = re.findall('<a href="/appdetail.php\?appID=[0-9]+&"', data)
		for url in matcher:
			full_url = 'http://app.sina.com.cn'+re.subn('&.+', '&', url.replace('<a href="', "").replace('"', ""))[0]
			urls.add(full_url.replace(prefix, ""))

	elif market == 'dcn':
		matcher = re.findall('href="http://android.d.cn/software/[0-9]+.html"', data)
		for url in matcher:
			full_url = url.replace('href="', "").replace('"', "")
			urls.add(full_url.replace(prefix, ""))
		matcher = re.findall('href="http://android.d.cn/game/[0-9]+.html"', data)
		for url in matcher:
			full_url = url.replace('href="', "").replace('"', "")
			urls.add(full_url.replace(prefix, ""))
		matcher = re.findall('href="/software/[0-9]+.html"', data)
		for url in matcher:
			urls.add(url.replace('href="/', "").replace('"', ""))
		matcher = re.findall('href="/game/[0-9]+.html"', data)
		for url in matcher:
			urls.add(url.replace('href="/', "").replace('"', ""))

	elif market == 'liqucn':
		matcher = re.findall('<a href="http://os-android.liqucn.com/[rwy][jyx]/[0-9]+.shtml"', data)
		for url in matcher:
			full_url = url.replace('<a href="', "").replace('"', "")
			urls.add(full_url.replace(prefix, ""))

	elif market == 'appchina':
		matcher = re.findall('<a href="/app/[^ ]*?">', data)
		for url in matcher:
			urls.add(url.replace('<a href="/app/', "").replace('">', ""))

	elif market == '10086':
		matcher = re.findall('class="mj_tj_tu" href="/android/info/[0-9]+.html', data)
		for url in matcher:
			urls.add(url.replace('class="mj_tj_tu" href="/android/info/', ""))
		matcher = re.findall('<a href="/android/info/[0-9]+.html', data)
		for url in matcher:
			urls.add(url.replace('<a href="/android/info/', ""))

	elif market == 'lenovo':
		matcher = re.findall('<a href="http://www.lenovomm.com/appdetail/.*?" target="_blank">', data)
		for url in matcher:
			urls.add(url.replace('<a href="http://www.lenovomm.com/appdetail/', "").replace('" target="_blank">', ""))
		matcher = re.findall('<a href="http://www.lenovomm.com/appdetail/.*?" target="_blank" hover>', data)
		for url in matcher:
			urls.add(url.replace('<a href="http://www.lenovomm.com/appdetail/', "").replace('" target="_blank" hover>', ""))

	elif market == 'zol':
		matcher = re.findall('<a target="_b[al][al]nk" href="/[^/]+/"', data)
		for url in matcher:
			urls.add(url.split('"')[-2][1:])
		matcher = re.findall('<a href="/[^/]+/" target="_blank"', data)
		for url in matcher:
			urls.add(url.split('"')[1][1:])
	#	matcher = re.findall('<a target="_blank" href=" http://sj.zol.com.cn/[^/]+/"', data)
	#	for url in matcher:
	#		urls.add(url.split('/')[-2]+'/')
			
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

	elif market == '91':
		matcher = re.findall('a target="_blank" href="/Soft/Android/.*?.html"', data)
		for url in matcher:
			urls.add(re.subn('-.*?\.html', ".html", url.replace('a target="_blank" href="/Soft/Android/', "").replace('"', ""))[0])

	elif market == 'oppo':
		matcher = re.findall('<a href="http://store.oppomobile.com/product/.*?\?from=.*?">', data)
		for url in matcher:
			full_url = re.subn('\?from=.+', "", url.replace('<a href="', ""))[0]
			if full_url.startswith(prefix):
				full_url = re.subn('_[0-9]+', "_0", full_url)[0]
				urls.add(full_url.replace(prefix, ""))

	elif market == 'pp':
		matcher = re.findall('<h3 class="title"><i class="icon"></i>你可能是要下载</h3>.+', data, re.S)
		if len(matcher):
			matcher = re.findall('<a href="/android/detail_[0-9]+/"', matcher[0])
			for url in matcher:
				full_url = prefix+url.replace('<a href="/android/', "").replace('"', "")
				urls.add(full_url.replace(prefix, ""))

	elif market == 'sogou':
		matcher = re.findall('<div class="rec r2">.*?</div>', data, re.S)
		if len(matcher):
			matcher = re.findall('<a href="http://zhushou.sogou.com/apps/detail/.*?">', matcher[0])
			for url in matcher:
				full_url = url.replace('<a href="', "").replace('">', "")
				urls.add(full_url.replace(prefix, ""))

	elif market == 'meizu':
		matcher = re.findall('<h3>相关推荐</h3>.+', data, re.S)
		if len(matcher):
			matcher1 = re.findall('<a href="/apps/public/detail\?package_name=.*?"', matcher[0])
			for url in matcher1:
				full_url = 'http://app.meizu.com'+url.replace('<a href="', "").replace('"', "")
				urls.add(full_url.replace(prefix, ""))
			matcher = re.findall('<a href="/games/public/detail\?package_name=.*?"', matcher[0])
			for url in matcher:
				full_url = 'http://app.meizu.com/apps'+url.replace('<a href="/games', "").replace('"', "")
				urls.add(full_url.replace(prefix, ""))

	elif market == 'liqucn':
		matcher = re.findall('app相关推荐</div>.*?</ul>', data, re.S)
		if len(matcher):
			matcher = re.findall('<a href="http://os-android.liqucn.com/[rwy][jyx]/[0-9]+.shtml"', matcher[0])
			for url in matcher:
				full_url = url.replace('<a href="', "").replace('"', "")
				urls.add(full_url.replace(prefix, ""))

	elif market == 'appchina':
		matcher = re.findall('<ul class="srel-ul">.*?</ul>', data, re.S)
		if len(matcher):
			matcher = re.findall('<a href="/app/[^ ]*?">', matcher[0])
			for url in matcher:
				urls.add(url.replace('<a href="/app/', "").replace('">', ""))

	elif market == '10086':
		matcher = re.findall('<span>相关推荐</span></div><div class="mj_tj_list">.*?</div></div></div>', data, re.S)
		if len(matcher):
			matcher = re.findall('class="mj_tj_tu" href="/android/info/[0-9]+.html', matcher[0])
			for url in matcher:
				urls.add(url.replace('class="mj_tj_tu" href="/android/info/', ""))

	elif market == 'lenovo':
		matcher = re.findall('<a href="http://www.lenovomm.com/appdetail/.*?" target="_blank">', data)
		for url in matcher:
			urls.add(url.replace('<a href="http://www.lenovomm.com/appdetail/', "").replace('" target="_blank">', ""))
	
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
					
	elif market == 'anzhi':
		for i in range(1, 10001):
			result.append("http://www.anzhi.com/list_1_"+str(i)+"_hot.html")
		for i in range(1, 66):
			result.append("http://www.anzhi.com/list_2_"+str(i)+"_hot.html")
			
	elif market == '91':
		category_name = ("/game/0", "/soft/0", "/game/34", "/game/44", "/game/36", "/game/35", "/game/40", "/game/42", "/game/33", "/game/41", "/game/43", "/game/39", "/game/37", "/game/53", "/game/45", "/game/38", "/soft/7", "/soft/18", "/soft/27", "/soft/29", "/soft/51", "/soft/6", "/soft/2", "/soft/28", "/soft/26", "/soft/48", "/soft/49", "/soft/47", "/soft/30", "/soft/17", "/soft/8", "/soft/5", "/soft/12", "/soft/16", "/soft/10", "/soft/19", "/soft/31", "/soft/52", "/soft/15", "/soft/23", "/soft/20", "/soft/11", "/soft/3", "/soft/25", "/soft/22", "/soft/9", "/soft/24", "/soft/4", "/soft/14", "/soft/21", "/soft/13", "/soft/1")
		for category in category_name:
			for i in range(1, 21):
				result.append('http://apk.91.com'+category+"_"+str(i)+"_13")

	elif market == 'oppo':
		for i in range(1, 764):
			result.append('http://store.oppomobile.com/product/category/22_7_'+str(i)+'.html')
		for i in range(1, 179):
			result.append('http://store.oppomobile.com/product/category/22_8_'+str(i)+'.html')

	elif market == 'pp':
		soft_category = ('5029', '5018', '5014', '5024', '5019', '5016', '5026', '5017', '5023', '5020', '5021', '5028', '5022', '5027')
		for c in soft_category:
			for i in range(1, 43):
				result.append('http://www.25pp.com/android/soft/fenlei/'+c+'/'+str(i)+'/')
		game_category = ('6001', '6003', '6008', '6004', '6002', '6007', '6009', '6005', '6006', '5015')
		for c in game_category:
			for i in range(1, 43):
				result.append('http://www.25pp.com/android/game/fenlei/'+c+'/'+str(i)+'/')

	elif market == 'sogou':
		category_list = (
			'3514-0', '0-5579', '0-5581', '0-5580', '0-5576', '0-5658', '0-5578', '0-5577', '0-6549', '3511-0', '0-5570', '0-5631', '0-5568', '0-5569', '0-5571', '0-5572', '0-5575', '0-5574', '0-5573', 
			'0-6543', '3512-0', '0-5553', '0-5555', '0-5554', '0-5557', '0-5558', '0-5629', '0-5659', '0-5660', '3507-0', '0-5627', '0-5621', '0-5624', '0-5626', '6488-0', '0-5564', '0-5565', '0-5663', 
			'0-6521', '0-6519', '0-5664', '0-6520', '0-6550', '6489-0', '0-6522', '0-6523', '0-6524', '0-6525', '0-6526', '3509-0', '0-5560', '0-5559', '0-6530', '0-6531', '0-6529', '0-6545', '0-6527', 
			'0-6528', '3510-0', '0-5607', '0-5609', '0-5611', '0-5666', '0-5591', '0-5613', '0-5592', '3513-0', '0-5583', '0-5586', '0-5587', '0-5590', '0-5589', '0-6533', '0-6542', '3506-0', '0-5635', 
			'0-5633', '0-5637', '0-5634', '0-5673', '0-5672', '6491-0', '0-6534', '0-5671', '0-6535', '3508-0', '0-5619', '0-5618', '0-5617', '0-5616', '0-5674', '6494-0', '0-5567', '0-6499', '0-3560', 
			'0-6498', '0-6500', '0-6551', '6495-0', '0-6538', '0-6537', '0-6536', '0-6539', '0-6540', '0-6541', '3495-0', '3503-0', '0-5605', '0-5610', '0-5606', '0-5675', '0-5608', '0-5612', '0-5614', 
			'0-6552', '3504-0', '0-6514', '0-5623', '0-6513', '0-5615', '0-5625', '0-5620', '0-5622', '6493-0', '0-6508', '0-6509', '0-6511', '0-6512', '6492-0', '0-6503', '0-6505', '0-6504', '0-6502', 
			'0-6501', '0-6506', '3499-0', '0-5599', '0-5603', '0-5602', '0-5598', '0-5601', '0-5604', '0-5600', '3497-0', '0-5594', '0-5593', '0-5595', '0-5597', '0-5596', '0-6553', '3498-0', '0-5641', 
			'0-5642', '0-5643', '0-5676', '0-5644', '0-5640', '0-6554', '3496-0', '0-5645', '0-5646', '0-6515', '0-6518', '0-6516', '0-5648', '0-5650', '0-6517', '3500-0', '0-5652', '0-5677', '0-5655', 
			'0-5657', '0-5653', '0-5680', '0-5654', '0-6555', '3505-0', '0-5632', '0-5630', '0-5636', '0-5628', '0-5639', '0-5638', '0-6658'
		)
		for c in category_list:
			result.append('http://zhushou.sogou.com/apps/list/'+c+'.html')

	elif market == 'gfan':
		soft_dict = {1:42, 21:24, 2:191, 141:98, 125:1, 3:70, 123:3, 26:1, 124:4, 22:21, 27:107, 122:2, 55:86, 61:44, 49:4, 25:28, 13:69, 6:76, 5:12, 12:26, 11:9, 56:58}
		for key, val in soft_dict.items():
			for i in range(1, val+1):
				result.append('http://apk.gfan.com/apps_'+str(key)+'_1_'+str(i)+'.html')
		result.append('http://apk.gfan.com/gamess_8_1_1.html')

	elif market == 'meizu':
		app_cate_dict = {'9014':5, '103':3, '102':4, '101':2, '100':3, '104':8, '105':7, '106':5, '338':5, '339':3, '344':4}
		for key, val in app_cate_dict.items():
			for i in range(0, val):
				result.append('http://app.meizu.com/apps/public/category/'+key+'/all/new/index/'+str(i*18)+'/18')
		game_cate_dict = {'1000':3, '1005':2, '1001':2, '1004':2, '9012':2, '1003':2, '1007':2, '9013':2, '1002':2}
		for key, val in app_cate_dict.items():
			for i in range(0, val):
				result.append('http://app.meizu.com/games/public/category/'+key+'/all/new/index/'+str(i*18)+'/18')

	elif market == 'sina':
		for soft_cate_id in range(101, 116):
			result.append('http://app.sina.cn/catlist.php?cat=100&secondcat='+str(soft_cate_id)+'&')
		for game_cate_id in range(201, 213):
			result.append('http://app.sina.cn/catlist.php?cat=200&secondcat='+str(game_cate_id)+'&')

	elif market == 'dcn':
		for i in range(1, 177):
			result.append('http://android.d.cn/game/list_2_1_0_0_0_0_0_0_0_0_0_'+str(i)+'_0.html')
		for i in range(1, 361):
			result.append('http://android.d.cn/software/list_2_0_0_'+str(i)+'.html')

	elif market == 'liqucn':
		result.append('http://os-android.liqucn.com/rj/')
		for i in range(2000, 5681):
			result.append('http://os-android.liqucn.com/rj/?page='+str(i))
		result.append('http://os-android.liqucn.com/yx/')
		for i in range(1, 1478):
			result.append('http://os-android.liqucn.com/yx/?page='+str(i))
		result.append('http://os-android.liqucn.com/wy/')
		for i in range(1, 265):
			result.append('http://os-android.liqucn.com/wy/?page='+str(i))

	elif market == 'appchina':
		for i in range(1, 35):
			result.append('http://www.appchina.com/category/30/1_1_'+str(i)+'_1_0_0_0.html')
		for i in range(1, 35):
			result.append('http://www.appchina.com/category/40/1_1_'+str(i)+'_1_0_0_0.html')

	elif market == '10086':
		for i in range(1, 46):
			result.append('http://mm.10086.cn/android/software/qbrj?pay=1&p='+str(i))
		for i in range(1, 69):
			result.append('http://mm.10086.cn/android/game/qbyx?pay=1&p='+str(i))

	elif market == 'lenovo':
		for i in range(1, 253):
			result.append('http://www.lenovomm.com/category/qbyy_hotest_flat_'+str(i)+'.html')
		for i in range(1, 41):
			result.append('http://www.lenovomm.com/category/qbyx_hotest_flat_'+str(i)+'.html')

	elif market == 'zol':
		for i in range(1, 386):
			result.append('http://sj.zol.com.cn/android_app/page_'+str(i)+'.html')
	
	return tuple(result)
	
if __name__ == '__main__':
	
	#Windows
	#phantomjs_path = 'phantomjs/bin/phantomjs.exe'
	
	#Linux
	phantomjs_path = 'phantomjs'
	
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
		'zol': 'http://sj.zol.com.cn/'
	}
	
	for key in url_prefix:
		if key != 'zol': continue
		url_set = set()
		url_tuple = generate_url(key)
		for root_url in url_tuple:
			err_time = 0
			while True:
				try:
					#动态加载
					driver = webdriver.PhantomJS(executable_path=phantomjs_path)
					driver.set_page_load_timeout(30)
					driver.get(root_url)
					time.sleep(0.5)
					data = driver.page_source
					driver.quit()
					
					#静态加载
					#web = request.urlopen(root_url, timeout=30)
					#charset = str(web.headers.get_content_charset())
					#if charset == "None": charset = "utf-8"
					#data = web.read().decode(charset)
					#if key == '91' and data.startswith("WOW"): continue
					
					url_set.update(get_extend_urls(key, data, url_prefix[key]))
					print ("完成："+root_url)
					break
				except:
					err_time += 1
					if err_time < 10: continue
					print ("错误："+root_url)
					break
		fout = open(key+"_url_list.txt", "w")
		for url in url_set:
			fout.write(url+"\n")
		fout.close()
		print ("完成："+key)
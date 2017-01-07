# -*- coding:utf-8 -*-

from urllib import request
import re, urllib

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
	
	return urls
	
if __name__ == '__main__':
	dict = {
	'googleplay':
	(
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
	),
	
	'yingyongbao':
	(
	'http://sj.qq.com/myapp/category.htm?orgame=1', 
	'http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=-10', 
	'http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=122', 
	'http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=102', 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=110", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=103", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=108", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=115", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=106", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=101", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=119", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=104", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=114", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=117", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=107", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=112", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=118", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=111", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=109", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=105", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=100", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=113", 
	"http://sj.qq.com/myapp/category.htm?orgame=1&categoryId=116", 
	"http://sj.qq.com/myapp/category.htm?orgame=2", 
	"http://sj.qq.com/myapp/category.htm?orgame=2&categoryId=147", 
	"http://sj.qq.com/myapp/category.htm?orgame=2&categoryId=121", 
	"http://sj.qq.com/myapp/category.htm?orgame=2&categoryId=149", 
	"http://sj.qq.com/myapp/category.htm?orgame=2&categoryId=144", 
	"http://sj.qq.com/myapp/category.htm?orgame=2&categoryId=151", 
	"http://sj.qq.com/myapp/category.htm?orgame=2&categoryId=148", 
	"http://sj.qq.com/myapp/category.htm?orgame=2&categoryId=153", 
	"http://sj.qq.com/myapp/category.htm?orgame=2&categoryId=146"
	),
	
	'baidu':
	(
	"http://shouji.baidu.com/software/501/list_1.html", 
	"http://shouji.baidu.com/software/501/list_2.html", 
	"http://shouji.baidu.com/software/501/list_3.html", 
	"http://shouji.baidu.com/software/501/list_4.html", 
	"http://shouji.baidu.com/software/501/list_5.html", 
	"http://shouji.baidu.com/software/501/list_6.html", 
	"http://shouji.baidu.com/software/501/list_7.html", 
	"http://shouji.baidu.com/software/501/list_8.html", 
	"http://shouji.baidu.com/software/502/list_1.html", 
	"http://shouji.baidu.com/software/502/list_2.html", 
	"http://shouji.baidu.com/software/502/list_3.html", 
	"http://shouji.baidu.com/software/502/list_4.html", 
	"http://shouji.baidu.com/software/502/list_5.html", 
	"http://shouji.baidu.com/software/502/list_6.html", 
	"http://shouji.baidu.com/software/502/list_7.html", 
	"http://shouji.baidu.com/software/502/list_8.html", 
	"http://shouji.baidu.com/software/503/list_1.html", 
	"http://shouji.baidu.com/software/503/list_2.html", 
	"http://shouji.baidu.com/software/503/list_3.html", 
	"http://shouji.baidu.com/software/503/list_4.html", 
	"http://shouji.baidu.com/software/503/list_5.html", 
	"http://shouji.baidu.com/software/503/list_6.html", 
	"http://shouji.baidu.com/software/503/list_7.html", 
	"http://shouji.baidu.com/software/503/list_8.html", 
	"http://shouji.baidu.com/software/508/list_1.html", 
	"http://shouji.baidu.com/software/508/list_2.html", 
	"http://shouji.baidu.com/software/508/list_3.html", 
	"http://shouji.baidu.com/software/508/list_4.html", 
	"http://shouji.baidu.com/software/508/list_5.html", 
	"http://shouji.baidu.com/software/508/list_6.html", 
	"http://shouji.baidu.com/software/508/list_7.html", 
	"http://shouji.baidu.com/software/508/list_8.html", 
	"http://shouji.baidu.com/software/506/list_1.html", 
	"http://shouji.baidu.com/software/506/list_2.html", 
	"http://shouji.baidu.com/software/506/list_3.html", 
	"http://shouji.baidu.com/software/506/list_4.html", 
	"http://shouji.baidu.com/software/506/list_5.html", 
	"http://shouji.baidu.com/software/506/list_6.html", 
	"http://shouji.baidu.com/software/506/list_7.html", 
	"http://shouji.baidu.com/software/506/list_8.html", 
	"http://shouji.baidu.com/software/504/list_1.html", 
	"http://shouji.baidu.com/software/504/list_2.html", 
	"http://shouji.baidu.com/software/504/list_3.html", 
	"http://shouji.baidu.com/software/504/list_4.html", 
	"http://shouji.baidu.com/software/504/list_5.html", 
	"http://shouji.baidu.com/software/504/list_6.html", 
	"http://shouji.baidu.com/software/504/list_7.html", 
	"http://shouji.baidu.com/software/504/list_8.html", 
	"http://shouji.baidu.com/software/510/list_1.html", 
	"http://shouji.baidu.com/software/510/list_2.html", 
	"http://shouji.baidu.com/software/510/list_3.html", 
	"http://shouji.baidu.com/software/510/list_4.html", 
	"http://shouji.baidu.com/software/510/list_5.html", 
	"http://shouji.baidu.com/software/510/list_6.html", 
	"http://shouji.baidu.com/software/510/list_7.html", 
	"http://shouji.baidu.com/software/510/list_8.html", 
	"http://shouji.baidu.com/software/507/list_1.html", 
	"http://shouji.baidu.com/software/507/list_2.html", 
	"http://shouji.baidu.com/software/507/list_3.html", 
	"http://shouji.baidu.com/software/507/list_4.html", 
	"http://shouji.baidu.com/software/507/list_5.html", 
	"http://shouji.baidu.com/software/507/list_6.html", 
	"http://shouji.baidu.com/software/507/list_7.html", 
	"http://shouji.baidu.com/software/507/list_8.html", 
	"http://shouji.baidu.com/software/505/list_1.html", 
	"http://shouji.baidu.com/software/505/list_2.html", 
	"http://shouji.baidu.com/software/505/list_3.html", 
	"http://shouji.baidu.com/software/505/list_4.html", 
	"http://shouji.baidu.com/software/505/list_5.html", 
	"http://shouji.baidu.com/software/505/list_6.html", 
	"http://shouji.baidu.com/software/505/list_7.html", 
	"http://shouji.baidu.com/software/505/list_8.html", 
	"http://shouji.baidu.com/software/509/list_1.html", 
	"http://shouji.baidu.com/software/509/list_2.html", 
	"http://shouji.baidu.com/software/509/list_3.html", 
	"http://shouji.baidu.com/software/509/list_4.html", 
	"http://shouji.baidu.com/software/509/list_5.html", 
	"http://shouji.baidu.com/software/509/list_6.html", 
	"http://shouji.baidu.com/software/509/list_7.html", 
	"http://shouji.baidu.com/software/509/list_8.html", 
	'http://shouji.baidu.com/game/401/list_1.html', 
	'http://shouji.baidu.com/game/401/list_2.html', 
	'http://shouji.baidu.com/game/401/list_3.html', 
	'http://shouji.baidu.com/game/401/list_4.html', 
	'http://shouji.baidu.com/game/401/list_5.html', 
	'http://shouji.baidu.com/game/401/list_6.html', 
	'http://shouji.baidu.com/game/401/list_7.html', 
	'http://shouji.baidu.com/game/401/list_8.html', 
	'http://shouji.baidu.com/game/403/list_1.html', 
	'http://shouji.baidu.com/game/403/list_2.html', 
	'http://shouji.baidu.com/game/403/list_3.html', 
	'http://shouji.baidu.com/game/403/list_4.html', 
	'http://shouji.baidu.com/game/403/list_5.html', 
	'http://shouji.baidu.com/game/403/list_6.html', 
	'http://shouji.baidu.com/game/403/list_7.html', 
	'http://shouji.baidu.com/game/403/list_8.html', 
	'http://shouji.baidu.com/game/405/list_1.html', 
	'http://shouji.baidu.com/game/405/list_2.html', 
	'http://shouji.baidu.com/game/405/list_3.html', 
	'http://shouji.baidu.com/game/405/list_4.html', 
	'http://shouji.baidu.com/game/405/list_5.html', 
	'http://shouji.baidu.com/game/405/list_6.html', 
	'http://shouji.baidu.com/game/405/list_7.html', 
	'http://shouji.baidu.com/game/405/list_8.html', 
	'http://shouji.baidu.com/game/408/list_1.html', 
	'http://shouji.baidu.com/game/408/list_2.html', 
	'http://shouji.baidu.com/game/408/list_3.html', 
	'http://shouji.baidu.com/game/408/list_4.html', 
	'http://shouji.baidu.com/game/408/list_5.html', 
	'http://shouji.baidu.com/game/408/list_6.html', 
	'http://shouji.baidu.com/game/408/list_7.html', 
	'http://shouji.baidu.com/game/408/list_8.html', 
	'http://shouji.baidu.com/game/402/list_1.html', 
	'http://shouji.baidu.com/game/402/list_2.html', 
	'http://shouji.baidu.com/game/402/list_3.html', 
	'http://shouji.baidu.com/game/402/list_4.html', 
	'http://shouji.baidu.com/game/402/list_5.html', 
	'http://shouji.baidu.com/game/402/list_6.html', 
	'http://shouji.baidu.com/game/402/list_7.html', 
	'http://shouji.baidu.com/game/402/list_8.html', 
	'http://shouji.baidu.com/game/406/list_1.html', 
	'http://shouji.baidu.com/game/406/list_2.html', 
	'http://shouji.baidu.com/game/406/list_3.html', 
	'http://shouji.baidu.com/game/406/list_4.html', 
	'http://shouji.baidu.com/game/406/list_5.html', 
	'http://shouji.baidu.com/game/406/list_6.html', 
	'http://shouji.baidu.com/game/406/list_7.html', 
	'http://shouji.baidu.com/game/406/list_8.html', 
	'http://shouji.baidu.com/game/404/list_1.html', 
	'http://shouji.baidu.com/game/404/list_2.html', 
	'http://shouji.baidu.com/game/404/list_3.html', 
	'http://shouji.baidu.com/game/404/list_4.html', 
	'http://shouji.baidu.com/game/404/list_5.html', 
	'http://shouji.baidu.com/game/404/list_6.html', 
	'http://shouji.baidu.com/game/404/list_7.html', 
	'http://shouji.baidu.com/game/404/list_8.html', 
	'http://shouji.baidu.com/game/407/list_1.html', 
	'http://shouji.baidu.com/game/407/list_2.html', 
	'http://shouji.baidu.com/game/407/list_3.html', 
	'http://shouji.baidu.com/game/407/list_4.html', 
	'http://shouji.baidu.com/game/407/list_5.html', 
	'http://shouji.baidu.com/game/407/list_6.html', 
	'http://shouji.baidu.com/game/407/list_7.html', 
	'http://shouji.baidu.com/game/407/list_8.html'
	),
	
	'360':
	(
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=1",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=2",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=3",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=4",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=5",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=6",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=7",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=8",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=9",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=10",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=11",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=12",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=13",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=14",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=15",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=16",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=17",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=18",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=19",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=20",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=21",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=22",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=23",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=24",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=25",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=26",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=27",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=28",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=29",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=30",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=31",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=32",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=33",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=34",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=35",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=36",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=37",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=38",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=39",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=40",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=41",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=42",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=43",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=44",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=45",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=46",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=47",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=48",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=49",
	"http://zhushou.360.cn/list/index/cid/1/order/download/?page=50",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=1",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=2",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=3",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=4",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=5",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=6",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=7",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=8",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=9",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=10",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=11",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=12",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=13",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=14",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=15",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=16",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=17",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=18",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=19",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=20",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=21",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=22",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=23",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=24",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=25",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=26",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=27",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=28",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=29",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=30",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=31",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=32",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=33",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=34",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=35",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=36",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=37",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=38",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=39",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=40",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=41",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=42",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=43",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=44",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=45",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=46",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=47",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=48",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=49",
	"http://zhushou.360.cn/list/index/cid/2/order/download/?page=50"	
	),

	'huawei':
	(
	"http://appstore.huawei.com/soft/list_23_2_1",
	"http://appstore.huawei.com/soft/list_23_2_2",
	"http://appstore.huawei.com/soft/list_23_2_3",
	"http://appstore.huawei.com/soft/list_23_2_4",
	"http://appstore.huawei.com/soft/list_23_2_5",
	"http://appstore.huawei.com/soft/list_23_2_6",
	"http://appstore.huawei.com/soft/list_23_2_7",
	"http://appstore.huawei.com/soft/list_23_2_8",
	"http://appstore.huawei.com/soft/list_23_2_9",
	"http://appstore.huawei.com/soft/list_24_2_1",
	"http://appstore.huawei.com/soft/list_24_2_2",
	"http://appstore.huawei.com/soft/list_24_2_3",
	"http://appstore.huawei.com/soft/list_24_2_4",
	"http://appstore.huawei.com/soft/list_24_2_5",
	"http://appstore.huawei.com/soft/list_24_2_6",
	"http://appstore.huawei.com/soft/list_24_2_7",
	"http://appstore.huawei.com/soft/list_24_2_8",
	"http://appstore.huawei.com/soft/list_24_2_9",
	"http://appstore.huawei.com/soft/list_26_2_1",
	"http://appstore.huawei.com/soft/list_26_2_2",
	"http://appstore.huawei.com/soft/list_26_2_3",
	"http://appstore.huawei.com/soft/list_26_2_4",
	"http://appstore.huawei.com/soft/list_26_2_5",
	"http://appstore.huawei.com/soft/list_26_2_6",
	"http://appstore.huawei.com/soft/list_26_2_7",
	"http://appstore.huawei.com/soft/list_26_2_8",
	"http://appstore.huawei.com/soft/list_26_2_9",
	"http://appstore.huawei.com/soft/list_30_2_1",
	"http://appstore.huawei.com/soft/list_30_2_2",
	"http://appstore.huawei.com/soft/list_30_2_3",
	"http://appstore.huawei.com/soft/list_30_2_4",
	"http://appstore.huawei.com/soft/list_30_2_5",
	"http://appstore.huawei.com/soft/list_30_2_6",
	"http://appstore.huawei.com/soft/list_30_2_7",
	"http://appstore.huawei.com/soft/list_30_2_8",
	"http://appstore.huawei.com/soft/list_30_2_9",
	"http://appstore.huawei.com/soft/list_345_2_1",
	"http://appstore.huawei.com/soft/list_345_2_2",
	"http://appstore.huawei.com/soft/list_345_2_3",
	"http://appstore.huawei.com/soft/list_345_2_4",
	"http://appstore.huawei.com/soft/list_345_2_5",
	"http://appstore.huawei.com/soft/list_345_2_6",
	"http://appstore.huawei.com/soft/list_345_2_7",
	"http://appstore.huawei.com/soft/list_345_2_8",
	"http://appstore.huawei.com/soft/list_345_2_9",
	"http://appstore.huawei.com/soft/list_33_2_1",
	"http://appstore.huawei.com/soft/list_33_2_2",
	"http://appstore.huawei.com/soft/list_33_2_3",
	"http://appstore.huawei.com/soft/list_33_2_4",
	"http://appstore.huawei.com/soft/list_33_2_5",
	"http://appstore.huawei.com/soft/list_33_2_6",
	"http://appstore.huawei.com/soft/list_33_2_7",
	"http://appstore.huawei.com/soft/list_33_2_8",
	"http://appstore.huawei.com/soft/list_33_2_9",
	"http://appstore.huawei.com/soft/list_358_2_1",
	"http://appstore.huawei.com/soft/list_358_2_2",
	"http://appstore.huawei.com/soft/list_358_2_3",
	"http://appstore.huawei.com/soft/list_358_2_4",
	"http://appstore.huawei.com/soft/list_358_2_5",
	"http://appstore.huawei.com/soft/list_358_2_6",
	"http://appstore.huawei.com/soft/list_358_2_7",
	"http://appstore.huawei.com/soft/list_358_2_8",
	"http://appstore.huawei.com/soft/list_358_2_9",
	"http://appstore.huawei.com/soft/list_28_2_1",
	"http://appstore.huawei.com/soft/list_28_2_2",
	"http://appstore.huawei.com/soft/list_28_2_3",
	"http://appstore.huawei.com/soft/list_28_2_4",
	"http://appstore.huawei.com/soft/list_28_2_5",
	"http://appstore.huawei.com/soft/list_28_2_6",
	"http://appstore.huawei.com/soft/list_28_2_7",
	"http://appstore.huawei.com/soft/list_28_2_8",
	"http://appstore.huawei.com/soft/list_28_2_9",
	"http://appstore.huawei.com/soft/list_25_2_1",
	"http://appstore.huawei.com/soft/list_25_2_2",
	"http://appstore.huawei.com/soft/list_25_2_3",
	"http://appstore.huawei.com/soft/list_25_2_4",
	"http://appstore.huawei.com/soft/list_25_2_5",
	"http://appstore.huawei.com/soft/list_25_2_6",
	"http://appstore.huawei.com/soft/list_25_2_7",
	"http://appstore.huawei.com/soft/list_25_2_8",
	"http://appstore.huawei.com/soft/list_25_2_9",
	"http://appstore.huawei.com/soft/list_31_2_1",
	"http://appstore.huawei.com/soft/list_31_2_2",
	"http://appstore.huawei.com/soft/list_31_2_3",
	"http://appstore.huawei.com/soft/list_31_2_4",
	"http://appstore.huawei.com/soft/list_31_2_5",
	"http://appstore.huawei.com/soft/list_31_2_6",
	"http://appstore.huawei.com/soft/list_31_2_7",
	"http://appstore.huawei.com/soft/list_31_2_8",
	"http://appstore.huawei.com/soft/list_31_2_9",
	"http://appstore.huawei.com/soft/list_27_2_1",
	"http://appstore.huawei.com/soft/list_27_2_2",
	"http://appstore.huawei.com/soft/list_27_2_3",
	"http://appstore.huawei.com/soft/list_27_2_4",
	"http://appstore.huawei.com/soft/list_27_2_5",
	"http://appstore.huawei.com/soft/list_27_2_6",
	"http://appstore.huawei.com/soft/list_27_2_7",
	"http://appstore.huawei.com/soft/list_27_2_8",
	"http://appstore.huawei.com/soft/list_27_2_9",
	"http://appstore.huawei.com/soft/list_29_2_1",
	"http://appstore.huawei.com/soft/list_29_2_2",
	"http://appstore.huawei.com/soft/list_29_2_3",
	"http://appstore.huawei.com/soft/list_29_2_4",
	"http://appstore.huawei.com/soft/list_29_2_5",
	"http://appstore.huawei.com/soft/list_29_2_6",
	"http://appstore.huawei.com/soft/list_29_2_7",
	"http://appstore.huawei.com/soft/list_29_2_8",
	"http://appstore.huawei.com/soft/list_29_2_9",
	"http://appstore.huawei.com/game/list_15_2_1",
	"http://appstore.huawei.com/game/list_15_2_2",
	"http://appstore.huawei.com/game/list_15_2_3",
	"http://appstore.huawei.com/game/list_15_2_4",
	"http://appstore.huawei.com/game/list_15_2_5",
	"http://appstore.huawei.com/game/list_15_2_6",
	"http://appstore.huawei.com/game/list_15_2_7",
	"http://appstore.huawei.com/game/list_15_2_8",
	"http://appstore.huawei.com/game/list_15_2_9",
	"http://appstore.huawei.com/game/list_16_2_1",
	"http://appstore.huawei.com/game/list_16_2_2",
	"http://appstore.huawei.com/game/list_16_2_3",
	"http://appstore.huawei.com/game/list_16_2_4",
	"http://appstore.huawei.com/game/list_16_2_5",
	"http://appstore.huawei.com/game/list_16_2_6",
	"http://appstore.huawei.com/game/list_16_2_7",
	"http://appstore.huawei.com/game/list_16_2_8",
	"http://appstore.huawei.com/game/list_16_2_9",
	"http://appstore.huawei.com/game/list_22_2_1",
	"http://appstore.huawei.com/game/list_22_2_2",
	"http://appstore.huawei.com/game/list_22_2_3",
	"http://appstore.huawei.com/game/list_22_2_4",
	"http://appstore.huawei.com/game/list_22_2_5",
	"http://appstore.huawei.com/game/list_22_2_6",
	"http://appstore.huawei.com/game/list_22_2_7",
	"http://appstore.huawei.com/game/list_22_2_8",
	"http://appstore.huawei.com/game/list_22_2_9",
	"http://appstore.huawei.com/game/list_21_2_1",
	"http://appstore.huawei.com/game/list_21_2_2",
	"http://appstore.huawei.com/game/list_21_2_3",
	"http://appstore.huawei.com/game/list_21_2_4",
	"http://appstore.huawei.com/game/list_21_2_5",
	"http://appstore.huawei.com/game/list_21_2_6",
	"http://appstore.huawei.com/game/list_21_2_7",
	"http://appstore.huawei.com/game/list_21_2_8",
	"http://appstore.huawei.com/game/list_21_2_9",
	"http://appstore.huawei.com/game/list_18_2_1",
	"http://appstore.huawei.com/game/list_18_2_2",
	"http://appstore.huawei.com/game/list_18_2_3",
	"http://appstore.huawei.com/game/list_18_2_4",
	"http://appstore.huawei.com/game/list_18_2_5",
	"http://appstore.huawei.com/game/list_18_2_6",
	"http://appstore.huawei.com/game/list_18_2_7",
	"http://appstore.huawei.com/game/list_18_2_8",
	"http://appstore.huawei.com/game/list_18_2_9",
	"http://appstore.huawei.com/game/list_20_2_1",
	"http://appstore.huawei.com/game/list_20_2_2",
	"http://appstore.huawei.com/game/list_20_2_3",
	"http://appstore.huawei.com/game/list_20_2_4",
	"http://appstore.huawei.com/game/list_20_2_5",
	"http://appstore.huawei.com/game/list_20_2_6",
	"http://appstore.huawei.com/game/list_20_2_7",
	"http://appstore.huawei.com/game/list_20_2_8",
	"http://appstore.huawei.com/game/list_20_2_9"
	)
	}
	
	url_prefix = {
	'yingyongbao': 'http://sj.qq.com/myapp/detail.htm?apkName=',
	'baidu': 'http://shouji.baidu.com/software/',
	'360': 'http://zhushou.360.cn/detail/index/soft_id/',
	'googleplay': 'https://play.google.com/store/apps/details?id=',
	'huawei': 'http://appstore.huawei.com/app/'
	}
	
	for key, val in dict.items():
		url_set = set()
		if key != 'huawei': continue
		for root_url in val:
			while True:
				try:
					web = request.urlopen(root_url, timeout=20)
					charset = str(web.headers.get_content_charset())
					if charset == "None": charset = "utf-8"
					data = web.read().decode(charset)
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
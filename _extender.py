# -*- coding:utf-8 -*-

import re

def get_extend_urls(market, data, prefix):
	urls = set()
	if market == 'yingyongbao':
		matcher = re.findall('<a href="../myapp/detail.htm\?apkName=.*?"', data)
		for url in matcher:
			full_url = 'http://sj.qq.com'+re.subn('\&(.+)', "", url.replace('"', "").replace('<a href=..', ""))[0]
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
				
	if market == '360':
		matcher = re.findall('<h2>本类热门应用</h2>.*?<script', data, re.S)
		if len(matcher):
			matcher = re.findall('href="/detail/index/soft_id/[0-9]+', matcher[0])
			for url in matcher:
				full_url = 'http://zhushou.360.cn'+url.replace('href="', "")
				if full_url.startswith(prefix): urls.add(full_url.replace(prefix, ""))
	
	return urls
# -*- coding:utf-8 -*-

from urllib import request
from selenium import webdriver
from _googleplayapi import GooglePlayAPI
import urllib, time, requests, re

def get_apk_download_link(market, data, url):
	if market == 'yingyongbao':
		matcher = re.findall('data-apkurl=".*?"', data)
		if len(matcher): return matcher[0].replace('data-apkurl="', "").replace('"', "")
		
	elif market == 'baidu':
		matcher = re.findall('<span class="one-setup-btn".*?data_url=".*?"', data, re.S)
		if len(matcher): return re.subn('<span class="one-setup-btn".*?data_url="', "", matcher[0].replace("\r", "").replace("\n", ""))[0].replace('"', "")
		
	elif market == '360':
		matcher = re.findall('url=.*?.apk" data-sid=', data)
		if len(matcher): return matcher[0].replace('url=', "").replace('" data-sid=', "")
		
	elif market == 'googleplay':
		return url
		
	elif market == 'huawei':
		matcher = re.findall('dlurl=".*?"', data)
		if len(matcher): return matcher[0].replace('dlurl="', "").replace('"', "")
		
	elif market == 'xiaomi':
		matcher = re.findall('<div class="app-info-down"><a href=".*?"', data)
		if len(matcher): return 'http://app.mi.com'+matcher[0].replace('<div class="app-info-down"><a href="', "").replace('"', "")
		
	elif market == 'wandoujia':
		return url+"/download"
		
	elif market == 'hiapk':
		matcher = re.findall('<a href="/appdown/.*?" class="link_btn"', data)
		if len(matcher): return 'http://apk.hiapk.com'+matcher[0].replace('<a href="', "").replace('" class="link_btn"', "")
		
	elif market == 'anzhi':
		matcher = re.findall('<a href="#" onclick="opendown\([0-9]+\);"', data)
		if len(matcher): return 'http://www.anzhi.com/dl_app.php?s='+matcher[0].replace('<a href="#" onclick="opendown(', "").replace(');"', "")+'&n=5'

	return ""
	
def get_icon_download_link(market, data):
	if market == 'yingyongbao':
		matcher = re.findall('<div class="det-icon">.*?src=".*?"', data, re.S)
		if len(matcher): return matcher[0].split('"')[-2]
	
	elif market == 'baidu':
		matcher = re.findall('<div class="app-pic">.*?=".*?"', data, re.S)
		if len(matcher): return matcher[0].split('"')[-2]
		
	elif market == '360':
		matcher = re.findall('<dt>.*?<img src=".*?"', data, re.S)
		if len(matcher): return matcher[0].split('"')[-2]
		
	elif market == 'googleplay':
		matcher = re.findall('<img class="cover-image" src=".*?"', data)
		if len(matcher): return 'https:'+matcher[0].split('"')[-2]
		
	elif market == 'huawei':
		matcher = re.findall('img class="app-ico" lazyload=".*?"', data)
		if len(matcher): return matcher[0].split('"')[-2]
		
	elif market == 'xiaomi':
		matcher = re.findall('<img class="yellow-flower" src=".*?"', data)
		if len(matcher): return matcher[0].split('"')[-2]
		
	elif market == 'wandoujia':
		matcher = re.findall('<img src=".*?" itemprop="image" width="110" height="110"', data)
		if len(matcher): return matcher[0].split('"')[-8]
		
	elif market == 'hiapk':
		matcher = re.findall('<img.*?src=".*?".*?ICON"', data)
		if len(matcher):
			matcher = re.findall('src=".*?"', matcher[0])
			if len(matcher): return matcher[0].split('"')[-2]
			
	elif market == 'anzhi':
		matcher = re.findall('var ICON="http://.*?";', data)
		if len(matcher): return matcher[0].split('"')[-2]
		
	return ""

def download_apk(market, url, apkfile, config):
	if market != 'googleplay':
		if not len(url): return False
		for i in range(10):
			try:
				web = requests.get(url, stream=True, timeout=30)
				with open(apkfile, 'wb') as fout:
					for chunk in web.iter_content(chunk_size=204800):
						if chunk:
							fout.write(chunk)
							fout.flush()
				fout.close()
				return True
			except:
				continue
	else:
		if not len(url): return False
		packagename = url.split("=")[1]
		for i in range(10):
			try:
				api = GooglePlayAPI(config['ANDROID_ID'])
				api.login(config['GOOGLE_LOGIN'], config['GOOGLE_PASSWORD'])
				m = api.details(packagename)
				doc = m.docV2
				vc = doc.details.appDetails.versionCode
				ot = doc.offer[0].offerType
				if api.download(packagename, vc, ot, apkfile): return True
			except:
				continue
		
	return False
	
def download_icon(market, url, pngfile):
	if not len(url):
		return False
	else:
		for i in range(10):
			try:
				web = requests.get(url, stream=True, timeout=30)
				with open(pngfile, 'wb') as fout:
					for chunk in web.iter_content(chunk_size=204800):
						if chunk:
							fout.write(chunk)
							fout.flush()
				fout.close()
				return True
			except:
				continue
	return False
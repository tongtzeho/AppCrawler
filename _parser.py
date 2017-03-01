# -*- coding:utf-8 -*-

import re

from _unescaper import *

def get_app_basic_info(market, data):
	dict = {}
	if market == 'yingyongbao':
		matcher = re.findall("det-name-int\">.*?</div>", data)
		if len(matcher): dict['Name'] = unescape(matcher[0].replace("det-name-int\">", "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall("det-ins-num\">.*?下载</div>", data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('det-ins-num">', "").replace('下载</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('det-size">.*?</div>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('det-size">', "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('star-num">.*?分</div>', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace('star-num">', "").replace('分</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<a href="#CommentList" id="J_CommentCount">（[0-9]*人评论）</a>', data)
		if len(matcher): dict['Rating_Num'] = unescape(matcher[0].replace('<a href="#CommentList" id="J_CommentCount">（', "").replace('人评论）</a>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('id="J_DetCate">.*?</a>', data)
		if len(matcher): dict['Category'] = unescape(matcher[0].replace('id="J_DetCate">', "").replace('</a>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('det-othinfo-tit">版本号：</div>.*?det-othinfo-data">.*?</div>', data, re.S)
		if len(matcher):
			matcher = re.findall('othinfo-data">.*?</div>', matcher[0])
			if len(matcher): dict['Edition'] = unescape(matcher[0].replace('othinfo-data">', "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('det-othinfo-tit">开发商：</div>.*?det-othinfo-data">.*?</div>', data, re.S)
		if len(matcher):
			matcher = re.findall('othinfo-data">.*?</div>', matcher[0])
			if len(matcher): dict['Developer'] = unescape(matcher[0].replace('othinfo-data">', "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))		
		matcher = re.findall('data-apkpublishtime="[0-9]*">.*?</div>', data)
		if len(matcher):
			matcher = re.findall('[0-9]*年[0-9]*月[0-9]*日', matcher[0])
			if len(matcher): dict['Update_Time'] = matcher[0]
		if 'adv-btn_has">有广告' in data: dict['Has_Ads'] = 'True'
		elif 'adv-btn">无广告' in data: dict['Has_Ads'] = 'False'
			
	elif market == 'baidu':
		matcher = re.findall('<span class="gray">.*?</span>', data)
		if len(matcher): dict['Name'] = unescape(matcher[0].replace('<span class="gray">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('class="download-num">下载次数: .*?</span>', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('class="download-num">下载次数: ', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('class="size">大小: .*?</span>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('class="size">大小: ', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('class="star-percent" style="width:[0-9]*%">', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace('class="star-percent" style="width:', "").replace('%">', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<a target="_self" href="/.*?/">.*?</a>', data)
		if len(matcher) >= 2:
			type0 = re.subn('<a target="_self" href="/.*?/">', "", unescape(matcher[0].replace('</a>', "")))[0]
			type1 = re.subn('<a target="_self" href="/.*?/">', "", unescape(matcher[1].replace('</a>', "")))[0]
			dict['Category'] = type0+"-"+type1
		matcher = re.findall('class="version">版本: .*?</span>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('class="version">版本: ', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))		
		
	elif market == '360':
		matcher = re.findall('<span title=".*?">', data)
		if len(matcher): dict['Name'] = unescape(matcher[0].replace('<span title="', "").replace('">', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="s-3">下载：.*?次</span>', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('<span class="s-3">下载：', "").replace('次</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="s-3">[0-9\.a-zA-Z]+</span>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<span class="s-3">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="s-1 js-votepanel">[0-9\.]+<em>', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace('<span class="s-1 js-votepanel">', "").replace('<em>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="vote-num">.*?</span>', data)
		if len(matcher): dict['Rating_Num'] = unescape(matcher[0].replace('<span class="vote-num">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>[Na0-9]+<span>', data)
		if len(matcher) >= 5:
			dict['5-Star_Rating_Num'] = unescape(matcher[0].replace('<li>', "").replace('<span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['4-Star_Rating_Num'] = unescape(matcher[1].replace('<li>', "").replace('<span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['3-Star_Rating_Num'] = unescape(matcher[2].replace('<li>', "").replace('<span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['2-Star_Rating_Num'] = unescape(matcher[3].replace('<li>', "").replace('<span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['1-Star_Rating_Num'] = unescape(matcher[4].replace('<li>', "").replace('<span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="review-count-all">(.*?)</span>', data)
		if len(matcher): dict['Comment_Num'] = unescape(matcher[0].replace('<span class="review-count-all">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace('(', "").replace(')', ""))
		matcher = re.findall('<span class="review-count-best">(.*?)</span>', data)
		if len(matcher): dict['Best_Comment_Num'] = unescape(matcher[0].replace('<span class="review-count-best">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace('(', "").replace(')', ""))
		matcher = re.findall('<span class="review-count-good">(.*?)</span>', data)
		if len(matcher): dict['Good_Comment_Num'] = unescape(matcher[0].replace('<span class="review-count-good">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace('(', "").replace(')', ""))
		matcher = re.findall('<span class="review-count-bad">(.*?)</span>', data)
		if len(matcher): dict['Bad_Comment_Num'] = unescape(matcher[0].replace('<span class="review-count-bad">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace('(', "").replace(')', ""))
		if '</span>有广告</li>' in data: dict['Has_Ads'] = 'True'
		elif '</span>无广告</li>' in data: dict['Has_Ads'] = 'False'
		if '</span>免费</li>' in data: dict['Free'] = 'True'
		elif '</span>含支付项</li>' in data: dict['Free'] = 'False'
		matcher = re.findall('权限.*?：[0-9]+.*?</li>', data, re.S)
		if len(matcher):
			matcher = re.findall('[0-9]+', matcher[0])
			if len(matcher): dict['Permission_Num'] = matcher[0]
		matcher = re.findall('"color:#[0-9a-f]+">.*?</a>', data)
		if len(matcher):
			tagall = ""
			for tag in matcher:
				tagall += re.subn('"color:#[0-9a-f]+">', "", unescape(tag.replace('</a>', "").replace('\t', " ").replace('\r', "").replace('\n', " ")))[0]+";"
			dict['Tag'] = tagall[:-1]
		matcher = re.findall('<strong>作者：</strong>.*?<', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('<strong>作者：</strong>', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<strong>更新时间：</strong>.*?<', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<strong>更新时间：</strong>', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<strong>版本：</strong>.*?<', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<strong>版本：</strong>', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<strong>系统：</strong>.*?<', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<strong>系统：</strong>', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<strong>语言：</strong>.*?<', data)
		if len(matcher): dict['Language'] = unescape(matcher[0].replace('<strong>语言：</strong>', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		
	elif market == 'googleplay':
		matcher = re.findall('<div class="id-app-title" tabindex="0">.*?</div>', data)
		if len(matcher): dict['Name'] = unescape(matcher[0].replace('<div class="id-app-title" tabindex="0">', "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="content" itemprop="numDownloads">.*?</div>', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('<div class="content" itemprop="numDownloads">', "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " ")).replace(' ', "")
		matcher = re.findall('<div class="content" itemprop="fileSize">.*?</div>', data)
		if len(matcher): dict['Size'] = unescape(re.subn(' *<.*?> *', "", matcher[0])[0])
		matcher = re.findall('<div class="score" aria-label=".*?">[0-9\.]+</div>', data)
		if len(matcher): dict['Rating'] = re.subn('<.*?>', "", matcher[0])[0]
		matcher = re.findall('<span class="reviews-num" aria-label=".*?">[0-9,]+</span>', data)
		if len(matcher): dict['Rating_Num'] = re.subn('<.*?>', "", matcher[0])[0].replace(",", "")
		matcher = re.findall('<span class="bar-number" aria-label=".*?">[0-9,]+</span>', data)
		if len(matcher) >= 5:
			dict['5-Star_Rating_Num'] = re.subn('<.*?>', "", matcher[0])[0].replace(",", "")
			dict['4-Star_Rating_Num'] = re.subn('<.*?>', "", matcher[1])[0].replace(",", "")
			dict['3-Star_Rating_Num'] = re.subn('<.*?>', "", matcher[2])[0].replace(",", "")
			dict['2-Star_Rating_Num'] = re.subn('<.*?>', "", matcher[3])[0].replace(",", "")
			dict['1-Star_Rating_Num'] = re.subn('<.*?>', "", matcher[4])[0].replace(",", "")
		matcher = re.findall('<span itemprop="genre">.*?</span>', data)
		if len(matcher):
			categoryall = ""
			for category in matcher:
				categoryall += unescape(category.replace('<span itemprop="genre">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))+";"
			dict['Category'] = categoryall[:-1]
		matcher = re.findall('<div class="content" itemprop="softwareVersion">.*?</div>', data)
		if len(matcher): dict['Edition'] = re.subn(' *<.*?> *', "", matcher[0])[0]
		matcher = re.findall('<span itemprop="name">.*?</span>', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('<span itemprop="name">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="content" itemprop="operatingSystems">.*?</div>', data)
		if len(matcher): dict['System'] = unescape(re.subn(' *<.*?> *', "", matcher[0])[0])
		matcher = re.findall('<div class="content" itemprop="datePublished">.*?</div>', data)
		if len(matcher): dict['Update_Time'] = unescape(re.subn(' *<.*?> *', "", matcher[0])[0])
		matcher = re.findall('<div class="content" itemprop="contentRating">.*?</div>', data)
		if len(matcher): dict['Age'] = unescape(re.subn(' *<.*?> *', "", matcher[0])[0])
		matcher = re.findall('</jsl> *</jsl> *<span>.*?</span> *</button>', data)
		if len(matcher): dict['Price'] = unescape(re.subn(' *<.*?> *', "", matcher[0])[0]).replace("安装", "免费").replace("Install", "Free")
		
	elif market == 'huawei':
		matcher = re.findall('<p><span class="title">.*?</span>', data)
		if len(matcher): dict['Name'] = unescape(matcher[0].replace('<p><span class="title">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="grey sub">.*?</span>', data)
		if len(matcher):
			matcher = re.findall('[0-9]+', matcher[0])
			if len(matcher): dict['Download'] = matcher[0]
		matcher = re.findall('<li class="ul-li-detail">大小：<span>.*?</span>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<li class="ul-li-detail">大小：<span>', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="score_[0-9]*">', data)
		if len(matcher):
			matcher = re.findall('[0-9]+', matcher[0])
			if len(matcher): dict['Rating'] = matcher[0]
		matcher = re.findall('（[0-9]+条）:</span>', data)
		if len(matcher):
			matcher = re.findall('[0-9]+', matcher[0])
			if len(matcher): dict['Rating_Num'] = matcher[0]
		matcher = re.findall('<span class="title flt ft-yh">.*?排行<', data)
		if len(matcher): dict['Category'] = unescape(matcher[0].replace('<span class="title flt ft-yh">', "").replace('排行<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li class="ul-li-detail">版本：<span>.*?</span>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<li class="ul-li-detail">版本：<span>', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li class="ul-li-detail">开发者：<span title=\'.*?\'>', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('<li class="ul-li-detail">开发者：<span title=\'', "").replace('\'>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li class="ul-li-detail">日期：<span>.*?</span>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<li class="ul-li-detail">日期：<span>', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		
	elif market == 'xiaomi':
		matcher = re.findall('</p><h3>.*?</h3><p', data)
		if len(matcher): dict['Name'] = unescape(matcher[0].replace('</p><h3>', "").replace('</h3><p', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('软件大小:</li><li>.*?</li>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('软件大小:</li><li>', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="star1-hover star1-[0-9]+', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace('<div class="star1-hover star1-', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('[0-9]+次评分 \)<\/span>', data)
		if len(matcher): dict['Rating_Num'] = unescape(matcher[0].replace('次评分 )</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<b>分类：</b>.*?<span', data)
		if len(matcher): dict['Category'] = unescape(matcher[0].replace('<b>分类：</b>', "").replace('<span', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('版本号：</li><li>.*?</li>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('版本号：</li><li>', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('"intro-titles"><p>.*?</p><h3>', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('"intro-titles"><p>', "").replace('</p><h3>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('更新时间：</li><li>.*?</li>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('更新时间：</li><li>', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<b>支持：</b>.*?</p>', data)
		if len(matcher): dict['Device'] = unescape(matcher[0].replace('<b>支持：</b>', "").replace('</p>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		
	elif market == 'wandoujia':
		matcher = re.findall('<span class="title" itemprop="name">.*?</span>', data)
		if len(matcher): dict['Name'] = unescape(matcher[0].replace('<span class="title" itemprop="name">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('data-install=".*?"', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('data-install="', "").replace('"', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('<meta itemprop="fileSize" content="[0-9]+"/>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<meta itemprop="fileSize" content="', "").replace('"/>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('data-like=".*?"', data)
		if len(matcher): dict['Like_Num'] = unescape(matcher[0].replace('data-like="', "").replace('"', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('<i>[0-9]+</i>[ \n\r\t]*<b>人评论</b>', data, re.S)
		if len(matcher):
			matcher = re.findall('<i>[0-9]+</i>', matcher[0])
			if len(matcher): dict['Comment_Num'] = unescape(matcher[0].replace('<i>', "").replace('</i>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('itemprop="SoftwareApplicationCategory" data-track="detail-click-appTag">.*?</a>', data)
		if len(matcher):
			categoryall = ""
			for category in matcher:
				categoryall += unescape(category.replace('itemprop="SoftwareApplicationCategory" data-track="detail-click-appTag">', "").replace('</a>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))+";"
			dict['Category'] = categoryall[:-1]
		matcher = re.findall('<div class="tag-box">[ \n\r\t]*<a href="http://www.wandoujia.com/tag/.*?">[ \n\r\t]*.*?[ \n\r\t]*</a>[ \n\r\t]*</div>', data, re.S)
		if len(matcher):
			tagall = ""
			for tag in matcher:
				tagall += unescape(re.subn('<.*?>', "", tag)[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))+";"
			dict['Tag'] = tagall[:-1]
		matcher = re.findall('<dt>版本</dt>[ \n\r\t]*<dd>.*?</dd>', data, re.S)
		if len(matcher):
			matcher = re.findall('<dd>.*?</dd>', matcher[0])
			if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<dd>', "").replace('</dd>', "").replace('\t', " ").replace('\r', " ").replace('\n', " "))
		matcher = re.findall('<dt>来自</dt>.*?<dd>.*?</dd>', data, re.S)
		if len(matcher): dict['Developer'] = unescape(re.subn('<.*?>', "", matcher[0].replace("<dt>来自</dt>", ""))[0].replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('datetime=".*?">', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('datetime="', "").replace('">', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<dt>要求</dt>.*?<dd.*?<', data, re.S)
		if len(matcher): dict['System'] = unescape(re.subn(' *<.*?> *', "", matcher[0].replace('<dt>要求</dt>', "").replace('\t', "").replace('\r', "").replace(" ", "").replace('\n', " "))[0].replace('<', ""))
		if '<s class="tag adv-embed"></s>' in data: dict['Has_Ads'] = 'True'
		elif '<s class="tag no-ad"></s>' in data: dict['Has_Ads'] = 'False'
		
	elif market == 'hiapk':
		matcher = re.findall('id="hidAppName" value=".*?">', data)
		if len(matcher): dict['Name'] = unescape(matcher[0].replace('id="hidAppName" value="', "").replace('">', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('>.*?热度</span>', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('热度</span>', "").replace('>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span id="appSize".*?>.*?</span>', data)
		if len(matcher): dict['Size'] = unescape(re.subn('<.*?>', "", matcher[0])[0])
		matcher = re.findall('<div class="star_num">.*?</div>', data, re.S)
		if len(matcher): dict['Rating'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<span id="startCount">[0-9]+</span>', data)
		if len(matcher): dict['Rating_Num'] = unescape(matcher[0].replace('<span id="startCount">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="font14 star_per_font">.*?</div>', data, re.S)
		if len(matcher) == 5:
			dict['5-Star_Rating_Num'] = unescape(matcher[0].replace('<div class="font14 star_per_font">', "").replace('</div>', "").replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
			dict['4-Star_Rating_Num'] = unescape(matcher[1].replace('<div class="font14 star_per_font">', "").replace('</div>', "").replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
			dict['3-Star_Rating_Num'] = unescape(matcher[2].replace('<div class="font14 star_per_font">', "").replace('</div>', "").replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
			dict['2-Star_Rating_Num'] = unescape(matcher[3].replace('<div class="font14 star_per_font">', "").replace('</div>', "").replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
			dict['1-Star_Rating_Num'] = unescape(matcher[4].replace('<div class="font14 star_per_font">', "").replace('</div>', "").replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('类别：</span>.*?</span>', data, re.S)
		if len(matcher): dict['Category'] = unescape(re.subn('<.*?>', "", matcher[0].replace("类别：", ""))[0].replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<div id="appSoftName" class="detail_title left">.*?</div>', data, re.S)
		if len(matcher) and 'Name' in dict: dict['Edition'] = unescape(re.subn('<.*?>', "", matcher[0].replace(dict['Name'], ""))[0].replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", "").replace("(", "").replace(")", ""))
		matcher = re.findall('<span class="d_u_line">.*?</span>', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('<span class="d_u_line">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="font14">上架时间：</span>.*?</span>', data, re.S)
		if len(matcher): dict['Update_Time'] = unescape(re.subn('<.*?>', "", matcher[0].replace("上架时间：", ""))[0].replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<span class="font14 detailMiniSdk d_gj_line left">.*?</span>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<span class="font14 detailMiniSdk d_gj_line left">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="font14">语言：</span>.*?</span>', data, re.S)
		if len(matcher): dict['Language'] = unescape(re.subn('<.*?>', "", matcher[0].replace("语言：", ""))[0].replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
		if '<div class="app_adv adv_result">' in data: dict['Has_Ads'] = 'True'
		elif '<div class="no_adv">' in data: dict['Has_Ads'] = 'False'
		
	elif market == 'anzhi':
		matcher = re.findall('var SOFT_NAME=".*?";', data)
		if len(matcher): dict['Name'] = unescape(matcher[0].replace('var SOFT_NAME="', "").replace('";', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="spaceleft">下载：.*?</span>', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('<span class="spaceleft">下载：', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="spaceleft">大小：.*?</span>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<span class="spaceleft">大小：', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div id="stars_detail" class="stars center" style="background-position:0 -?[0-9]+px;"></div>', data)
		if len(matcher): dict['Rating'] = str(int(abs(int(matcher[0].replace('<div id="stars_detail" class="stars center" style="background-position:0 ', "").replace('px;"></div>', ""))/15)))
		matcher = re.findall('style="position:relative;">评论\([0-9]+\)', data)
		if len(matcher): dict['Rating_Num'] = unescape(matcher[0].replace('style="position:relative;">评论(', "").replace(')', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>分类：.*?</li>', data)
		if len(matcher): dict['Category'] = unescape(matcher[0].replace('<li>分类：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="app_detail_version">.*?</span>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<span class="app_detail_version">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace('(', "").replace(')', ""))
		matcher = re.findall('<li>作者：.*?</li>', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('<li>作者：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>时间：.*?</li>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<li>时间：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>系统：.*?</li>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<li>系统：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		if '<span class="spaceleft">资费：免费</span>' in data: dict['Free'] = 'True'
		
	elif market == '91':
		matcher = re.findall('<h1 class="ff f20 fb fl">.*?</h1>', data, re.S)
		if len(matcher): dict['Name'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('下载次数：.*?\r?\n.*?</li>', data)
		if len(matcher): dict['Download'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace("下载次数：", "").replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<li>文件大小：.*?</li>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<li>文件大小：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="spr star"><a class="w. spr"></a></span><span class="ding spr">', data)
		if len(matcher): dict['Rating'] = matcher[0].replace('<span class="spr star"><a class="w', "").replace(' spr"></a></span><span class="ding spr">', "")
		matcher = re.findall('<span class="ding spr">.*?</span>', data, re.S)
		if len(matcher): dict['Like_Num'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<span class="cai spr">.*?</span>', data, re.S)
		if len(matcher): dict['Dislike_Num'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		_91categorydict = {
		"/game/34_1_5": "休闲娱乐", "/game/44_1_5": "竞速游戏", "/game/36_1_5": "益智游戏", "/game/35_1_5": "射击游戏", "/game/40_1_5": "策略游戏", "/game/42_1_5": "动作游戏",
		"/game/33_1_5": "角色扮演", "/game/41_1_5": "模拟经营", "/game/43_1_5": "体育竞技", "/game/39_1_5": "冒险游戏", "/game/37_1_5": "棋牌天地", "/game/53_1_5": "网络游戏",
		"/game/45_1_5": "格斗游戏", "/game/38_1_5": "情景游戏", "/soft/7_1_5": "系统工具", "/soft/18_1_5": "日常应用", "/soft/27_1_5": "影音媒体", "/soft/29_1_5": "视频软件",
		"/soft/51_1_5": "图书教育", "/soft/6_1_5": "网络应用", "/soft/2_1_5": "即时聊天", "/soft/28_1_5": "音频软件", "/soft/26_1_5": "其他工具", "/soft/48_1_5": "书籍杂志",
		"/soft/49_1_5": "社区交友", "/soft/47_1_5": "生活健康", "/soft/30_1_5": "图像处理", "/soft/17_1_5": "查询参考", "/soft/8_1_5": "系统管理", "/soft/5_1_5": "浏览辅助",
		"/soft/12_1_5": "主题美化", "/soft/16_1_5": "地图导航", "/soft/10_1_5": "安全防范", "/soft/19_1_5": "新闻阅读", "/soft/31_1_5": "照相增强", "/soft/52_1_5": "儿童教学",
		"/soft/15_1_5": "电子词典", "/soft/23_1_5": "时钟日历", "/soft/20_1_5": "理财工具", "/soft/11_1_5": "中文输入", "/soft/3_1_5": "通话辅助", "/soft/25_1_5": "名片管理",
		"/soft/22_1_5": "文档处理", "/soft/9_1_5": "文件管理", "/soft/24_1_5": "日程备忘", "/soft/4_1_5": "短信增强", "/soft/14_1_5": "词典查询", "/soft/21_1_5": "计算工具",
		"/soft/13_1_5": "蓝牙红外", "/soft/1_1_5": "网络通信"
		}
		matcher = re.findall('<a href=".*?" class="more fr">更多>></a>', data)
		if len(matcher):
			categoryid = unescape(matcher[0].replace('<a href="', "").replace('" class="more fr">更多>></a>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			if categoryid in _91categorydict: dict['Category'] = _91categorydict[categoryid]
		matcher = re.findall('<li class="long">热门标签：.*?</li>', data, re.S)
		if len(matcher):
			matcher = re.findall('<a href=.*?>.*?</a>', matcher[0], re.S)
			if len(matcher):
				tagall = ""
				for tag in matcher:
					tagall += unescape(re.subn('<.*?>', "", tag)[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))+";"
				dict['Tag'] = tagall[:-1]
		matcher = re.findall('<li>版本：.+', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<li>版本：', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li class="long">开发商：.*?</li>', data)
		if len(matcher): dict['Developer'] = re.subn('<.*?>', "", unescape(matcher[0].replace('<li class="long">开发商：', "").replace('</li>', " ").replace('\r', "").replace('\n', " ")))[0]
		matcher = re.findall('<li>分享日期：.*?</li>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<li>分享日期：', "").replace('</li>', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>适用固件：.*?</li>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<li>适用固件：', "").replace('</li>', " ").replace('\r', "").replace('\n', " "))
		if '>无广告</em>' in data: dict['Has_Ads'] = 'False'
		elif '>内嵌广告</em>' in data: dict['Has_Ads'] = 'True'

	elif market == 'oppo':
		matcher = re.findall('<div class="soft_info_middle">.*?<h3>.*?</h3>', data, re.S)
		if len(matcher): dict['Name'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('&nbsp;&nbsp;.*?次下载', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('&nbsp;&nbsp;', "").replace('次下载', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>大小：.*?</li>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<li>大小：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="soft_info_nums">.*?<div class="star_[0-9]+"></div>', data, re.S)
		if len(matcher): dict['Rating'] = unescape(re.subn('<.*?>', "", matcher[0].replace('<div class="star_', "").replace('"></div>', ""))[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<span>[0-9]+</span>个评分', data)
		if len(matcher): dict['Rating_Num'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace("个评分", "").replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<li>类别：.*?</li>', data)
		if len(matcher): dict['Category'] = unescape(matcher[0].replace('<li>类别：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>版本：.*?</li>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<li>版本：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>发布时间：.*?</li>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<li>发布时间：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(".", "-"))
		matcher = re.findall('<li>适用系统：.*?</li>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<li>适用系统：', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))

	elif market == 'pp':
		matcher = re.findall('<h1 class="app-title ellipsis" title=".*?">.*?</h1>', data)
		if len(matcher): dict['Name'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<div class="app-downs">.*?下载&nbsp;\|', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('<div class="app-downs">', "").replace('下载&nbsp;|', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('<span class="ellipsis">大[&nbsp;]*小[&nbsp;]*<strong>.*?</strong>', data)
		if len(matcher): dict['Size'] = unescape(re.subn('<.*?<strong>', "", matcher[0])[0].replace('</strong>', "").replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<div class="app-score" title="[0-9\.]+分">', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace('<div class="app-score" title="', "").replace('分">', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="app-comment-count">[0-9]+&nbsp;人评论</div>', data)
		if len(matcher): dict['Comment_Num'] = unescape(matcher[0].replace('<div class="app-comment-count">', "").replace('&nbsp;人评论</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('</h3><div class="app-tag-list clearfix">.*?</div>', data)
		if len(matcher): dict['Tag'] = unescape(re.subn('<.*?>', "", matcher[0].replace("</a>", ";"))[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))[:-1]
		matcher = re.findall('<span class="ellipsis">版[&nbsp;]*本[&nbsp;]*<strong>.*?</strong>', data)
		if len(matcher): dict['Edition'] = unescape(re.subn('<.*?<strong>', "", matcher[0])[0].replace('</strong>', "").replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<span class="ellipsis">更新时间[&nbsp;]+<strong>.*?</strong>', data)
		if len(matcher): dict['Update_Time'] = unescape(re.subn('<.*?<strong>', "", matcher[0])[0].replace('</strong>', "").replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<span class="ellipsis" title=.*?>最低版本[&nbsp;]+<strong>.*?</strong>', data)
		if len(matcher): dict['System'] = unescape(re.subn('<.*?<strong>', "", matcher[0])[0].replace('</strong>', "").replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		if '<span class="icon-done safe-tag">无广告</span>' in data: dict['Has_Ads'] = 'False'

	elif market == 'sogou':
		matcher = re.findall('<p class="name">.*?</p>\n.*?<p class="stars.*/p>', data)
		if len(matcher): dict['Name'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<span>.*?次下载</span>', data)
		if len(matcher): dict['Download'] = unescape(matcher[0].replace('<span>', "").replace('次下载</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('<span>大小：.*?</span>', data)
		if len(matcher): dict['Size'] = unescape(matcher[0].replace('<span>大小：', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('<p class="stars s[0-9]+">', data)
		if len(matcher): dict['Rating'] = unescape(matcher[0].replace('<p class="stars s', "").replace('">', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('<label>分类：</label>.*?</td>', data, re.S)
		if len(matcher):
			matcher = re.findall('<a href=.*?</a>', matcher[0])
			if len(matcher): dict['Category'] = unescape(re.subn('<.*?>', "", matcher[0])[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('<label>标签：</label>.*?</td>', data, re.S)
		if len(matcher):
			matcher = re.findall('<a href=.*?</a>', matcher[0])
			if len(matcher):
				tagall = ""
				for tag in matcher:
					tagall += unescape(re.subn('<.*?>', "", tag)[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))+";"
				dict['Tag'] = tagall[:-1]
		matcher = re.findall('<label>版本：</label>.*?</td>', data)
		if len(matcher): dict['Edition'] = unescape(matcher[0].replace('<label>版本：</label>', "").replace('</td>', "").replace('\t', "").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('<label>更新时间：</label>.*?</td>', data)
		if len(matcher): dict['Update_Time'] = unescape(matcher[0].replace('<label>更新时间：</label>', "").replace('</td>', "").replace('\t', "").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<label>作者：</label>.*?</td>', data)
		if len(matcher): dict['Developer'] = unescape(matcher[0].replace('<label>作者：</label>', "").replace('</td>', "").replace('\t', "").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<label>平台：</label>.*?</td>', data)
		if len(matcher): dict['System'] = unescape(matcher[0].replace('<label>平台：</label>', "").replace('</td>', "").replace('\t', "").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<label>语言：</label>.*?</td>', data)
		if len(matcher): dict['Language'] = unescape(matcher[0].replace('<label>语言：</label>', "").replace('</td>', "").replace('\t', "").replace('\r', "").replace('\n', " ").replace(" ", ""))
		if '<span>免费</span>' in data: dict['Free'] = 'True'
		if '<span>有广告</span>' in data: dict['Has_Ads'] = 'True'
		elif '<span>无广告</span>' in data: dict['Has_Ads'] = 'False'

	return dict

def get_app_permission(market, data):
	list = []
	if market == 'yingyongbao':
		matcher = re.findall('<li class="t">需要调用以下重要权限</li>.*?</ul>', data, re.S)
		if len(matcher):
			matcher = re.findall('<div class="r">.*?</div></li>', matcher[0])
			for permission in matcher:
				list.append(unescape(permission.replace('<div class="r">', "").replace('</div></li>', "")))
				
	elif market == 'googleplay':
		matcher = re.findall('<li jstcache="[0-9]+" jsinstance="[\*0-9]+">.*?</li>', data)
		if len(matcher):
			for permission in matcher:
				list.append(unescape(re.subn('<.*?>', "", permission)[0]))
				
	elif market == 'xiaomi':
		matcher = re.findall('<li>▪ .*?</li>', data)
		if len(matcher):
			for permission in matcher:
				list.append(unescape(permission.replace('<li>▪ ', "").replace('</li>', "")))

	elif market == 'wandoujia':
		matcher = re.findall('<li><span class="perms" itemprop="permissions">.*?</span></li>', data)
		if len(matcher):
			for permission in matcher:
				list.append(unescape(permission.replace('<li><span class="perms" itemprop="permissions">', "").replace('</span></li>', "")))

	elif market == 'pp':
		matcher = re.findall('<div class="permission-list none"><p>该应用需要以下重要权限：</p><ul class="clearfix">.*?</div>', data)
		if len(matcher):
			matcher = re.findall('<li>.*?</li>', matcher[0])
			for permission in matcher:
				list.append(unescape(permission.replace('<li>', "").replace('</li>', "")))
	
	return tuple(set(list))
	
def get_app_description(market, data):
	if market == 'yingyongbao':
		matcher = re.findall('<div class="det-intro-tit">应用信息</div>.*?</div>[ |\n|\r|\t]*</div>', data, re.S)
		if len(matcher):
			matcher1 = re.findall('.*?<div class="det-app-data-tit">更新内容：</div>', matcher[0], re.S)
			if len(matcher1):
				tmp0 = re.subn('<.*?>', '', matcher1[0].replace('<div class="det-intro-tit">应用信息</div>', "").replace('<div class="det-app-data-tit">更新内容：</div>', "").replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
				tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
				tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
				if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
				else: return tmp2
			else:
				tmp0 = re.subn('<.*?>', '', matcher[0].replace('<div class="det-intro-tit">应用信息</div>', "").replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
				tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
				tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
				if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
				else: return tmp2
			
	elif market == 'baidu':
		matcher = re.findall('<div class="brief-long".*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<a href="javascript:;" target="_self" class="fold">收起</a>', "").replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == '360':
		matcher = re.findall('<div class="breif">.*?<div', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<div class="breif">', "").replace('<div', "").replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'googleplay':
		matcher = re.findall('<h1 aria-label=".*?"></h1>.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'huawei':
		matcher = re.findall('<div id="app_desc" style="display:none;">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
	
	elif market == 'xiaomi':
		matcher = re.findall('<h3>应用介绍</h3><p class="pslide">.*?</p>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<h3>应用介绍</h3><p class="pslide">', "").replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'wandoujia':
		matcher = re.findall('<div data-originheight="100" class="con" itemprop="description">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'hiapk':
		matcher = re.findall('<pre id="softIntroduce">.*?</pre>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'anzhi':
		matcher = re.findall('<div class="app_detail_title">简介：</div>.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<div class="app_detail_title">简介：</div>', "").replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == '91':
		matcher = re.findall('<h3 class="h3_txt">内容介绍</h3>.*?</div>.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<h3 class="h3_txt">内容介绍</h3>', "").replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'oppo':
		matcher = re.findall('<input type="hidden" id="soft_description" value=".*?" />', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<input type="hidden" id="soft_description" value="', "").replace('" />', "").replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'pp':
		matcher = re.findall('<div class="app-detail-intro expand-panel">.*?</div>', data)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'sogou':
		matcher = re.findall('<div class="article">\n.*?<div class="textcon">\n.*?<div class="text">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	return ""
	
def get_app_release_note(market, data):
	if market == 'yingyongbao':
		matcher = re.findall('<div class="det-intro-tit">应用信息</div>.*?</div>[ |\n|\r|\t]*</div>', data, re.S)
		if len(matcher):
			matcher1 = re.findall('<div class="det-app-data-tit">更新内容：</div>.*?<div.*?[ |\n|\r|\t]*</div>', matcher[0], re.S)
			if len(matcher1):
				tmp0 = re.subn('<.*?>', '', matcher1[0].replace('<div class="det-app-data-tit">更新内容：</div>', "").replace('<br>', "\n").replace('</div>', "\n"))[0]
				tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
				tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
				if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
				else: return tmp2
				
	elif market == '360':
		matcher = re.findall('<br><b>【更新内容】</b><br>.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<br><b>【更新内容】</b><br>', "").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'googleplay':
		matcher = re.findall('<div class="recent-change">.*?</div>', data, re.S)
		if len(matcher):
			result = ""
			for note in matcher:
				result += unescape(re.subn('<.*?>', "", note)[0].replace('<br>', "\n").replace('</div>', "\n"))+"\n"
			return result
			
	elif market == 'xiaomi':
		matcher = re.findall('<h3 class="special-h3">新版特性</h3><p class="pslide">.*?</p>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<h3 class="special-h3">新版特性</h3><p class="pslide">', "").replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'wandoujia':
		matcher = re.findall('<div data-originheight="100" class="con">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
	
	elif market == 'hiapk':
		matcher = re.findall('<pre class="soft_imprint_font">.*?</pre>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'anzhi':
		matcher = re.findall('<div class="app_detail_title">更新说明：</div>.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<div class="app_detail_title">更新说明：</div>', "").replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'pp':
		matcher = re.findall('<div class="app-detail-log expand-panel">.*?</div>', data)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace("</br>", "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', unescape(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
		
	return ""
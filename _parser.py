# -*- coding:utf-8 -*-

from urllib import request
import urllib, re

def replace_html(s):
	s = s.replace('&quot;','"')
	s = s.replace('&amp;','&')
	s = s.replace('&lt;','<')
	s = s.replace('&gt;','>')
	s = s.replace('&nbsp;',' ')
	s = s.replace('&ldquo;', '“')
	s = s.replace('&rdquo;', '”')
	s = s.replace('&hellip;', '…')
	a = s.replace('&middot;', '·')
	return s

def get_app_basic_info(market, data):
	dict = {}
	if market == 'yingyongbao':
		matcher = re.findall("det-name-int\">.*?</div>", data)
		if len(matcher): dict['Name'] = replace_html(matcher[0].replace("det-name-int\">", "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall("det-ins-num\">.*?下载</div>", data)
		if len(matcher): dict['Download'] = replace_html(matcher[0].replace('det-ins-num">', "").replace('下载</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('det-size">.*?</div>', data)
		if len(matcher): dict['Size'] = replace_html(matcher[0].replace('det-size">', "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('star-num">.*?分</div>', data)
		if len(matcher): dict['Rating'] = replace_html(matcher[0].replace('star-num">', "").replace('分</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<a href="#CommentList" id="J_CommentCount">（[0-9]*人评论）</a>', data)
		if len(matcher): dict['Rating_Num'] = replace_html(matcher[0].replace('<a href="#CommentList" id="J_CommentCount">（', "").replace('人评论）</a>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('id="J_DetCate">.*?</a>', data)
		if len(matcher): dict['Category'] = replace_html(matcher[0].replace('id="J_DetCate">', "").replace('</a>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('det-othinfo-tit">版本号：</div>.*?det-othinfo-data">.*?</div>', data, re.S)
		if len(matcher):
			matcher = re.findall('othinfo-data">.*?</div>', matcher[0])
			if len(matcher): dict['Edition'] = replace_html(matcher[0].replace('othinfo-data">', "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('det-othinfo-tit">开发商：</div>.*?det-othinfo-data">.*?</div>', data, re.S)
		if len(matcher):
			matcher = re.findall('othinfo-data">.*?</div>', matcher[0])
			if len(matcher): dict['Developer'] = replace_html(matcher[0].replace('othinfo-data">', "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))		
		matcher = re.findall('data-apkpublishtime="[0-9]*">.*?</div>', data)
		if len(matcher):
			matcher = re.findall('[0-9]*年[0-9]*月[0-9]*日', matcher[0])
			if len(matcher): dict['Update_Time'] = matcher[0]
		if 'adv-btn_has">有广告' in data: dict['Has_Ads'] = 'True'
		elif 'adv-btn">无广告' in data: dict['Has_Ads'] = 'False'
			
	elif market == 'baidu':
		matcher = re.findall('<span class="gray">.*?</span>', data)
		if len(matcher): dict['Name'] = replace_html(matcher[0].replace('<span class="gray">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('class="download-num">下载次数: .*?</span>', data)
		if len(matcher): dict['Download'] = replace_html(matcher[0].replace('class="download-num">下载次数: ', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('class="size">大小: .*?</span>', data)
		if len(matcher): dict['Size'] = replace_html(matcher[0].replace('class="size">大小: ', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('class="star-percent" style="width:[0-9]*%">', data)
		if len(matcher): dict['Rating'] = replace_html(matcher[0].replace('class="star-percent" style="width:', "").replace('%">', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<a target="_self" href="/.*?/">.*?</a>', data)
		if len(matcher) >= 2:
			type0 = re.subn('<a target="_self" href="/.*?/">', "", replace_html(matcher[0].replace('</a>', "")))[0]
			type1 = re.subn('<a target="_self" href="/.*?/">', "", replace_html(matcher[1].replace('</a>', "")))[0]
			dict['Category'] = type0+"-"+type1
		matcher = re.findall('class="version">版本: .*?</span>', data)
		if len(matcher): dict['Edition'] = replace_html(matcher[0].replace('class="version">版本: ', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))		
		
	elif market == '360':
		matcher = re.findall('<span title=".*?">', data)
		if len(matcher): dict['Name'] = replace_html(matcher[0].replace('<span title="', "").replace('">', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="s-3">下载：.*?次</span>', data)
		if len(matcher): dict['Download'] = replace_html(matcher[0].replace('<span class="s-3">下载：', "").replace('次</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="s-3">[0-9\.a-zA-Z]+</span>', data)
		if len(matcher): dict['Size'] = replace_html(matcher[0].replace('<span class="s-3">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="s-1 js-votepanel">[0-9\.]+<em>', data)
		if len(matcher): dict['Rating'] = replace_html(matcher[0].replace('<span class="s-1 js-votepanel">', "").replace('<em>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="vote-num">.*?</span>', data)
		if len(matcher): dict['Rating_Num'] = replace_html(matcher[0].replace('<span class="vote-num">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li>[Na0-9]+<span>', data)
		if len(matcher) >= 5:
			dict['5-Star_Rating_Num'] = replace_html(matcher[0].replace('<li>', "").replace('<span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['4-Star_Rating_Num'] = replace_html(matcher[1].replace('<li>', "").replace('<span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['3-Star_Rating_Num'] = replace_html(matcher[2].replace('<li>', "").replace('<span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['2-Star_Rating_Num'] = replace_html(matcher[3].replace('<li>', "").replace('<span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
			dict['1-Star_Rating_Num'] = replace_html(matcher[4].replace('<li>', "").replace('<span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="review-count-all">(.*?)</span>', data)
		if len(matcher): dict['Comment_Num'] = replace_html(matcher[0].replace('<span class="review-count-all">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace('(', "").replace(')', ""))
		matcher = re.findall('<span class="review-count-best">(.*?)</span>', data)
		if len(matcher): dict['Best_Comment_Num'] = replace_html(matcher[0].replace('<span class="review-count-best">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace('(', "").replace(')', ""))
		matcher = re.findall('<span class="review-count-good">(.*?)</span>', data)
		if len(matcher): dict['Good_Comment_Num'] = replace_html(matcher[0].replace('<span class="review-count-good">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace('(', "").replace(')', ""))
		matcher = re.findall('<span class="review-count-bad">(.*?)</span>', data)
		if len(matcher): dict['Bad_Comment_Num'] = replace_html(matcher[0].replace('<span class="review-count-bad">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace('(', "").replace(')', ""))
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
				tagall += re.subn('"color:#[0-9a-f]+">', "", replace_html(tag.replace('</a>', "").replace('\t', " ").replace('\r', "").replace('\n', " ")))[0]+";"
			dict['Tag'] = tagall[:-1]
		matcher = re.findall('<strong>作者：</strong>.*?<', data)
		if len(matcher): dict['Developer'] = replace_html(matcher[0].replace('<strong>作者：</strong>', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<strong>更新时间：</strong>.*?<', data)
		if len(matcher): dict['Update_Time'] = replace_html(matcher[0].replace('<strong>更新时间：</strong>', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<strong>版本：</strong>.*?<', data)
		if len(matcher): dict['Edition'] = replace_html(matcher[0].replace('<strong>版本：</strong>', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<strong>系统：</strong>.*?<', data)
		if len(matcher): dict['System'] = replace_html(matcher[0].replace('<strong>系统：</strong>', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<strong>语言：</strong>.*?<', data)
		if len(matcher): dict['Language'] = replace_html(matcher[0].replace('<strong>语言：</strong>', "").replace('<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		
	elif market == 'googleplay':
		matcher = re.findall('<div class="id-app-title" tabindex="0">.*?</div>', data)
		if len(matcher): dict['Name'] = replace_html(matcher[0].replace('<div class="id-app-title" tabindex="0">', "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="content" itemprop="numDownloads">.*?</div>', data)
		if len(matcher): dict['Download'] = replace_html(matcher[0].replace('<div class="content" itemprop="numDownloads">', "").replace('</div>', "").replace('\t', " ").replace('\r', "").replace('\n', " ")).replace(' ', "")
		matcher = re.findall('<div class="content" itemprop="fileSize">.*?</div>', data)
		if len(matcher): dict['Size'] = replace_html(re.subn(' *<.*?> *', "", matcher[0])[0])
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
				categoryall += replace_html(category.replace('<span itemprop="genre">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))+";"
			dict['Category'] = categoryall[:-1]
		matcher = re.findall('<div class="content" itemprop="softwareVersion">.*?</div>', data)
		if len(matcher): dict['Edition'] = re.subn(' *<.*?> *', "", matcher[0])[0]
		matcher = re.findall('<span itemprop="name">.*?</span>', data)
		if len(matcher): dict['Developer'] = replace_html(matcher[0].replace('<span itemprop="name">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="content" itemprop="operatingSystems">.*?</div>', data)
		if len(matcher): dict['System'] = replace_html(re.subn(' *<.*?> *', "", matcher[0])[0])
		matcher = re.findall('<div class="content" itemprop="datePublished">.*?</div>', data)
		if len(matcher): dict['Update_Time'] = replace_html(re.subn(' *<.*?> *', "", matcher[0])[0])
		matcher = re.findall('<div class="content" itemprop="contentRating">.*?</div>', data)
		if len(matcher): dict['Age'] = replace_html(re.subn(' *<.*?> *', "", matcher[0])[0])
		matcher = re.findall('</jsl> *</jsl> *<span>.*?</span> *</button>', data)
		if len(matcher): dict['Price'] = replace_html(re.subn(' *<.*?> *', "", matcher[0])[0]).replace("安装", "免费").replace("Install", "Free")
		
	elif market == 'huawei':
		matcher = re.findall('<p><span class="title">.*?</span>', data)
		if len(matcher): dict['Name'] = replace_html(matcher[0].replace('<p><span class="title">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="grey sub">.*?</span>', data)
		if len(matcher):
			matcher = re.findall('[0-9]+', matcher[0])
			if len(matcher): dict['Download'] = matcher[0]
		matcher = re.findall('<li class="ul-li-detail">大小：<span>.*?</span>', data)
		if len(matcher): dict['Size'] = replace_html(matcher[0].replace('<li class="ul-li-detail">大小：<span>', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<span class="score_[0-9]*">', data)
		if len(matcher):
			matcher = re.findall('[0-9]+', matcher[0])
			if len(matcher): dict['Rating'] = matcher[0]
		matcher = re.findall('（[0-9]+条）:</span>', data)
		if len(matcher):
			matcher = re.findall('[0-9]+', matcher[0])
			if len(matcher): dict['Rating_Num'] = matcher[0]
		matcher = re.findall('<span class="title flt ft-yh">.*?排行<', data)
		if len(matcher): dict['Category'] = replace_html(matcher[0].replace('<span class="title flt ft-yh">', "").replace('排行<', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li class="ul-li-detail">版本：<span>.*?</span>', data)
		if len(matcher): dict['Edition'] = replace_html(matcher[0].replace('<li class="ul-li-detail">版本：<span>', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li class="ul-li-detail">开发者：<span title=\'.*?\'>', data)
		if len(matcher): dict['Developer'] = replace_html(matcher[0].replace('<li class="ul-li-detail">开发者：<span title=\'', "").replace('\'>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<li class="ul-li-detail">日期：<span>.*?</span>', data)
		if len(matcher): dict['Update_Time'] = replace_html(matcher[0].replace('<li class="ul-li-detail">日期：<span>', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		
	elif market == 'xiaomi':
		matcher = re.findall('</p><h3>.*?</h3><p', data)
		if len(matcher): dict['Name'] = replace_html(matcher[0].replace('</p><h3>', "").replace('</h3><p', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('软件大小:</li><li>.*?</li>', data)
		if len(matcher): dict['Size'] = replace_html(matcher[0].replace('软件大小:</li><li>', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<div class="star1-hover star1-[0-9]+', data)
		if len(matcher): dict['Rating'] = replace_html(matcher[0].replace('<div class="star1-hover star1-', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('[0-9]+次评分 \)<\/span>', data)
		if len(matcher): dict['Rating_Num'] = replace_html(matcher[0].replace('次评分 )</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<b>分类：</b>.*?<span', data)
		if len(matcher): dict['Category'] = replace_html(matcher[0].replace('<b>分类：</b>', "").replace('<span', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('版本号：</li><li>.*?</li>', data)
		if len(matcher): dict['Edition'] = replace_html(matcher[0].replace('版本号：</li><li>', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('"intro-titles"><p>.*?</p><h3>', data)
		if len(matcher): dict['Developer'] = replace_html(matcher[0].replace('"intro-titles"><p>', "").replace('</p><h3>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('更新时间：</li><li>.*?</li>', data)
		if len(matcher): dict['Update_Time'] = replace_html(matcher[0].replace('更新时间：</li><li>', "").replace('</li>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<b>支持：</b>.*?</p>', data)
		if len(matcher): dict['Device'] = replace_html(matcher[0].replace('<b>支持：</b>', "").replace('</p>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		
	elif market == 'wandoujia':
		matcher = re.findall('<span class="title" itemprop="name">.*?</span>', data)
		if len(matcher): dict['Name'] = replace_html(matcher[0].replace('<span class="title" itemprop="name">', "").replace('</span>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('data-install=".*?"', data)
		if len(matcher): dict['Download'] = replace_html(matcher[0].replace('data-install="', "").replace('"', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('<meta itemprop="fileSize" content="[0-9]+"/>', data)
		if len(matcher): dict['Size'] = replace_html(matcher[0].replace('<meta itemprop="fileSize" content="', "").replace('"/>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('data-like=".*?"', data)
		if len(matcher): dict['Like_Num'] = replace_html(matcher[0].replace('data-like="', "").replace('"', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('<i>[0-9]+</i>[ \n\r\t]*<b>人评论</b>', data, re.S)
		if len(matcher):
			matcher = re.findall('<i>[0-9]+</i>', matcher[0])
			if len(matcher): dict['Comment_Num'] = replace_html(matcher[0].replace('<i>', "").replace('</i>', "").replace('\t', " ").replace('\r', "").replace('\n', " ").replace(" ", ""))
		matcher = re.findall('itemprop="SoftwareApplicationCategory" data-track="detail-click-appTag">.*?</a>', data)
		if len(matcher):
			categoryall = ""
			for category in matcher:
				categoryall += replace_html(category.replace('itemprop="SoftwareApplicationCategory" data-track="detail-click-appTag">', "").replace('</a>', "").replace('\t', " ").replace('\r', "").replace('\n', " "))+";"
			dict['Category'] = categoryall[:-1]
		matcher = re.findall('<div class="tag-box">[ \n\r\t]*<a href="http://www.wandoujia.com/tag/.*?">[ \n\r\t]*.*?[ \n\r\t]*</a>[ \n\r\t]*</div>', data, re.S)
		if len(matcher):
			tagall = ""
			for tag in matcher:
				tagall += replace_html(re.subn('<.*?>', "", tag)[0].replace('\t', " ").replace('\r', "").replace('\n', "").replace(" ", ""))+";"
			dict['Tag'] = tagall[:-1]
		matcher = re.findall('<dt>版本</dt>[ \n\r\t]*<dd>.*?</dd>', data, re.S)
		if len(matcher):
			matcher = re.findall('<dd>.*?</dd>', matcher[0])
			if len(matcher): dict['Edition'] = replace_html(matcher[0].replace('<dd>', "").replace('</dd>', "").replace('\t', " ").replace('\r', " ").replace('\n', " "))
		matcher = re.findall('<dt>来自</dt>.*?<dd>.*?</dd>', data, re.S)
		if len(matcher): dict['Developer'] = replace_html(re.subn('<.*?>', "", matcher[0].replace("<dt>来自</dt>", ""))[0].replace('\t', "").replace('\r', "").replace('\n', "").replace(" ", ""))
		matcher = re.findall('datetime=".*?">', data)
		if len(matcher): dict['Update_Time'] = replace_html(matcher[0].replace('datetime="', "").replace('">', "").replace('\t', " ").replace('\r', "").replace('\n', " "))
		matcher = re.findall('<dt>要求</dt>.*?<dd.*?<', data, re.S)
		if len(matcher): dict['System'] = replace_html(re.subn(' *<.*?> *', "", matcher[0].replace('<dt>要求</dt>', "").replace('\t', "").replace('\r', "").replace(" ", "").replace('\n', " "))[0].replace('<', ""))
		if '<s class="tag adv-embed"></s>' in data: dict['Has_Ads'] = 'True'
		elif '<s class="tag no-ad"></s>' in data: dict['Has_Ads'] = 'False'

	return dict

def get_app_permission(market, data):
	list = []
	if market == 'yingyongbao':
		matcher = re.findall('<li class="t">需要调用以下重要权限</li>.*?</ul>', data, re.S)
		if len(matcher):
			matcher = re.findall('<div class="r">.*?</div></li>', matcher[0])
			for permission in matcher:
				list.append(replace_html(permission.replace('<div class="r">', "").replace('</div></li>', "")))
				
	elif market == 'googleplay':
		matcher = re.findall('<li jstcache="[0-9]+" jsinstance="[\*0-9]+">.*?</li>', data)
		if len(matcher):
			for permission in matcher:
				list.append(replace_html(re.subn('<.*?>', "", permission)[0]))
				
	elif market == 'xiaomi':
		matcher = re.findall('<li>▪ .*?</li>', data)
		if len(matcher):
			for permission in matcher:
				list.append(replace_html(permission.replace('<li>▪ ', "").replace('</li>', "")))

	elif market == 'wandoujia':
		matcher = re.findall('<li><span class="perms" itemprop="permissions">.*?</span></li>', data)
		if len(matcher):
			for permission in matcher:
				list.append(replace_html(permission.replace('<li><span class="perms" itemprop="permissions">', "").replace('</span></li>', "")))		
	
	return tuple(set(list))
	
def get_app_description(market, data):
	if market == 'yingyongbao':
		matcher = re.findall('<div class="det-intro-tit">应用信息</div>.*?</div>[ |\n|\r|\t]*</div>', data, re.S)
		if len(matcher):
			matcher1 = re.findall('.*?<div class="det-app-data-tit">更新内容：</div>', matcher[0], re.S)
			if len(matcher1):
				tmp0 = re.subn('<.*?>', '', matcher1[0].replace('<div class="det-intro-tit">应用信息</div>', "").replace('<div class="det-app-data-tit">更新内容：</div>', "").replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
				tmp1 = re.subn('( |\t)+', ' ', replace_html(tmp0))[0]
				tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
				if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
				else: return tmp2
			else:
				tmp0 = re.subn('<.*?>', '', matcher[0].replace('<div class="det-intro-tit">应用信息</div>', "").replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
				tmp1 = re.subn('( |\t)+', ' ', replace_html(tmp0))[0]
				tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
				if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
				else: return tmp2
			
	elif market == 'baidu':
		matcher = re.findall('<div class="brief-long".*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<a href="javascript:;" target="_self" class="fold">收起</a>', "").replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', replace_html(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == '360':
		matcher = re.findall('<div class="breif">.*?<div', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<div class="breif">', "").replace('<div', "").replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', replace_html(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'googleplay':
		matcher = re.findall('<h1 aria-label=".*?"></h1>.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', replace_html(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'huawei':
		matcher = re.findall('<div id="app_desc" style="display:none;">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', replace_html(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
	
	elif market == 'xiaomi':
		matcher = re.findall('<h3>应用介绍</h3><p class="pslide">.*?</p>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<h3>应用介绍</h3><p class="pslide">', "").replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', replace_html(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == 'wandoujia':
		matcher = re.findall('<div.*?class="con" itemprop="description">.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', replace_html(tmp0))[0]
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
				tmp1 = re.subn('( |\t)+', ' ', replace_html(tmp0))[0]
				tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
				if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
				else: return tmp2
				
	elif market == '360':
		matcher = re.findall('<br><b>【更新内容】</b><br>.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<br><b>【更新内容】</b><br>', "").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', replace_html(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
			
	elif market == 'googleplay':
		matcher = re.findall('<div class="recent-change">.*?</div>', data, re.S)
		if len(matcher):
			result = ""
			for note in matcher:
				result += replace_html(re.subn('<.*?>', "", note)[0].replace('<br>', "\n").replace('</div>', "\n"))+"\n"
			return result
			
	elif market == 'xiaomi':
		matcher = re.findall('<h3 class="special-h3">新版特性</h3><p class="pslide">.*?</p>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', matcher[0].replace('<h3 class="special-h3">新版特性</h3><p class="pslide">', "").replace('<p>', "\n").replace("<br />", "\n").replace('<br>', "\n").replace('</div>', "\n"))[0]
			tmp1 = re.subn('( |\t)+', ' ', replace_html(tmp0))[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2
		
	return ""
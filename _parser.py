# -*- coding:utf-8 -*-

from urllib import request
import urllib, re

def replace_html(s):
	s = s.replace('&quot;','"')
	s = s.replace('&amp;','&')
	s = s.replace('&lt;','<')
	s = s.replace('&gt;','>')
	s = s.replace('&nbsp;',' ')
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
		
	return dict

def get_app_permission(market, data):
	list = []
	if market == 'yingyongbao':
		matcher = re.findall('<li class="t">需要调用以下重要权限</li>.*?</ul>', data, re.S)
		if len(matcher):
			matcher = re.findall('<div class="r">.*?</div></li>', matcher[0])
			for permission in matcher:
				list.append(replace_html(permission.replace('<div class="r">', "").replace('</div></li>', "")))
	return tuple(list)
	
def get_app_description(market, data):
	if market == 'yingyongbao':
		matcher = re.findall('<div class="det-intro-tit">应用信息</div>.*?</div>[ |\n|\r|\t]*</div>', data, re.S)
		if len(matcher):
			matcher1 = re.findall('.*?<div class="det-app-data-tit">更新内容：</div>', matcher[0], re.S)
			if len(matcher1):
				tmp0 = re.subn('<.*?>', '', replace_html(matcher1[0].replace('<div class="det-intro-tit">应用信息</div>', "").replace('<div class="det-app-data-tit">更新内容：</div>', "").replace('<br>', "\n").replace('</div>', "\n")))[0]
				tmp1 = re.subn('( |\t)+', ' ', tmp0)[0]
				tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
				if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
				else: return tmp2
			else:
				tmp0 = re.subn('<.*?>', '', replace_html(matcher[0].replace('<div class="det-intro-tit">应用信息</div>', "").replace('<br>', "\n").replace('</div>', "\n")))[0]
				tmp1 = re.subn('( |\t)+', ' ', tmp0)[0]
				tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
				if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
				else: return tmp2
			
	elif market == 'baidu':
		matcher = re.findall('<div class="brief-long".*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', replace_html(matcher[0].replace('<a href="javascript:;" target="_self" class="fold">收起</a>', "").replace('<br>', "\n").replace('</div>', "\n")))[0]
			tmp1 = re.subn('( |\t)+', ' ', tmp0)[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	elif market == '360':
		matcher = re.findall('<div class="breif">.*?<div', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', replace_html(matcher[0].replace('<div class="breif">', "").replace('<div', "").replace('<br>', "\n").replace('</div>', "\n")))[0]
			tmp1 = re.subn('( |\t)+', ' ', tmp0)[0]
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
				tmp0 = re.subn('<.*?>', '', replace_html(matcher1[0].replace('<div class="det-app-data-tit">更新内容：</div>', "").replace('<br>', "\n").replace('</div>', "\n")))[0]
				tmp1 = re.subn('( |\t)+', ' ', tmp0)[0]
				tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
				if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
				else: return tmp2
				
	if market == '360':
		matcher = re.findall('<br><b>【更新内容】</b><br>.*?</div>', data, re.S)
		if len(matcher):
			tmp0 = re.subn('<.*?>', '', replace_html(matcher[0].replace('<br><b>【更新内容】</b><br>', "").replace('<br>', "\n").replace('</div>', "\n")))[0]
			tmp1 = re.subn('( |\t)+', ' ', tmp0)[0]
			tmp2 = re.subn('(\r?\n+ *)+', '\n', tmp1)[0]
			if tmp2.startswith('\n') or tmp2.startswith(' '): return tmp2[1:]
			else: return tmp2

	return ""
	
def get_app_download_link(market, data):
	if market == 'yingyongbao':
		matcher = re.findall('data-apkurl=".*?"', data)
		if len(matcher): return matcher[0].replace('data-apkurl="', "").replace('"', "")
		
	elif market == 'baidu':
		matcher = re.findall('<span class="one-setup-btn".*?data_url=".*?"', data, re.S)
		if len(matcher): return re.subn('<span class="one-setup-btn".*?data_url="', "", matcher[0].replace("\r", "").replace("\n", ""))[0].replace('"', "")
		
	elif market == '360':
		matcher = re.findall('url=.*?.apk" data-sid=', data)
		if len(matcher): return matcher[0].replace('url=', "").replace('" data-sid=', "")
		
	return ""
	
def get_icon_download_link(market, data):
	if market == 'yingyongbao':
		matcher = re.findall('<div class="det-icon">.*?src=".*?"', data, re.S)
		if len(matcher): return matcher[0].split('"')[-2]
	
	if market == 'baidu':
		matcher = re.findall('<div class="app-pic">.*?=".*?"', data, re.S)
		if len(matcher): return matcher[0].split('"')[-2]
		
	if market == '360':
		matcher = re.findall('<dt>.*?<img src=".*?"', data, re.S)
		if len(matcher): return matcher[0].split('"')[-2]
		
	return ""
	
#def get_app_special_info(market, url):
#	dict = {}
#	if market == 'yingyongbao':
#		for i in range(10):
#			try:
#				web = request.urlopen(url)
#				data = web.read().decode(web.headers.get_content_charset())
#				if ',"success":true,' in data:
#					matcher = re.findall('"total":[0-9]*,', data)
#					dict['Rating_Num'] = matcher[0].replace('"total":', "").replace(",", "")
#					return dict
#				continue
#			except urllib.error.URLError:
#				print("Internet Error")
#				time.sleep(1)
#				continue
#			except ConnectionResetError:
#				print("Internet Error")
#				time.sleep(1)
#				continue
#	return dict
				
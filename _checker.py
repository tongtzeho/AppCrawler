# -*- coding:utf-8 -*-

import re

def page_invalid(market, data):
	if market == 'yingyongbao':
		return '抱歉，没有找到相关结果，<span id="lastSec">3</span>秒后返回首页</a></div>' in data
	elif market == 'baidu':
		return "<p>请检查您所输入的URL地址是否有误。</p>" in data
	elif market == '360':
		return '<span class="t">获取应用内容失败，请尝试ctrl+f5刷新</span>' in data
	elif market == 'googleplay':
		return '<div id="error-section" class="rounded">We\'re sorry, the requested URL was not found on this server.</div>' in data or '<div id="error-section" class="rounded">抱歉，在此服务器中找不到请求的网址。</div>' in data
	elif market == 'huawei':
		return '<p>欢迎来到火星做客，可惜我们这儿找不到你需要的应用。</p>' in data
	elif market == 'xiaomi':
		return '<title>小米应用商店</title>' in data and '<h1 class="sidebar-h">应用分类</h1>' in data
	elif market == 'wandoujia':
		return '<title>「豌豆荚」官方网站</title>' in data and '<span class="v-m">下载手机版豌豆荚</span>' in data
	elif market == 'hiapk':
		return '<div class="font14 tipline30">您要查看的页面可能已经被删除、名称被更改，或者暂时不可用</div>' in data
	return False	

def check_response(market, result):
	if not len(result): return False
	elif len(result) >= 8 and (not len(result[4]) or not len(result[7])): return False
	if market == 'yingyongbao':
		if not 'Name' in result[0]: return False
		if not 'Download' in result[0]: return False
		if not 'Size' in result[0]: return False
		if not 'Rating' in result[0]: return False
		if not 'Rating_Num' in result[0]: return False
		if not 'Category' in result[0]: return False
		if not 'Edition' in result[0]: return False
		if not 'Developer' in result[0]: return False
		if not 'Update_Time' in result[0]: return False
		if not len(result[1]): return False
		if not len(result[2]): return False
	elif market == 'baidu':
		if not 'Name' in result[0]: return False
		if not 'Download' in result[0]: return False
		if not 'Size' in result[0]: return False
		if not 'Rating' in result[0]: return False
		if not 'Category' in result[0]: return False
		if not 'Edition' in result[0]: return False
		if not len(result[2]): return False
	elif market == '360':
		if not 'Name' in result[0]: return False
		if not 'Download' in result[0]: return False
		if not 'Size' in result[0]: return False
		if not 'Rating' in result[0]: return False
		if not 'Rating_Num' in result[0]: return False
		if not 'Edition' in result[0]: return False
		if not 'Developer' in result[0]: return False
		if not 'Update_Time' in result[0]: return False
		if not '5-Star_Rating_Num' in result[0]: return False
		if not '4-Star_Rating_Num' in result[0]: return False
		if not '3-Star_Rating_Num' in result[0]: return False
		if not '2-Star_Rating_Num' in result[0]: return False
		if not '1-Star_Rating_Num' in result[0]: return False
		if not 'Comment_Num' in result[0]: return False
		if not 'Best_Comment_Num' in result[0]: return False
		if not 'Good_Comment_Num' in result[0]: return False
		if not 'Bad_Comment_Num' in result[0]: return False
		if not len(result[2]): return False
	elif market == 'googleplay':
		if not 'Name' in result[0]: return False
		if not 'Download' in result[0]: return False
		if not 'Rating' in result[0]: return False
		if not 'Rating_Num' in result[0]: return False
		if not 'Category' in result[0]: return False
		if not 'Developer' in result[0]: return False
		if not 'Update_Time' in result[0]: return False
		if not '5-Star_Rating_Num' in result[0]: return False
		if not '4-Star_Rating_Num' in result[0]: return False
		if not '3-Star_Rating_Num' in result[0]: return False
		if not '2-Star_Rating_Num' in result[0]: return False
		if not '1-Star_Rating_Num' in result[0]: return False
		if not 'Age' in result[0]: return False
		if not 'Price' in result[0]: return False
		if not len(result[1]): return False
		if not len(result[2]): return False
	elif market == 'huawei':
		if not 'Name' in result[0]: return False
		if not 'Download' in result[0]: return False
		if not 'Size' in result[0]: return False		
		if not 'Rating' in result[0]: return False
		if not 'Edition' in result[0]: return False
		if not 'Developer' in result[0]: return False
		if not 'Update_Time' in result[0]: return False
		if not len(result[2]): return False	
	elif market == 'xiaomi':
		if not 'Name' in result[0]: return False
		if not 'Size' in result[0]: return False		
		if not 'Rating' in result[0]: return False
		if not 'Rating_Num' in result[0]: return False
		if not 'Category' in result[0]: return False
		if not 'Edition' in result[0]: return False
		if not 'Developer' in result[0]: return False
		if not 'Update_Time' in result[0]: return False
		if not len(result[2]): return False
	elif market == 'wandoujia':
		if not 'Name' in result[0]: return False
		if not 'Download' in result[0]: return False
		if not 'Size' in result[0]: return False
		if not 'Category' in result[0]: return False
		if not 'Edition' in result[0]: return False
		if not 'Developer' in result[0]: return False
		if not 'Update_Time' in result[0]: return False
		if not len(result[2]): return False
	elif market == 'hiapk':
		if not 'Name' in result[0]: return False
		if not 'Download' in result[0]: return False
		if not 'Size' in result[0]: return False
		if not 'Rating' in result[0]: return False
		if not 'Rating_Num' in result[0]: return False
		if not 'Category' in result[0]: return False
		if not 'Edition' in result[0]: return False
		if not 'Developer' in result[0]: return False
		if not 'Update_Time' in result[0]: return False
		if not len(result[2]): return False 
	return True
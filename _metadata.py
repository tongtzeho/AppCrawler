# -*- coding:utf-8 -*-

import codecs, time, os, pymysql, multiprocessing, threading
from _crawler import open_url
from _crawler import url_prefix
from _database import market_id_dict
from _database import limitlen
from _database import parse_number
from _database import parse_rating
from _database import parse_date

store_item = (
	'Name', 
	'Download', 
	'Rating', 
	'Rating_Num', 
	'5-Star_Rating_Num', 
	'4-Star_Rating_Num', 
	'3-Star_Rating_Num', 
	'2-Star_Rating_Num', 
	'1-Star_Rating_Num', 
	'Category', 
	'Tag', 
	'Edition', 
	'Update_Time',
	'Developer',
	'Description',
	'Release_Note'
)

def connect_mysql():
	try:
		conn = pymysql.connect(host='localhost', port=3306, user='root', password='pkuoslab', db='Metadata', charset='utf8')
		return conn
	except:
		time.sleep(1)
		return None

def parse_response(response, market):
	cmd_dict = {}
	if response[2] != None and len(response[2]): cmd_dict['Description'] = "'"+limitlen(response[2].replace("\\", "\\\\").replace("\r", "").replace("\n", "\\n").replace("\t", "\\t").replace("'", "\\'").replace("\"", "\\\""), 5000)+"'"
	if response[3] != None and len(response[3]): cmd_dict['Release_Note'] = "'"+limitlen(response[3].replace("\\", "\\\\").replace("\r", "").replace("\n", "\\n").replace("\t", "\\t").replace("'", "\\'").replace("\"", "\\\""), 1500)+"'"
	for key, val in response[0].items():
		if key in store_item:
			if key == 'Name': cmd_dict[key] = "'"+limitlen(response[0][key].replace("\\", "\\\\").replace("\r", "").replace("\n", "\\n").replace("\t", "\\t").replace("'", "\\'").replace("\"", "\\\""), 100)+"'"
			elif key == 'Download': cmd_dict[key] = str(parse_number(market, response[0][key]))
			elif key == 'Rating': cmd_dict[key] = str(parse_rating(market, response[0][key]))
			elif key == 'Rating_Num': cmd_dict[key] = str(parse_number(market, response[0][key]))
			elif key == '5-Star_Rating_Num': cmd_dict['Five_Star'] = str(parse_number(market, response[0][key]))
			elif key == '4-Star_Rating_Num': cmd_dict['Four_Star'] = str(parse_number(market, response[0][key]))
			elif key == '3-Star_Rating_Num': cmd_dict['Three_Star'] = str(parse_number(market, response[0][key]))
			elif key == '2-Star_Rating_Num': cmd_dict['Two_Star'] = str(parse_number(market, response[0][key]))
			elif key == '1-Star_Rating_Num': cmd_dict['One_Star'] = str(parse_number(market, response[0][key]))
			elif key == 'Category': cmd_dict[key] = "'"+limitlen(response[0][key].replace("\\", "\\\\").replace("\r", "").replace("\n", "\\n").replace("\t", "\\t").replace("'", "\\'").replace("\"", "\\\""), 40)+"'"
			elif key == 'Tag': cmd_dict[key] = "'"+limitlen(response[0][key].replace("\\", "\\\\").replace("\r", "").replace("\n", "\\n").replace("\t", "\\t").replace("'", "\\'").replace("\"", "\\\""), 120)+"'"
			elif key == 'Edition': cmd_dict[key] = "'"+limitlen(response[0][key].replace("\\", "\\\\").replace("\r", "").replace("\n", "\\n").replace("\t", "\\t").replace("'", "\\'").replace("\"", "\\\""), 30)+"'"
			elif key == 'Update_Time': cmd_dict[key] = parse_date(market, response[0][key])
			elif key == 'Developer': cmd_dict[key] = "'"+limitlen(response[0][key].replace("\\", "\\\\").replace("\r", "").replace("\n", "\\n").replace("\t", "\\t").replace("'", "\\'").replace("\"", "\\\""), 60)+"'"
	return cmd_dict

def update_metadata(response, package, url, market):
	conn = connect_mysql()
	if (conn == None): return -2
	cursor = conn.cursor()
	try:
		marketidstr = market_id_dict[market]
		cmd_dict = parse_response(response, market)
		ifexists = cursor.execute("select * from Metadata where Package_Name='"+package+"' and MarketID="+marketidstr)
		if (ifexists == 0):
			cmd1 = "(Package_Name, MarketID, Url, Time"
			cmd2 = "('"+package[:299]+"', "+marketidstr+", '"+url[:319]+"', "+str(int(time.time()))
			for key, val in cmd_dict.items():
				cmd1 += ', '+key
				cmd2 += ', '+val
			cmd1 += ')'
			cmd2 += ')'
			cursor.execute("insert into Metadata "+cmd1+" values "+cmd2)
			conn.commit()
			return 0
		else:
			old_arr = cursor.fetchall()[0]
			none_num_old = 0
			for field in old_arr:
				if field == None:
					none_num_old += 1
			none_num_new = len(store_item)-len(cmd_dict)
			if none_num_new <= none_num_old:
				cmd = "Time="+str(int(time.time()))
				for key, val in cmd_dict.items():
					cmd += ", "+key+'='+val
				cursor.execute("update Metadata set "+cmd+" where Package_Name='"+package+"' and MarketID="+marketidstr)
				conn.commit()
				return 1
			else:
				return 2
	except:
		return -1

def read_url_pair(url_pair_file):
	if not os.path.isfile(url_pair_file):
		return None
	result = []
	fin = codecs.open(url_pair_file, 'r', 'utf-8')
	for line in fin:
		if len(line.split(' ')) == 2:
			result.append(line)
	fin.close()
	return tuple(result)

def main_loop(threadidstr, market, thread_num, url_pkg_tuple):
	while True:
		url_pkg_index = int(threadidstr)
		while url_pkg_index < len(url_pkg_tuple):
			url_pkg = url_pkg_tuple[url_pkg_index]
			url_pkg_index += thread_num
			if os.path.isfile('md_exit'):
				print (market+threadidstr+'('+str(url_pkg_index)+'/'+str(len(url_pkg_tuple))+')'+"：结束")
				return
			try:
				url = url_prefix[market]+url_pkg.split(' ')[0]
				package = url_pkg.split(' ')[1].replace('\r', '').replace('\n', '')
			except:
				print (market+threadidstr+'('+str(url_pkg_index)+'/'+str(len(url_pkg_tuple))+')'+"：链接格式错误（"+url_pkg+"）")
				continue
			print (market+threadidstr+'('+str(url_pkg_index)+'/'+str(len(url_pkg_tuple))+')'+"：开始连接（"+url+"）")
			response = open_url(market, url)
			if not len(response):
				print (market+threadidstr+'('+str(url_pkg_index)+'/'+str(len(url_pkg_tuple))+')'+"：无效的链接（"+url+"）")
				continue
			if not len(response[0]):
				print (market+threadidstr+'('+str(url_pkg_index)+'/'+str(len(url_pkg_tuple))+')'+"：访问链接失败（"+url+"）")
				time.sleep(1)
				continue
			state = update_metadata(response, package, url, market)
			if state == -2:
				print (market+threadidstr+'('+str(url_pkg_index)+'/'+str(len(url_pkg_tuple))+')'+"：数据库连接失败")
			elif state == -1:
				print (market+threadidstr+'('+str(url_pkg_index)+'/'+str(len(url_pkg_tuple))+')'+"：数据错误！（"+package+"）")
			elif state == 0:
				print (market+threadidstr+'('+str(url_pkg_index)+'/'+str(len(url_pkg_tuple))+')'+"：新增"+package)
			elif state == 1:
				print (market+threadidstr+'('+str(url_pkg_index)+'/'+str(len(url_pkg_tuple))+')'+"：更新"+package)
			elif state == 2:
				print (market+threadidstr+'('+str(url_pkg_index)+'/'+str(len(url_pkg_tuple))+')'+"：更新失败"+package)
		print (market+threadidstr+"：完成！")

def initialization(param):
	market = param[0]
	root = param[1]
	thread_num = param[2]
	print ("初始化进程：("+market+", "+str(thread_num)+")")
	url_pkg_tuple = read_url_pair(root+market+"_url_pair.txt")
	threads = []
	for i in range(1, thread_num):
		threads.append(threading.Thread(target=main_loop, args=(str(i), market, thread_num, url_pkg_tuple)))
	for t in threads:
		t.start()
	main_loop('0', market, thread_num, url_pkg_tuple)
	for t in threads:
		t.join()
	print ("进程"+market+"退出")
	
if __name__ == '__main__':
	if not os.path.isfile("metadata.txt"): exit()
	if os.path.isfile('md_exit'): os.remove('md_exit')
	fin_settings = open("metadata.txt", "r")
	market_set = set()
	param_list = []
	for line in fin_settings:
		line = line.replace("\r", "").replace("\n", "")
		if line.startswith('#') or len(line.split(' ')) < 3: continue
		market = line.split(' ')[0]
		root = line.split(' ')[1]
		thread_num = int(line.split(' ')[2].replace('\r', "").replace('\n', ""))
		if market in market_set: exit()
		if market in market_id_dict:
			market_set.add(market)
			param_list.append((market, root, thread_num))
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
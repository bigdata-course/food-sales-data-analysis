#!/usr/bin/env python
# -*- coding: utf-8 -*-
f = open('hotel_daily.csv')
f2 = open('hotel_predict','w')

st = f.readline()
f2.write('id,hotel_id,the_date,dayofweek,total_need_money\n')
while st:
	st = f.readline()
	if st:
		st = st.strip('\n').split(',')
		the_date = '2016-7-1'
		dayofweek = '星期五'
		s = [st[0],st[1],the_date,dayofweek,'0\n']
		f2.write(','.join(s))
		the_date = '2016-7-2'
		dayofweek = '星期六'
		s = [st[0],st[1],the_date,dayofweek,'0\n']
	        f2.write(','.join(s))
		the_date = '2016-7-3'
	        dayofweek = '星期日'
		s = [st[0],st[1],the_date,dayofweek,'0\n']
	        f2.write(','.join(s))
		the_date = '2016-7-4'
	        dayofweek = '星期一'
	        s = [st[0],st[1],the_date,dayofweek,'0\n']
	        f2.write(','.join(s))
		the_date = '2016-7-5'
	        dayofweek = '星期二'
        	s = [st[0],st[1],the_date,dayofweek,'0\n']
       	 	f2.write(','.join(s))
		the_date = '2016-7-6'
	        dayofweek = '星期三'
	        s = [st[0],st[1],the_date,dayofweek,'0\n']
	        f2.write(','.join(s))
		the_date = '2016-7-7'
	        dayofweek = '星期四'
	        s = [st[0],st[1],the_date,dayofweek,'0\n']
	        f2.write(','.join(s))
f.close()
f2.close()
f = open('food_daily.csv')
f2= open('food_predict','w')
st = f.readline()
f2.write('hotel_id,food_id,cate_code,unit_money,check_date,dayofweek,total_num\n')
strs = []
while st:
	st = f.readline()
	if st:
		st = st.strip('\n').split(',')
		if st[1]+st[3] in strs:
			continue
		strs.append(st[1]+st[3])
		the_date = '2016-7-1'
                dayofweek = '星期五'
                s = [st[1],st[3],st[5],st[7],the_date,dayofweek,'0\n']
                f2.write(','.join(s))
                the_date = '2016-7-2'
                dayofweek = '星期六'
                s = [st[1],st[3],st[5],st[7],the_date,dayofweek,'0\n']
                f2.write(','.join(s))
                the_date = '2016-7-3'
                dayofweek = '星期日'
                s = [st[1],st[3],st[5],st[7],the_date,dayofweek,'0\n']
                f2.write(','.join(s))
                the_date = '2016-7-4'
                dayofweek = '星期一'
                s = [st[1],st[3],st[5],st[7],the_date,dayofweek,'0\n']
                f2.write(','.join(s))
                the_date = '2016-7-5'
                dayofweek = '星期二'
                s = [st[1],st[3],st[5],st[7],the_date,dayofweek,'0\n']
                f2.write(','.join(s))
                the_date = '2016-7-6'
                dayofweek = '星期三'
                s = [st[1],st[3],st[5],st[7],the_date,dayofweek,'0\n']
                f2.write(','.join(s))
                the_date = '2016-7-7'
                dayofweek = '星期四'
                s = [st[1],st[3],st[5],st[7],the_date,dayofweek,'0\n']
                f2.write(','.join(s))
f.close()
f2.close()
'''
f= open('food_predict')
st = f.readline()
while st:
	st = f.readline()
	if st:
		st = st.strip('\n').split(',')
f.close()
'''

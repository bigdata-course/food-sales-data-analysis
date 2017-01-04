#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
def readCSV_hotel():
	cluster = "data2/hotel.csv"
	hotel = pd.read_csv(cluster)
	hotel = hotel.filter(regex='hotel_id|caixi|format|fast_hotel|num_of_table|num_of_seat|num_of_waiter|num_of_foodcate|num_of_food|num_of_member|num_of_printer|num_of_printer_net|num_of_printer_drv')
	fast_hotel = hotel.drop_duplicates(['fast_hotel'])['fast_hotel']
	i = 0
	for f in fast_hotel:
		hotel.loc[ hotel.fast_hotel==f,'fast_hotel' ]= i
		i+=1
	format = hotel.drop_duplicates(['format'])['format']
	i=0
	for c in format:
		hotel.loc[ hotel.format==c,'format']=i
		i+=1
	caixi = hotel.drop_duplicates(['caixi'])['caixi']
	i=0
	for c in caixi:
		hotel.loc[ hotel.caixi==c,'caixi']=i
		i+=1
	cluster = "data2/hotel_daily.csv"
	cluster = pd.read_csv(cluster)
	cluster = cluster.filter(regex="hotel_id|dayofweek|total_need_money|the_date")
	#hotel = pd.concat([hotel,cluster], axis=1, join_axes=["hotel_id"])
	#cluster = pd.concat([cluster,hotel], axis=1)#,ignore_index=True)
	
	test = "data2/hotel_predict"
	test = pd.read_csv(test)
	test = test.filter(regex="hotel_id|dayofweek|total_need_money|the_date")
	#test = pd.concat([test,hotel], axis=1)#,ignore_index=True)
	dayofweek = test.drop_duplicates(['dayofweek'])['dayofweek']
	i=0
	for c in dayofweek:
		test.loc[test.dayofweek==c,'dayofweek']=i
		cluster.loc[cluster.dayofweek==c,'dayofweek']=i
		i+=1
	
	cluster = pd.merge(cluster,hotel,on='hotel_id')
	test = pd.merge(test,hotel,on='hotel_id')
	return (cluster,test)

def readCSV_food():
	food = "data2/food_daily.csv"
	food = pd.read_csv(food)
	food = food.filter(regex='hotel_id|food_id|unit_money|cate_code|dayofweek|total_num|check_date')#|total_money')
	test = "data2/food_predict"
	test = pd.read_csv(test,index_col=False)
	test = test.filter(regex='hotel_id|food_id|unit_money|cate_code|dayofweek|total_num|check_date')
	dayofweek = test.drop_duplicates(['dayofweek'])['dayofweek']
        i=0
        for c in dayofweek:
                test.loc[test.dayofweek==c,'dayofweek']=i
                food.loc[food.dayofweek==c,'dayofweek']=i
                i+=1
	return food,test

def clusters_test(hotel):
	import matplotlib.pyplot as plt
        from sklearn.cluster import KMeans
        scores = []
        for i in xrange(3,80,1):
                km = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=1,verbose=False)
                km.fit(hotel)
                scores.append(-km.score(hotel)/len(hotel))
	for a,b in zip(scores,xrange(3,80,1)):
		print b,a
        plt.figure(figsize=(8,4))
        plt.plot(xrange(3,80,1),scores,label="error",color="red",linewidth=1)
        plt.xlabel("n_features")
        plt.ylabel("error")
        plt.legend()
        plt.show()

def clusters(hotel):
	from sklearn.cluster import KMeans
	random_state = 170
	y_pred = KMeans(n_clusters=5, random_state=random_state).fit_predict(hotel)
	return y_pred

def regression_test(X,Y,testx):
	from sklearn.linear_model import LinearRegression
	from sklearn import cross_validation
	from sklearn.model_selection import cross_val_score
	from sklearn.metrics import mean_squared_error
	from math import sqrt
	X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y, test_size=0.4, random_state=0)
	print 'Linear'
	clf = LinearRegression()
	clf.fit(X_train,y_train)
	res = 0  
	#for a,b in zip(list(y_test),clf.predict(X_test)):
	#	res+=np.log(a)-np.log(b)	
	print sqrt(mean_squared_error(list(y_test),clf.predict(X_test)))
	#print cross_val_score(clf, X, Y, cv=10)
	from sklearn.tree import DecisionTreeRegressor
	print 'Decision'
	clf = DecisionTreeRegressor(random_state=0)
	clf.fit(X_train,y_train)
	print sqrt(mean_squared_error(list(y_test),clf.predict(X_test)))
	#print cross_val_score(clf, X, Y, cv=10)
	
def regression(x,y,testx):
	from sklearn.linear_model import LinearRegression
	lr = LinearRegression()
	lr.fit(x, y)
	testy = lr.predict(testx)
	return testy

if __name__ == '__main__':
	hotel,hotel_test = readCSV_hotel()
	regex = 'hotel_id|caixi|format|fast_hotel|num_of_table|num_of_seat|num_of_waiter|num_of_foodcate|num_of_food|num_of_member|num_of_printer|num_of_printer_net|num_of_printer_drv'
	'''
	#hotel = hotel.filter(regex=regex)
	#clusters_test(hotel)
	
	hotel_id = hotel.drop_duplicates(['hotel_id'])[0:250]
	hotel = hotel[hotel['hotel_id'].isin(hotel_id['hotel_id'])]
	regexs = regex+'|dayofweek'
	regression_test(hotel.filter(regex=regexs),hotel['total_need_money'],hotel_test.filter(regex=regexs))
	hotel = hotel.filter(regex=regex)
        hotel['cluster'] = clusters(hotel)
	hotel = hotel.filter(regex='hotel_id|cluster').drop_duplicates(['hotel_id'])
	print len(hotel)
	food,food_test = readCSV_food()
	food = food[food['hotel_id'].isin(hotel['hotel_id'])]
        food = pd.merge(food,hotel,on='hotel_id')
	food.to_csv('data2/food_result')
	regression_test(food.filter(regex=regexs),food['total_num'],food_test.filter(regex=regexs))
        regexs = 'hotel_id|food_id|unit_money|cate_code|dayofweek|cluster'
	'''
	regexs = regex+'|dayofweek'
	pred = regression(hotel.filter(regex=regexs),hotel['total_need_money'],hotel_test.filter(regex=regexs))
	hotel_test['total_need_money']=pred
	hotel_test.to_csv('result/hotel.predict')
	hotel = hotel.filter(regex=regex)
	hotel['cluster'] = clusters(hotel)
	hotel = hotel.filter(regex='hotel_id|cluster').drop_duplicates(['hotel_id'])

	food,food_test = readCSV_food()
	food = pd.merge(food,hotel,on='hotel_id')
	food_test = pd.merge(food_test,hotel,on='hotel_id')
	regexs = 'hotel_id|food_id|unit_money|cate_code|dayofweek|cluster'
	#regexs = regex + '|food_id|unit_money|cate_code|dayofweek' 
	#pred = regression(food.filter(regex=regexs),food['total_num'],food_test.filter(regex=regexs))
	pred = regression(food.filter(regex=regexs),food['total_num'],food_test.filter(regex=regexs))
	food_test['total_num']=pred
	food_test.to_csv('result/food.predict')
	#res = pd.concat([hotel,food], axis=1)
	#print res

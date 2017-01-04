#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import pandas as pd
import numpy as np
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report,accuracy_score
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import train_test_split
from cassandra.cluster import Cluster

'''
只测试的时候在main里把train的test改为true
要确定init的strs和features
然后单独python Train.py

1、readcsv
2、processdata
3、trainandsave
4、test
------------------------
实际使用时，先启用index.py

客户端curl 'http://ip:8000?train' or test

train
1、readfromcassandra
2、processdata
3、trainandsave

test
1、readfromcassandra
2、processdata
3、loadclf
4、testandsave
'''
class Train:
	def __init__(self,test = False):
		self.fn = "order_detail.csv"
		self.minOrder = 10
		self.tests = test
		self.strs = ['lr']#TODO
		self.features = 'emp_id'#TODO
		if self.tests is False:
			cluster = Cluster(['192.168.70.67'])
			self.session = cluster.connect('hotel')
		pass

	def readData(self):
		if self.tests :
			self.data = pd.read_csv(self.fn,dtype={'food_name': np.str_,'hotel_id':np.str_},parse_dates=['create_time'])
		else:
			self.data = self.readFromCassandra()
		self.processData()
		self.features = self.data.filter(regex=self.features)
		self.targets = self.data['emp_id']#TODO

	def showData(self,data):
		data.info()
		print data.head()
		pass

	def processData(self):
		'''
		self.data = self.data[['food_name','hotel_id','create_time']]
		if self.test:
			_test_date = pd.to_datetime('2016-6-1')
			self.test = self.data[self.data['create_time'] >= _test_date]
			self.data = self.data[self.data['create_time'] < _test_date]

		for _hotel_id in self.data.drop_duplicates(['hotel_id'])['hotel_id'] :
			_hotel = self.data[self.data.hotel_id == _hotel_id]
			if len(_hotel)<self.minOrder:
				self.showData(_hotel)
				continue
			#a_df = pd.DataFrame(columns=['count'])
		'''
		pass
	
	def test(self,X_test,y_test):
		for i in xrange(0,len(self.strs)):
			clf = self.classifiers[i]
			y_pred = clf.predict(X_test,y_test)
			print 'predict#############################'
			print clf
			print accuracy_score(y_test,y_pred)
			print classification_report(y_test, y_pred)
		
	def testAndSave(self):
		self.data = self.readData()
		self.loadClf()
		for i in xrange(0,len(self.strs)):
			clf = self.classifiers[i]
			y_pred = clf.predict(self.features,self.targets)
			print 'predict#############################'
			saveToCassandra(y_pred)

	def trainAndSave(self):
		self.data = self.readData()
		self.classifiers = [LogisticRegression(C=1, penalty='l2'),KNeighborsClassifier(),RandomForestClassifier(n_estimators=20, class_weight='balanced'),AdaBoostClassifier(),GaussianNB(),DecisionTreeClassifier(max_depth=5)]

		if self.tests:
			self.features, X_test, self.targets, y_test = train_test_split(self.features, self.targets, test_size = .3, random_state=1)
			
		for i in xrange(0,len(self.strs)):
                	print 'fit##################'
                	self.classifiers[i].fit(self.features, self.targets)
			joblib.dump(self.classifiers[i],'result/'+self.strs[i])
		
		if self.tests:	
			self.test(X_test,y_test)

	def loadClf(self):
		for i in xrange(0,len(self.strs)):
			self.classifiers[i] = joblib.load('result/'+self.strs[i])

	def readFromCassandra(self):
		result = self.session.execute("select * from order_detail")
		df = pd.DataFrame({'emp_id':[1],'emp_name':['1']})
		for r in result:
			print r
			df = df.append(r)
		return df

	def saveToCassandra(self,result):
		for index in xrange(result):
			strs='insert into order_detail(result) values ( '+result[index]+' ) where id='+str(index)
			session.execute(strs)
		pass

if __name__ == '__main__':
	train =  Train(filename = 'order_detail.csv',test = True)
	
	train.trainAndSave()

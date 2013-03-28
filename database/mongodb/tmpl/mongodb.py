# -*- coding: utf-8 -*-
""" Класс для работы с MongoDB """
from pymongo import Connection
from bson.objectid import ObjectId
import hashlib
from random import randint

#import wiki.config.config

class MongoDB( object ):
	def __init__( self ):
		self.connection = Connection()
		self.db = self.connection.wiki

	# получает пост по url
	def get_page( self, url = None ):
		try:
			if url is None:
				return None
			# Делаю запрос к БД на получение соответствующего поста
			res = self.db.wiki.find( { 'url' : url } )
			# Произвожу парсинг данных
			post_url = res[0]['url']
			create = res[0]['create']
			update = None
			text = None
			title = None
			for d in res[0]['pages']:
				if d['public'] == 1:
					text = d['text']
					update = d['update']
					title = d['title']
					break
			data = { 'url' : post_url, 'create' : create, 'update' : update, 'text' : text, 'title' : title  }
			return data
		except:
			return None

	# Создает новый документ в MongoDB
	def insert_page( self, url, title, text, comment ):
		res = self.db.wiki.insert( {
						'url': url,
						'title' : title,
						'create': '2013-03-00',
						'pages':[
								{
									'text' : text,
									'url' : url,
									'comment' : comment,
									'update' : '2013-03-00',
									'title' : title,
									'public' : 1,
									'id' : ObjectId()
								 }
							]
						}
					)
	def update_page( self, url_alt, url, title, text, comment ):
		# устанавливаю значение Public в 0
		self.db.wiki.update( { 'url':url, 'pages.public' : 1 }, { '$set' : { 'pages.$.public' : 0 } } )
		# добавляю статью в массив
		self.db.wiki.update( 	{
						'url' : url
					},
					{
						'$push' :{
								'pages' :
								{
									'url' : url,
									'text' : text,
									'comment' : comment,
									'update' : '2013-01-00',
									'title' : title,
									'public': 1,
									'id' : ObjectId()
								}
							}
					}
				 )
	#	self.db.wiki.update( { url } )

	# получает всю историю версий поста
	def getPageHistory( self, url ):
		if url is None:
			return None
		else:
			# Делаю запрос к БД на получение соответствующего поста
			res = self.db.wiki.find( { 'url' : url } )
			# Произвожу парсинг результата, с приведением результата в нормальный вид
			pages = []
			for d in res[0]['pages']:
				if d['public'] == 1:
					d['public'] = 'true'
				else:
					d['public'] = 'false'
				data = {
						'text' : d['text'],
						'title' : d['title'],
						'update' : d['update'],
						'public' : d['public'],
						'size' : len( d['text'] ),
						'comment' : d['comment'],
						'id' : d['id']
					}
				pages.append( data )
			return { 'create' : res[0]['create'], 'id' : res[0]['_id'], 'pages' : pages, 'title' : res[0]['title'] }

	# получает пост с id == id_page из истории
	def getPagePostHistory(  self, url, id_page ):
		res = self.db.wiki.find( { 'url' : url } )
		text = None
		title = None
		update = None
		create = res[0]['create']
		for d in res[0]['pages']:
			if str( d['id'] ) == id_page:
				text = d['text']
				title = d['title']
				update = d['update']
				break
		if text is None:
			return None
		else:
			return { 'text' : text, 'update': update, 'title': title, 'id' : id_page, 'create' : create }

	# Делает активной статью в истории
	def setPageActivityHistory( self, url, id_page ):
		# устанавливаю значение Public в 0
		self.db.wiki.update( { 'url':url, 'pages.public' : 1 }, { '$set' : { 'pages.$.public' : 0 } } )
		# утснавливаю флаг public у новой статьи
		self.db.wiki.update( { 'url':url, 'pages.id' : ObjectId(id_page) }, { '$set' : { 'pages.$.public' : 1 } } )


	# random page
	def getRandomPage( self ):
		 res = self.db.wiki.find()
		 count = res.count()
		 num = randint( 0, count-1 )
		 return res[num]['url']

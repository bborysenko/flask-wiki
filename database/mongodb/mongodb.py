# -*- coding: utf-8 -*-:
""" Класс для работы с MongoDB """

import datetime

from pymongo import Connection
from bson.objectid import ObjectId

class MongoDB( object ):
    def __init__( self ):
		self.connection = Connection()
		self.db = self.connection.wiki

	# получает пост по url
    def get_page( self, url = None ):
        try:
            if url is None:
                return None
            wiki = self.db.wiki.find( { 'url' : url } )

            if wiki is None:
                return None

            page = self.db.pages.find( { '_id' : wiki[0]['page_id'] } )

            return { 'url' : wiki[0]['url'],
                    'text' : page[0]['text'],
                    'title' : page[0]['title'],
                    'tags' : wiki[0]['tags'],
                    'comment' : page[0]['comment'],
                    'access' : wiki[0]['access']
                   }
        except:
            return None
	# Создает новый документ в MongoDB
    def insert_page( self, url, title, text, comment, user, tags, access ):
        arr_t = tags.split(',')
        arr_tags = []
        for d in arr_t:
            elem = d.strip()
            arr_tags.append(elem)

        document_id = self.db.wiki.insert(
                                            {
                                                'url':url,
                                                'title' : title,
                                                'page_id' : None,
                                                'tags': arr_tags,
                                                'user_name':user,
                                                'creation_date': datetime.datetime.now(),
                                                'page_id' : None,
                                                'access' : access
                                            }
                                        )
        page_id = self.db.pages.insert(
                                        {
                                            'tags' : arr_tags,
                                            'url' : url,
                                            'title' : title,
                                            'text' : text,
                                            'creation_date': datetime.datetime.now(),
                                            'user_name' : user,
                                            'comment' : comment,
                                            'wiki_id' : ObjectId(document_id),
                                            'active' : 1
                                        }
                                    )
        self.db.wiki.update( { '_id' : ObjectId(document_id) }, { '$set': {'page_id' : ObjectId(page_id) } } )

    def update_page( self, url_page, url, title, text, comment, tags, user, access ):
        arr_t = tags.split(',')
        arr_tags = []
        for d in arr_t:
            elem = d.strip()
            arr_tags.append(elem)

        # Получаю пост из wiki
        wiki = self.db.wiki.find({ 'url' : url_page })
        # Сохраняю новую запись
        page_id = self.db.pages.insert(
                                    {
                                        'title' : title,
                                        'url' : url,
                                        'tags' : arr_tags,
                                        'text' : text,
                                        'creation_date' : datetime.datetime.now(),
                                        'user_name' : user,
                                        'comment' : comment,
                                        'wiki_id' : ObjectId(wiki[0]['_id']),
                                        'active' : 1
                                    }
                                )
        # Переписываю атрибут active
        self.db.pages.update( { '_id' : ObjectId(wiki[0]['page_id']) }, { '$set' : { 'active' : 0 } } )

        self.db.wiki.update(
                                {
                                    '_id' : ObjectId(wiki[0]['_id'])
                                },
                                {
                                    '$set' :
                                    {
                                        'page_id' : ObjectId(page_id),
                                        'tags' : arr_tags,
                                        'url' : url,
                                        'access' : access,
                                        'title' : title
                                    }
                                }
                            )
	# получает всю историю поста
    def get_pages_history( self, url ):
        if url is None:
            return None
        else:
            wiki = self.db.wiki.find({'url':url})
            data = self.db.pages.find({'wiki_id':ObjectId(wiki[0]['_id'])})#.sort({'creation_date':1})
            posts = []
            for d in data:
                if d['_id'] == wiki[0]['page_id']:
                    d['public'] = True
                else:
                    d['public'] = False

                post = {
                        'text' : d['text'],
                        'title' : d['title'],
                        'creation_date' : d['creation_date'],
                        'public' : d['public'],
                        'size' : len(d['text']),
                        'user' : d['user_name'],
                        'comment' : d['comment'],
                        '_id' : d['_id']
                }
                posts.append(post)

            return {'title': wiki[0]['title'], 'posts':posts}
#            except:
#                return None

	# получает пост с id == id_page из истории
    def get_page_history(  self, id_page ):
        try:
            page = self.db.pages.find( { '_id' : ObjectId( id_page ) } )
            return { 'text' : page[0]['text'], 'title' : page[0]['title'] }
            return page
        except:
            return None

    # Делает активной статью в истории
    def set_activity_history( self, url, id_page ):
        wiki = self.db.wiki.find( { 'url':url } )
        self.db.pages.update( { '_id' : ObjectId(wiki[0]['page_id']) }, { '$set' : { 'active' : 0 } } )
        self.db.wiki.update( { 'url':url  }, { '$set' : { 'page_id' : ObjectId(id_page) } } )
        self.db.pages.update( { '_id' : ObjectId(id_page) }, { '$set' : { 'active' : 1 } } )

	# random page
    def get_random_page( self ):
        pass

    # Поиск страниц по тегу
    def find_page_tags(self, tags):
        try:
            arr_t = tags.split(',')
            arr_tags = []
            for d in arr_t:
                elem = d.strip()
                arr_tags.append(elem)
            pages = []
            for tag in arr_tags:
                wiki = self.db.wiki.find({'tags': tag})
                for d in wiki:
                    key = True
                    # избавляюсь от повторении в выводе
                    for data in pages:
                        if data['_id'] == d['page_id']:
                            key = False
                    if key is True:
                        page = self.db.pages.find({ '_id' : ObjectId(d['page_id'])})
                        pages.append(page[0])

            return pages
        except:
            return None

    # Возвращает все страницы
    def get_all_pages(self, page_num, page_size):
        page_limit = page_size
        page_skip = 0
        if page_num is not None or int(page_num) != 0:
             page_skip = int(page_num) * int(page_size) - int(page_size)

        wiki = self.db.wiki.find().skip(int(page_skip)).limit(int(page_limit))
        pages = []
        for d in wiki:
            page = self.db.pages.find( {'_id':ObjectId(d['page_id'])} )
            pages.append(page[0])
        return pages

    # возвращает колличество записей
    def get_all_count(self):
        return int(self.db.wiki.find().count())

    def get_result_search(self, str_search):
        if str_search is None or str_search == "":
            return None
        data = self.db.command( 'text',
                                'pages',
                                search =  str_search,
                                limit = 200,
                                filter = { 'active' : 1 },
                                language = "Russian"
                            )

        pages = []
        data = data['results']
        for d in data:
            pages.append(d['obj'])

        return pages

    # получить все сообщения для поста
    def get_messages_forum( self, url ):
        wiki = self.db.wiki.find( { 'url' : url } )

        posts = self.db.forum.find( { 'wiki_id' : ObjectId(wiki[0]['_id']) } )

        return posts

    def set_message_forum( self, url, text, user_name ):

        wiki = self.db.wiki.find( { 'url' : url } )

        self.db.forum.insert(
                                {
                                    'user_name' : user_name,
                                    'wiki_id' : ObjectId(wiki[0]['_id']),
                                    'text' : text,
                                    'creation_date' : datetime.datetime.now()
                                }
                            )
    def find_pages(self, letter):
        letter_lower = letter.lower()

        pages = self.db.pages.find( { "active" : 1, "title" :{ "$regex": '^%s' % letter_lower, "$options": 'i' } } )
        return pages

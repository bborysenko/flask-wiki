# -*- coding: utf-8 -*-:
""" Класс для работы с MongoDB """

import datetime

from pymongo import Connection
from bson.objectid import ObjectId

class MongoDB( object ):
    def __init__( self, host, port, database ):
        self.connection = Connection(host = host, port = int(port))
        self.db = self.connection[database]


    # получает пост по url
    def get_page( self, url = None ):
        try:
            if url is None:
                return None
            wiki = self.db.wiki.find_one( { 'url' : url } )

            if wiki is None:
                return None

            page = self.db.pages.find_one( { '_id' : wiki['page_id'] } )
            return {'url' : wiki['url'],
                    'text' : page['text'],
                    'title' : page['title'],
                    'tags' : wiki['tags'],
                    'comment' : page['comment'],
                    'access' : wiki['access']
                    }
        except:
            return None

	# Создает новый документ в MongoDB
    def insert_page( self, url, title, text, comment, user, tags, access ):

        arr_tags = [w.strip(';?!: ') for w in tags.split(',')]

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
                                            'access' : access,
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
        arr_tags = [ w.strip(';?!: ') for w in tags.split(',')]
        # Получаю пост из wiki
        wiki = self.db.wiki.find_one({ 'url' : url_page })
        # Сохраняю новую запись
        page_id = self.db.pages.insert(
                                    {
                                        'title' : title,
                                        'url' : url,
                                        'access' : access,
                                        'tags' : arr_tags,
                                        'text' : text,
                                        'creation_date' : datetime.datetime.now(),
                                        'user_name' : user,
                                        'comment' : comment,
                                        'wiki_id' : ObjectId(wiki['_id']),
                                        'active' : 1
                                    }
                                )
        # Переписываю атрибут active
        self.db.pages.update( { '_id' : ObjectId(wiki['page_id']) }, { '$set' : { 'active' : 0 } } )

        self.db.wiki.update(
                                {
                                    '_id' : ObjectId(wiki['_id'])
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
            wiki = self.db.wiki.find_one({'url':url})
            data = self.db.pages.find({'wiki_id':ObjectId(wiki['_id'])})#.sort({'creation_date':1})
            posts = []
            for d in data:
                if d['_id'] == wiki['page_id']:
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

            return {'title': wiki['title'], 'posts':posts}


	# получает пост с id == id_page из истории
    def get_page_history(  self, url, page_id ):
        try:
            page = self.db.pages.find_one( { '_id' : ObjectId( page_id ) } )
            return { 'text' : page['text'], 'title' : page['title'] }
        except:
            return None

    # Делает активной статью в истории
    def set_activity_history( self, url, page_id ):
        wiki = self.db.wiki.find_one( { 'url':url } )
        self.db.pages.update( { '_id' : ObjectId(wiki['page_id']) }, { '$set' : { 'active' : 0 } } )
        page = self.db.pages.find_one( { '_id' : ObjectId(page_id) } )
        self.db.wiki.update(
                            {
                                'url' : url
                            },
                            {
                                '$set' :
                                {
                                    'page_id' : ObjectId(page_id),
                                    'tags' : page['tags'],
                                    'url' : page['url'],
                                    'access' : page['access'],
                                    'title' : page['title']
                                }
                            }
                        )
        self.db.pages.update( { '_id' : ObjectId(page_id) }, { '$set' : { 'active' : 1 } } )

	# random page
    def get_random_page( self ):
        pass

    # Поиск страниц по тегу
    def find_page_tags(self, tags):
        arr_tags = [ w.strip(';?!: ') for w in tags.split(',')]
        wiki = self.db.wiki.find({'tags' : {'$in':arr_tags}})
        # получаю id статей
        arr_id = [d['page_id'] for d in wiki]
        return self.db.pages.find( { '_id' : { '$in' : arr_id } } )

    # Возвращает все страницы
    def get_all_pages(self, page_num, page_size):
        # нужно для пагинации
        page_limit = page_size
        page_skip = 0
        if page_num is not None or int(page_num) != 0:
             page_skip = int(page_num) * int(page_size) - int(page_size)

        wiki = self.db.wiki.find().skip(int(page_skip)).limit(int(page_limit))
        arr_id = [d['page_id'] for d in wiki]
        return self.db.pages.find( { '_id' : { '$in' : arr_id } } )

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
        return [d['obj'] for d in data['results']]

    # получить все сообщения для поста
    def get_messages_forum( self, url ):
        wiki = self.db.wiki.find_one( { 'url' : url } )
        posts = self.db.forum.find( { 'wiki_id' : ObjectId(wiki['_id']) } )
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

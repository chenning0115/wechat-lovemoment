
#!/usr/bin/env python
# —*- coding:utf-8 -*-
#
# Copyright 2017 charnix
#
#

import sys
sys.path.append('..')
import constants
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId


import logging
logger = logging.getLogger(constants.LOGGING_NAME)
#Mongodb database
db = None
class moments_fileds:
    _id = '_id'
    timestamp = 'timestamp' #系统上传时间戳
    m_date = 'mdate' #故事发生的时间
    author = 'author'
    title = 'title'
    description = 'description'
    pic_urls = 'picurls'
    content = 'content'

def get_connection(database=constants.mongo_dbname):
    global db
    if db is None:
        db = MongoClient(host=constants.mongo_url,port=constants.mongo_port)[database]
    return db

def insert_moment(author='lover',
                  title='Title',
                  mdate = None,
                  description='This is just a test',
                  content="Hello world! This is out first wechat APP, please give me five~ Thank you~",
                  pic_urls=['default.jpg']):
    timestamp = datetime.utcnow()
    if mdate is None:
        mdate = timestamp
    else:
        mdate = datetime.strptime(mdate,"%Y-%m-%d %H:%M:%S")
    doc_data = {
        moments_fileds.timestamp:timestamp,
        moments_fileds.author:author,
        moments_fileds.m_date:mdate,
        moments_fileds.title:title,
        moments_fileds.content:content,
        moments_fileds.description:description,
        moments_fileds.pic_urls:pic_urls
    }
    try:
        db = get_connection()
        _id = db[constants.mongo_table_moments].insert(doc_data)
        logging.info('sucess insert moment %s' % _id)
    except Exception as e:
        logging.info('failed insert moment:%s' % str(e))
        return None
    return _id


def find_moments_sort_by_timestamp(skip_num = 0, limit_num = constants.GET_MOMENTS_NUM_PER_PAGE):
    try:
        db = get_connection()
        res = db[constants.mongo_table_moments].find().sort([(moments_fileds.m_date,-1)])\
            .skip(skip_num).limit(limit_num)
    except Exception as e:
        print(e)
        return None
    reslist = []
    for l in res:
        tempinfo = {}
        tempinfo[moments_fileds._id] = str(l[moments_fileds._id])
        tempinfo[moments_fileds.timestamp] = l[moments_fileds.timestamp].strftime('%b-%d-%y %H:%M:%S')
        tempinfo[moments_fileds.title] = l[moments_fileds.title]
        tempinfo[moments_fileds.m_date] = l[moments_fileds.m_date].strftime('%b-%d-%y %H:%M:%S')
        tempinfo[moments_fileds.pic_urls] = l[moments_fileds.pic_urls]
        tempinfo[moments_fileds.description] = l[moments_fileds.description]
        reslist.append(tempinfo)
    return reslist

def find_by_id(_id=None):
    if _id is not None:
        try:
            db = get_connection()
            res = db[constants.mongo_table_moments].find_one({'_id':ObjectId(_id)})
            res[moments_fileds._id] = str(res[moments_fileds._id])
            res[moments_fileds.m_date] = res[moments_fileds.m_date].strftime('%b-%d-%y %H:%M:%S')
            res[moments_fileds.timestamp] = res[moments_fileds.timestamp].strftime('%b-%d-%y %H:%M:%S')
            return res
        except Exception as e:
            print(e)
            return None


if __name__=='__main__':
    insert_moment()
    print(find_moments_sort_by_timestamp(2,1))
    find_by_id('5898073bc3666e1e94c4f9c4')




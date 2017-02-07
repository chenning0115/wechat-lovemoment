#!/usr/bin/env python
# —*- coding:utf-8 -*-
#
# Copyright 2017 charnix
#
#



import sys
sys.path.append('..')
import os
import tornado.web
from tornado.web import RequestHandler
import constants
import mongomanager
import json
import logging
from datetime import datetime
import lovemement.mongomanager as mongomanager

logger = logging.getLogger(constants.LOGGING_NAME)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class Handler_getimage(RequestHandler):
    def get(self):
        image_id = self.get_argument(constants.url_param_image_id)
        image_path = os.path.join(constants.path_file_images,image_id)
        self.set_header("Content-type", "image/jpg,image/png,image/*")
        with open(image_path,'rb') as fin:
            data = fin.read()
            self.write(data)
            self.flush()

class Handler_getmoments(RequestHandler):
    def get(self):
        page_number = int(self.get_argument(constants.url_param_page_num))
        skip_num = constants.GET_MOMENTS_NUM_PER_PAGE * page_number
        res = mongomanager.find_moments_sort_by_timestamp(
            skip_num,constants.GET_MOMENTS_NUM_PER_PAGE)
        if res is None:
            error_msg = 'true'
            reslist = []
        else:
            error_msg = 'false'
            reslist = res
        logging.info('get moments: pagenumber=%d\tsize=%d' % (page_number,len(reslist)))

        response_dict = {
            "error": error_msg,
            'results':reslist
        }
        response_data = json.dumps(response_dict)
        self.write(response_data)
        self.flush()

class Handler_detail(RequestHandler):
    def get(self):
        _id = self.get_argument(constants.url_param_detail_id)
        logger.info(_id)
        res = mongomanager.find_by_id(_id)
        logger.info(res)
        error_msg = 'false' if res is None else 'true'
        response_dict = {
            "error": error_msg,
            'results': res
        }
        response_data = json.dumps(response_dict)
        self.write(response_data)
        self.flush()


class Handler_uploaddata(RequestHandler):
    def get(self):
        logger.info('someone upload by get!')
        pass
    def post(self):
        try:
            mdate_str = self.get_argument('mdate')+':00'
            content = self.get_argument('content')
            title = self.get_argument('title')
            description = self.get_argument('description')
            author = self.get_argument('author')
            picurls = []
            for field_name, files in self.request.files.items():
                for info in files:
                    filename, content_type = info['filename'], info['content_type']
                    body = info['body']
                    temp_items = content_type.strip().split('/')
                    if len(temp_items)==2:
                        typestr = temp_items[1]
                    else:
                        typestr = 'png'
                    logging.info('POST "%s" "%s" %d bytes',
                                 filename, content_type, len(body))
                    filename_timestamp = str(int(datetime.now().timestamp()))+'.'+typestr
                    with open(os.path.join(constants.path_file_images,filename_timestamp),'wb') as fout:
                        fout.write(body)
                        fout.flush()
                        picurls.append(filename_timestamp)
            mongomanager.insert_moment(author=author,title=title,mdate=mdate_str,description=description,
                                       content=content,pic_urls=picurls)
            # response_dict = {'error':'false'}
            self.write('true')
        except Exception as e:
            logger.info('wocao!!!')
            # response_dict = {'error': 'true'}
            self.write('false')
            print(e)


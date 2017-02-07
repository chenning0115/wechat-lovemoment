#!/usr/bin/env python
#-*-coding:utf-8-*-
#
# Copyright 2017 charnix
#
# —*- coding:utf-8 -*-


import os
path_base = os.path.abspath(os.path.dirname(__file__))
path_file_images = os.path.join(path_base,'images')


# server interal constants
PORT = 8080

GET_MOMENTS_NUM_PER_PAGE = 5


#mongodb url and port
mongo_url = 'localhost'
mongo_port = 27017
mongo_dbname = 'lovemoment'
mongo_table_moments = 'moments'



#url parameter constants

url_param_image_id='image_id'
url_param_page_num = 'page_num'
url_param_detail_id = '_id'

url_param_upload_file_sign='charnix_img_file'


#logging conf
path_file_logging_conf = os.path.join(path_base,'logging.conf')
LOGGING_NAME = 'cn'
#!/usr/bin/env python
# —*- coding:utf-8 -*-
#
# Copyright 2017 charnix
#
#

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import sys
sys.path.append('..')
import constants
import momenthandlers
import sys
import logging
import logging.config

# import lovemement.momenthandlers as momenthandlers




def main():
    logger = logging.getLogger(constants.LOGGING_NAME)

    application = tornado.web.Application([
        (r"/getimage", momenthandlers.Handler_getimage),
        (r"/getmoments",momenthandlers.Handler_getmoments),
        (r"/detail",momenthandlers.Handler_detail),
        (r"/uploadimg", momenthandlers.Handler_uploaddata),
        (r"/delete",momenthandlers.Handler_delete),
    ])
    https = sys.argv[1]
    if https == 'https':
        http_server = tornado.httpserver.HTTPServer(application,
                                                ssl_options={
                                                    "certfile": "./certfile/ca.csr",
                                                    "keyfile": "./certfile/ca.key"
                                                })
    else:
        http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(constants.PORT)
    logger.info('server start.. by %s' % https)
    tornado.ioloop.IOLoop.current().start()




if __name__=='__main__':
    logging.config.fileConfig(constants.path_file_logging_conf)
    main()

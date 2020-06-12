from flask import request
import os
import logging

LOGGING_LEVEL = logging.INFO
LOGGING_HANDLER = logging.StreamHandler()
LOGGING_FORMATTER = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

APPLICATION_HOST = os.environ.get("HOST",default="http://127.0.0.1:5000")

SWAGGER_TEMPLATE = {
  "swagger": "2.0",
  "info": {
    "title": "REST API",
    "description": "API description",
    "contact": {
      "author": "Wetcom",
      "url": "",
    },
    "version": "0.1.1"
  },
  "host": APPLICATION_HOST,
  "basePath": "/",  # base bash for blueprint registration
}

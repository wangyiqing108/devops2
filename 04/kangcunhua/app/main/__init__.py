#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: kang.cunhua@qq.com
# @Date:   2016-05-27 14:40:47
# @Last Modified by:   kang.cunhua@qq.com
# @Last Modified time: 2016-06-12 19:54:12
from flask import Blueprint

main = Blueprint('main', __name__)
from . import views, errors, resources

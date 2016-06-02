#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "SONG Xiang"


from __future__ import unicode_literals
from flask import render_template, request, jsonify
from . import main
import app.utils
import json

"""
    IDC列表页
"""
@main.route("/resources/idc/", methods=["GET"])
def resource_idc():
    ret = app.utils.api_action("idc.get")

    return render_template("resources/server_idc_list.html",
                           title = "IDC信息",
                           idcs=ret,
                           show_resource=True,
                           show_idc_list=True)
"""
    修改IDC信息
"""
@main.route("/resources/idc/modify/<int:idc_id>", methods=["GET"])
def resources_idc_modify(idc_id):
    ret = app.utils.api_action("idc.get",{"where":{"id":idc_id}})
    if ret:
        return render_template("resources/server_idc_modify.html",
                               title= "修改IDC信息",
                               idc=ret[0],
                               show_resource=True,
                               show_idc_list=True)
    return render_template("404.html"),404
"""
    更新IDC信息
"""
@main.route("/resources/idc/update",methods=["POST"])
def resources_idc_update():
    data = request.form.to_dict()
    id = data.pop("id")
    print data
    ret = app.utils.api_action("idc.update", {"data":data, "where":{"id":id}})
    if ret:
        return render_template("public/success.html", next_url="/resources/idc/")
    else:
        return render_template("public/error.html", next_url="/resources/idc/")

"""
    添加IDC信息页面
"""
@main.route("/resources/idc/add/", methods=["GET"])
def resources_add_idc():
    return render_template("resources/server_add_idc.html",
                           title="添加IDC",
                           show_resrouce=True,
                           show_idc_list=True)
"""
    添加信息操作
"""

@main.route("/resources/idc/doadd/", methods=["POST"])
def resources_doadd_idc():
    params = request.form.to_dict()
    ret = app.utils.api_action("idc.create", params)
    if ret:
        return render_template("public/success.html", next_url="/resources/idc/",title="操作成功")
    else:
        return render_template("public/error.html", next_url="/resources/idc/",title="操作成功")

"""
    删除信息操作
"""
@main.route("/resources/idc/delete", methods=["POST"])
def resources_delete_idc():
    id = request.form.get("id")
    ret = app.utils.api_action("idc.delete", {"id": id})
    print ret
    return jsonify(ret=ret)
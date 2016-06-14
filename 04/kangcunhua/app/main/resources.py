#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: kang.cunhua@qq.com
# @Date:   2016-05-27 14:40:47
# @Last Modified by:   kang.cunhua@qq.com
# @Last Modified time: 2016-06-14 20:48:03
from __future__ import unicode_literals
from flask import render_template, request
from . import main
import app.utils


"""
    IDC 列表页面
"""


@main.route("/resources/idc/", methods=["GET"])
def resources_idc():
    ret = app.utils.api_action("idc.get", {"where": {"status": 1}})
    return render_template("resources/server_idc_list.html",
                           title="IDC信息",
                           show_resource=True,
                           show_idc_list=True,
                           idcs=ret)

"""
    修改IDC信息
"""


@main.route("/resources/idc/modify/<int:idc_id>", methods=["GET"])
def resources_idc_modify(idc_id):
    ret = app.utils.api_action("idc.get", {"where": {"id": idc_id}})
    if ret:
        return render_template("resources/server_idc_modify.html",
                               title="修改IDC信息",
                               show_resource=True,
                               show_idc_list=True,
                               idc=ret[0])
    return render_template("404.html"), 404


@main.route("/resources/idc/update", methods=["POST"])
def resources_idc_update():
    data = request.form.to_dict()
    id = data.pop("id")
    ret = app.utils.api_action("idc.update", {"data": data, "where": {"id": id}})
    if ret:
        return render_template("public/success.html", next_url="/resources/idc/")
    else:
        return render_template("public/error.html", next_url="/resources/idc/")


@main.route("/resources/idc/add/", methods=["GET"])
def resources_add_idc():
    return render_template("resources/server_idc_add.html",
                           title="添加IDC",
                           show_resource=True,
                           show_idc_list=True)


@main.route("/resources/idc/doadd/", methods=["POST"])
def resources_doadd_idc():
    params = request.form.to_dict()
    ret = app.utils.api_action("idc.create", params)
    if ret:
        return render_template("public/success.html", next_url="/resources/idc/", title="操作成功")
    else:
        return render_template("public/error.html", next_url="/resources/idc/", title="操作失败")


@main.route("/resources/idc/delete/", methods=["POST"])
def resources_idc_delete():
    id = request.form.get("id", 0)
    ret = app.utils.api_action("idc.update", {"where": {"id": id}, "data": {"status": 0}})
    return str(ret)


"""
    服务器列表页面
"""


@main.route("/resources/server/list/", methods=["GET"])
def resources_server_list():
    return render_template("resources/server_list.html",
                           title="服务器信息",
                           show_resource=True,
                           show_serverlist=True)

"""
    添加服务器
"""


@main.route("/resources/server/add/", methods=["GET"])
def resources_server_add():
    manufacturers = app.utils.api_action("manufacturers.get")

    return render_template("resources/server_add.html",
                           title="添加服务器",
                           manufacturers=manufacturers,
                           show_resource=True,
                           show_serverlist=True)


"""
    添加制造商
"""


@main.route("/resources/server/manufacturers/add/", methods=["GET"])
def resources_manufacturers_add():
    return render_template("resources/server_add_manufacturers.html",
                           title="添加制造商")


"""
    执行添加制造商
"""


@main.route("/resources/server/manufacturers/doadd/", methods=["POST"])
def resources_manufacturers_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("manufacturers.create", params)
    if ret:
        return render_template("public/success.html", next_url="/resources/server/manufacturers/add/")
    else:
        return render_template("public/error.html", next_url="/resources/server/manufacturers/add/")
"""
    添加制造商操作
"""


@main.route("/resources/server/manufacturers/doadd/", methods=["POST"])
def resources_doadd_manufacturers():
    params = request.form.to_dict()
    ret = app.utils.api_action("manufacturers.create", params)
    jump_url = "/resources/server/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)

"""
    添加服务器类型
"""


@main.route("/resources/server/servertype/add/", methods=["GET"])
def resources_server_type_add():
    manufacturers = app.utils.api_action("manufacturers.get")
    return render_template("resources/server_add_servertype.html",
                           title="添加服务器类型",
                           manufacturers=manufacturers)

"""
    执行添加服务器类型操作
"""


@main.route("/resources/server/servertype/doadd/", methods=["POST"])
def resources_doadd_servertype():
    params = request.form.to_dict()
    ret = app.utils.api_action("servertype.create", params)
    jump_url = "/resources/server/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)

"""
    ajax操作
    获取服务器型号
"""


@main.route("/resources/ajax/get/server/type/", methods=["GET"])
def resources_ajax_get_server_type():
    params = request.args.to_dict()
    if params:
        servertype = app.utils.api_action("servertype.get", {"where": params})
        return json.dumps(servertype)
    return ''


"""
    添加业务线或产品线
"""


@main.route("/resources/server/product/add/", methods=["GET"])
def resources_server_product_add():
    products = app.utils.api_action("product.get", {"where": {"pid": 0}})
    return render_template("resources/server_add_product.html",
                           products=products)

"""
    执行添加业务或产品线
"""


@main.route("/resources/server/product/doadd/", methods=["POST"])
def resources_server_doadd_product():
    params = request.form.to_dict()
    ret = app.utils.api_action("product.create", params)
    jump_url = "/resources/server/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)

"""
    ajax操作
    根据一级业务线,获取他的二级业务线
"""


@main.route("/resources/ajax/get/server/product/", methods=["GET"])
def resources_ajax_get_server_product():
    params = request.args.to_dict()
    print params
    if params:
        ret = app.utils.api_action("product.get", {"where": params, "output": ["id", "service_name", "pid"]})
        return json.dumps(ret)
    return ''

"""
    添加服务器状态
"""


@main.route("/resources/status/add/", methods=["GET"])
def resources_status_add():
    return render_template("resources/server_add_status.html")

"""
    执行添加服务器状态
"""


@main.route("/resources/status/doadd/", methods=["POST"])
def resources_doadd_status():
    params = request.form.to_dict()
    ret = app.utils.api_action("status.create", params)
    jump_url = "/resources/server/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)
"""
    添加raid状态
"""


@main.route("/resources/server/raid/add/", methods=["GET"])
def resources_server_raid_add():
    return render_template("resources/server_add_raid.html")

"""
    执行添加raid状态
"""


@main.route("/resources/server_raid_doadd/", methods=["POST"])
def resources_doadd_server_raid():
    params = request.form.to_dict()
    ret = app.utils.api_action("raid.create", params)
    jump_url = "/resources/server/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)

"""
    添加机柜号
"""


@main.route("/resources/cabinet/add/", methods=["GET"])
def resources_server_raid_type_add():
    idcs = app.utils.api_action("idc.get", {"output": ["name", "id"]})
    powers = app.utils.api_action("power.get")
    return render_template("resources/server_add_cabinet.html",
                           idcs=idcs,
                           powers=powers)

"""
    执行添加机柜号
"""


@main.route("/resources/cabinet/doadd/", methods=["POST"])
def resources_doadd_cabinet_type():
    params = request.form.to_dict()
    ret = app.utils.api_action("cabinet.create", params)
    jump_url = "/resources/server/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)


"""
    添加功率
"""


@main.route("/resources/power/add/", methods=["GET"])
def resources_power_add():
    return render_template("resources/server_add_power.html")

"""
    执行添加功率
"""


@main.route("/resources/power/doadd/", methods=["POST"])
def resources_doadd_power():
    params = request.form.to_dict()
    ret = app.utils.api_action("power.create", params)
    jump_url = "/resources/power/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)


"""
    ajax操作
    获取机柜号
"""


@main.route("/resources/ajax/get/cabinet/", methods=["GET"])
def resources_ajax_get_cabinet():
    params = request.args.to_dict()
    print params
    if params:
        ret = app.utils.api_action("cabinet.get", {"where": params, "output": ["name", "id"]})
        return json.dumps(ret)
    return ''


"""
    添加raid类型
"""


@main.route("/resources/server/raidcardtype/add/", methods=["GET"])
def resources_server_raid_cardtype_add():
    return render_template("resources/server_add_raidcardtype.html",)

"""
    执行添加机柜号
"""


@main.route("/resources/server_raidcardtype_doadd/", methods=["POST"])
def resources_doadd_raidtype_type():
    params = request.form.to_dict()
    ret = app.utils.api_action("raidtype.create", params)
    jump_url = "/resources/server/raidcardtype/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)


"""
    添加远程管理卡
"""


@main.route("/resources/server/managementcardtype/add/", methods=["GET"])
def resources_server_managementcardtype_add():
    return render_template("resources/server_add_managementcardtype.html",)

"""
    执行添加远程管理卡
"""


@main.route("/resources/server/managementcardtype/doadd/", methods=["POST"])
def resources_doadd_raidtydpe_type():
    params = request.form.to_dict()
    ret = app.utils.api_action("managementcardtype.create", params)
    jump_url = "/resources/server/managementcardtype/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)


"""
    添加供应商
"""


@main.route("/resources/server/supplier/add/", methods=["GET"])
def resources_server_supplier_add():
    return render_template("resources/server_add_supplier.html",)

"""
    执行添加供应商
"""


@main.route("/resources/server/supplier/doadd/", methods=["POST"])
def resources_doadd_supplier():
    params = request.form.to_dict()
    ret = app.utils.api_action("supplier.create", params)
    jump_url = "/resources/server/supplier/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)

"""
    执行添加服务器
"""


@main.route("/resources/server/doadd/", methods=["POST"])
def resources_doadd_server():
    params = request.form.to_dict()
    ret = app.utils.api_action("server.create", params)
    jump_url = "/resources/server/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)


"""
    执行修改服务器
"""


@main.route("/resources/server/modify/doadd/", methods=["POST"])
def resources_doadd_modify_server():
    params = request.form.to_dict()
    server_id = request.form.get('id')
    resource = {"data": params, "where": {"id": server_id}}
    ret = app.utils.api_action("server.update", resource)
    jump_url = "/resources/server/add/"
    return app.utils.jump(ret, success_url=jump_url, error_url=jump_url)

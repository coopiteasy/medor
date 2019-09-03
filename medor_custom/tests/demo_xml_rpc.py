# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import xmlrpclib

HOST = '127.0.0.1'
PORT = 8069
# PORT = 9999
DB = 'medor'  # fixme
# DB = 'odoo-test-9'  # fixme
USER = 'medor_api_user'
PASSWORD = 'medor_api_user'


def demo_xml_rpc():

    url = 'http://%s:%d/xmlrpc/2/' % (HOST, PORT)

    common = xmlrpclib.ServerProxy(url + 'common')
    models = xmlrpclib.ServerProxy(url + 'object')

    uid = common.authenticate(DB, USER, PASSWORD, {})

    stats = models.execute_kw(
            DB, uid, PASSWORD,
            'res.company', 'read',
            [1], {'fields': ['nb_subscribers', 'nb_cooperators']}
    )
    print(stats)

    deposit_points = models.execute_kw(
            DB, uid, PASSWORD,
            'res.company', 'get_deposit_point',
            [], {}
    )
    print(deposit_points)

    subscription = models.execute_kw(
            DB, uid, PASSWORD,
            'res.users', 'get_subscription',
            [1], {}
    )
    print subscription

    subscription = models.execute_kw(
            DB, uid, PASSWORD,
            'res.users', 'get_subscription',
            [5910], {}
    )
    print subscription

    subscription = models.execute_kw(
            DB, uid, PASSWORD,
            'res.users', 'get_subscription',
            [2881], {}
    )
    print subscription

    partner_fields = models.execute_kw(
            DB, uid, PASSWORD,
            'res.users', 'read',
            [2881], {'fields': ['partner_id']}
    )
    print partner_fields  # {'partner_id': [7555, 'JACOBS Aline'], 'id': 2881}

    partner_id = partner_fields['partner_id'][0]
    partner_info = models.execute_kw(
            DB, uid, PASSWORD,
            'res.partner', 'read',
            [partner_id], {'fields': ['name', 'firstname', 'lastname']}
    )
    print partner_info


if __name__ == '__main__':
    demo_xml_rpc()

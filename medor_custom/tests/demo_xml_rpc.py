# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import xmlrpclib

HOST = '127.0.0.1'
PORT = 9999
DB = 'odoo-test-9'  # fixme
USER = 'admin'  # todo test client user
PASSWORD = 'admin'


def test_xml_rpc():

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


if __name__ == '__main__':
    test_xml_rpc()

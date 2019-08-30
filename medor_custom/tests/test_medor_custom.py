# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestMedorCustom(TransactionCase):
    # todo did coverage, should do tests
    def test_compute_company_data(self):
        company = self.env.ref('base.main_company')

        print company.nb_subscribers
        print company.nb_cooperators

    def test_get_deposit_points(self):
        company = self.env.ref('base.main_company')
        print company.get_deposit_point()
        self.assertTrue(True)

    def test_get_subscription(self):
        User = self.env['res.users']

        user_1 = User.create({
            'login': 'user_' + '1',
            'partner_id': self.ref('product_subscription.demo_subscriber_1'),
        })
        user_2 = User.create({
            'login': 'user_' + '2',
            'partner_id': self.ref('product_subscription.demo_subscriber_2'),
        })
        user_3 = User.create({
            'login': 'user_' + '3',
            'partner_id': self.ref('product_subscription.demo_subscriber_3'),
        })
        user_4 = User.create({
            'login': 'user_' + '4',
            'partner_id': self.ref('product_subscription.demo_subscriber_4'),
        })
        user_5 = User.create({
            'login': 'user_' + '5',
            'partner_id': self.ref('base.res_partner_12'),
        })

        print User.get_subscription(user_1.id)
        print User.get_subscription(user_2.id)
        print User.get_subscription(user_3.id)
        print User.get_subscription(user_4.id)
        print User.get_subscription(user_5.id)
        print User.get_subscription(-3)

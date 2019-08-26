# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestProductRelease(TransactionCase):

    def test_compute_company_data(self):
        company = self.env.ref('base.main_company')

        # self.assertEqual(company.nb_subscribers, 4)
        # self.assertEqual(company.nb_cooperators, 1)

    def test_get_deposit_points(self):
        company = self.env.ref('base.main_company')
        print(company.get_deposit_point())
        self.assertTrue(True)

    # todo test from xml rpc

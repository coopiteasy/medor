# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
import json


class ResCompany(models.Model):
    _inherit = 'res.company'

    nb_subscribers = fields.Integer(
        string='Nb Subscribers',
        compute='_compute_company_data')
    nb_cooperators = fields.Integer(
        string='Nb Cooperators',
        compute='_compute_company_data')

    @api.multi
    def _compute_company_data(self):
        for company in self:
            subscribers = (
                self.env['res.partner']
                    .sudo()
                    .search([('subscriber', '=', True)])
            )
            company.nb_subscribers = len(subscribers)

            cooperators = (
                self.env['res.partner']
                    .sudo()
                    .search([('member', '=', True)])
            )
            company.nb_cooperators = len(cooperators)

    @api.model
    def get_deposit_point(self):
        deposit_points = (
            self.env['res.partner']
                .search([('deposit_point', '=', True)])
        )

        data = [{
            'name': dp.name,
            'address': dp._display_address(dp)
        } for dp in deposit_points]

        return json.dumps({'deposit_points': data})

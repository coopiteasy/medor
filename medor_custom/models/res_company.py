# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
import json


class ResCompany(models.Model):
    _inherit = "res.company"

    nb_cooperators = fields.Integer(
        string="Nb Cooperators", compute="_compute_company_data"
    )
    nb_subscribers = fields.Integer(
        string="Nb Subscribers", compute="_compute_company_data"
    )
    nb_trial_subscribers = fields.Integer(
        string="Nb Trial Subscribers", compute="_compute_company_data"
    )

    @api.multi
    def _compute_company_data(self):
        for company in self:
            subscriptions = (
                self.env["product.subscription.object"]
                .sudo()
                .search(
                    [
                        ("state", "in", ["ongoing", "renew"]),
                    ]
                )
            )

            subscriber_ids = (
                subscriptions.filtered(lambda s: not s.is_trial)
                .mapped("subscriber")
                .ids
            )
            company.nb_subscribers = len(set(subscriber_ids))

            trial_subscriber_ids = (
                subscriptions.filtered(lambda s: s.is_trial).mapped("subscriber").ids
            )
            company.nb_trial_subscribers = len(set(trial_subscriber_ids))

            cooperators = self.env["res.partner"].sudo().search([("member", "=", True)])
            company.nb_cooperators = len(cooperators)

    @api.model
    def get_deposit_point(self):
        deposit_points = self.env["res.partner"].search([("deposit_point", "=", True)])

        data = [
            {"name": dp.name, "address": dp._display_address(dp)}
            for dp in deposit_points
            if dp.name
        ]

        return json.dumps({"deposit_points": data})

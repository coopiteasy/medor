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
    nb_web_subscribers = fields.Integer(
        string="Nb Web Subscribers", compute="_compute_company_data"
    )

    @api.multi
    def _compute_company_data(self):
        for company in self:
            query = """
            select 'nb_cooperators' as metric, count(id)
            from res_partner rp
            where rp.member and active
            union
            select 'nb_subscribers' as metric, count(distinct subscriber)
            from product_subscription_object pso
                     join product_subscription_template pst ON pst.id = pso.template
            where not pso.is_trial
              and pso.state in ('ongoing', 'renew')
            union
            select 'nb_trial_subscribers' as metric, count(distinct subscriber)
            from product_subscription_object pso
                     join product_subscription_template pst ON pst.id = pso.template
            where pso.is_trial
              and pso.state in ('ongoing', 'renew')
            union
            select 'nb_web_subscribers' as metric, count(distinct pso.subscriber)
            from product_subscription_object pso
                     join product_subscription_template pst ON pst.id = pso.template
                     join res_partner rp on rp.id = pso.subscriber
            where not pso.is_trial and pst.is_web_subscription
              and pso.state in ('ongoing', 'renew', 'terminated')
              and pso.end_date >= now()
              and rp.active;
            """
            self.env.cr.execute(query)
            res = self.env.cr.fetchall()
            metrics = {}
            for k, v in res:
                metrics[str(k)] = int(v)
            company.nb_cooperators = metrics["nb_cooperators"]
            company.nb_subscribers = metrics["nb_subscribers"]
            company.nb_trial_subscribers = metrics["nb_trial_subscribers"]
            company.nb_web_subscribers = metrics["nb_web_subscribers"]

    @api.model
    def get_deposit_point(self):
        deposit_points = self.env["res.partner"].search([("deposit_point", "=", True)])

        data = [
            {"name": dp.name, "address": dp._display_address(dp)}
            for dp in deposit_points
            if dp.name
        ]

        return json.dumps({"deposit_points": data})

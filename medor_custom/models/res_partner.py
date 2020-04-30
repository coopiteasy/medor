# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, vals):
        vals.update(
            {"out_inv_comm_type": "bba", "out_inv_comm_algorithm": "random"}
        )
        return super(ResPartner, self).create(vals)

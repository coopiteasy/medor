# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import json

from openerp import models, fields, api
from openerp.exceptions import AccessError, MissingError


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def get_subscription(self, user_id):
        user = self.env["res.users"].browse(user_id)
        if not user:
            return json.dumps({"error": "user not found"})

        try:
            partner = user.partner_id
        except MissingError:
            return json.dumps(
                {
                    "id": user_id,
                    "start": "",
                    "end": "",
                    "subscription": "",
                    "subscribed": False,
                }
            )

        subscriptions = partner.subscriptions.filtered(
            lambda s: s.state in ["renew", "ongoing"]
        )

        if subscriptions:
            first = subscriptions.sorted(lambda s: s.start_date)[0]
            last = subscriptions.sorted(lambda s: s.end_date, reverse=True)[0]

            return json.dumps(
                {
                    "id": user_id,
                    "start": first.start_date,
                    "end": last.end_date,
                    "subscription": first.template.name,
                    "subscribed": partner.is_web_subscribed,
                }
            )
        else:
            return json.dumps(
                {
                    "id": user_id,
                    "start": "",
                    "end": "",
                    "subscription": "",
                    "subscribed": False,
                }
            )

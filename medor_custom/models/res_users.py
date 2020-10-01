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
            lambda s: s.state in ["renew", "ongoing", "terminated"]
        )

        if subscriptions:
            today = fields.Date.today()

            current_subscriptions = subscriptions.filtered(
                lambda s: s.start_date <= today <= s.end_date
            )

            if current_subscriptions:
                current_subscription = current_subscriptions.sorted(
                    lambda s: s.end_date, reverse=True
                )[0]
                start_date = current_subscription.start_date
                end_date = current_subscription.end_date
                name = current_subscription.template.name
            else:
                last_subscription = subscriptions.sorted(
                    lambda s: s.end_date, reverse=True
                )[0]
                start_date = last_subscription.start_date
                end_date = last_subscription.end_date
                name = last_subscription.template.name

            return json.dumps(
                {
                    "id": user_id,
                    "start": start_date,
                    "end": end_date,
                    "subscription": name,
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
                    "subscribed": partner.is_web_subscribed,
                }
            )

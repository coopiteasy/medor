# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp import fields
import utils

_MC_TRIAL_TEMPLATE = 'medor_custom.template_trial_subscription'


class TrialSubscription(http.Controller):

    def create_user(self, user_values):
        sudo_users = request.env['res.users'].sudo()
        user_id = sudo_users._signup_create_user(user_values)
        sudo_users.with_context({'create_user': True}).action_reset_password()
        return user_id

    @http.route('/trial_subscription',
                type='http',
                auth='public',
                website=True)
    def get_trial_subscription_form(self):
        return request.website.render(_MC_TRIAL_TEMPLATE)

    @http.route('/trial_subscription/subscribe',
                type='http',
                auth='public',
                website=True)
    def subscribe_trial_subscription(self, **kwargs):
        utils.generic_form_checks(
            request=request,
            template='',
            **kwargs
        )

        values = {
            'firstname': kwargs.get('firstname').title(),
            'lastname': kwargs.get('lastname').upper(),
            'email': kwargs.get('email'),
        }
        subscriber = request.env['res.partner'].create(values)

        self.create_user({
            'login': subscriber.email,
            'partner_id': subscriber.id,
        })

        trial_template = request.env.ref('medor_custom.data_medor_trial_subscription_trial')
        request.env['product.subscription.object'].create({
            'subscriber': subscriber.id,
            'template': trial_template.id,
            'counter': 0,
            'subscribed_on': fields.Date.today(),
            'state': 'ongoing',
        })

        return request.website.render(
            "medor_custom.template_trial_subscription_thanks",
            {
                '_values': values,
                '_kwargs': kwargs,
            }
        )


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

    @http.route(['/trial_subscription',
                 '/new/subscription/trial'],
                type='http',
                auth='public',
                website=True)
    def get_trial_subscription_form(self, **kwargs):
        if 'redirect' in kwargs:
            request.session['redirect_'] = kwargs.get('redirect')
        return request.website.render(_MC_TRIAL_TEMPLATE)

    @http.route('/trial_subscription/subscribe',
                type='http',
                auth='public',
                website=True)
    def subscribe_trial_subscription(self, **kwargs):
        user_obj = request.env['res.users']
        partner_obj = request.env['res.partner']
        utils.generic_form_checks(
            request=request,
            template='',
            **kwargs
        )

        sub_email = kwargs.get('email')
        values = {
            'firstname': kwargs.get('firstname').title(),
            'lastname': kwargs.get('lastname').upper(),
            'email': sub_email,
        }

        subscriber = partner_obj.sudo().search([('email', '=', sub_email)])
        if subscriber:
            subscriber = partner_obj.sudo().create(values)

        if not user_obj.user_exist(subscriber.email):
            user_obj.create_user({
                'login': subscriber.email,
                'partner_id': subscriber.id,
            })

        trial_template = request.env.ref('medor_custom.data_medor_trial_subscription_trial')
        request.env['product.subscription.object'].sudo().create({
            'subscriber': subscriber.id,
            'template': trial_template.id,
            'counter': 0,
            'subscribed_on': fields.Date.today(),
            'start_date': fields.Date.today(),
            'state': 'ongoing',
        })

        if 'redirect_' in request.session:
            return request.redirect(request.session['redirect_'])
        return request.website.render(
            "medor_custom.template_trial_subscription_thanks",
            {
                '_values': values,
                '_kwargs': kwargs,
            }
        )

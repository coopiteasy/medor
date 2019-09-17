# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs <http://coopiteasy.be>
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.http import request

from openerp.addons.website_product_subscription.controllers.subscribe import SubscribeController
from openerp.addons.medor_custom.controllers.delivery_form import DeliveryForm


class MedorSubscribeController(SubscribeController):

    def subscribe_form_validation(self):
        """Execute form check and validation"""
        super(MedorSubscribeController, self).subscribe_form_validation()
        user = None
        if request.session.uid:
            user = request.env['res.users'].browse(request.session.uid)
        form = DeliveryForm(request.params, user)
        form.delivery_subscription_selection = False
        form.normalize_form_data()
        form.validate_form()
        form.init_form_data()
        if request.httprequest.method == 'GET':
            form.set_form_defaults()

    def process_subscribe_form(self):
        sub_req = super(
            MedorSubscribeController, self
        ).process_subscribe_form()
        params = request.params
        form = DeliveryForm(None)  # Empty form to access @property
        partner_obj = request.env['res.partner']
        if params['delivery_method'] == 'friend':
            values = {
                key[7:]: params[key]
                for key in params
                if key in form.friend_address_fields
            }
            friend = partner_obj.sudo().create(values)
            params['friend_id'] = friend.id
            sub_req.subscriber = friend.id
        elif params['delivery_method'] == 'other':
            # TODO: Deliver subscription to a another person.
            pass
        return sub_req

# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import http
from openerp.http import request
from openerp.tools.translate import _

from openerp.exceptions import ValidationError

from openerp.addons.medor_custom.controllers.delivery_form import DeliveryForm


class MedorDelivery(http.Controller):

    @http.route(
        '/edit/delivery_method',
        type='http',
        auth='user',
        website=True
    )
    def delivery_form(self, **kw):
        user = request.env.user
        form = DeliveryForm(request.params, user=request.env.user)
        form.normalize_form_data()
        form.validate_form()
        form.init_form_data()
        form.set_form_defaults()
        if ('error' not in request.params
                and request.httprequest.method == 'POST'):
            if request.params['delivery_method'] == 'me':
                # Get company if the current user is a representative.
                partner = user
                if user.parent_id and user.type == 'representative':
                    partner = user.parent_id
                for address in partner.child_ids:
                    if address.type == 'delivery':
                        # TODO: unlink or archive ?
                        # address.unlink()
                        address.active = False
            elif request.params['delivery_method'] == 'friend':
                # Get company if the current user is a representative.
                partner = user
                if user.parent_id and user.type == 'representative':
                    partner = user.parent_id
                values = {
                    key[7:]: request.params[key]
                    for key in request.params
                    if key in form.friend_address_fields
                }
                self.modify_delivery_address(partner, values)
            else:
                # TODO
                pass
            return request.redirect(request.params.get('redirect', ''))
        return request.website.render(
            'medor_custom.delivery_form', request.params
        )

    def modify_delivery_address(self, user, values):
        """Write values to the delivery address of the given user."""
        partner = user
        if user.child_ids:
            for address in user.child_ids:
                if address.type == 'delivery':
                    partner = address
        return partner.write(values)

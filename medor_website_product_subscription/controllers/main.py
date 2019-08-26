# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp.tools.translate import _

from openerp.exceptions import ValidationError

from openerp.addons.medor_website_product_subscription.controllers.medor_form import UserForm


class MedorWebsiteProductSubscription(http.Controller):

    @http.route(
        '/edit/user/',
        type='http',
        auth='user',
        website=True
    )
    def user_form(self, **kw):
        user = request.env.user
        form = UserForm(request.params, user=request.env.user)
        form.normalize_form_data()
        form.validate_form()
        form.init_form_data()
        form.set_form_defaults()
        if ('error' not in request.params
                and request.httprequest.method == 'POST'):
            # representative
            values = {
                key: request.params[key]
                for key in request.params
                if key in form.user_fields
            }
            user.write(values)
            if user.parent_id:
                # company
                representative = user.parent_id
                representative.write({
                    'name': request.params['company_name'],
                })
                try:
                    representative.vat = request.params['vat']
                except ValidationError as err:
                    request.params['error'] = err.name
                if request.params.get('invoice_address', False):
                    values = {
                        key[4:]: request.params[key]
                        for key in request.params
                        if key in form.user_inv_fields
                    }
                    self.modify_invoice_address(user, values)
            if 'error' not in request.params:
                return request.redirect(request.params.get('redirect', ''))
        return request.website.render(
            'medor_website_product_subscription.user_form', request.params
        )

    def modify_invoice_address(self, user, values):
        """Write values to the invoice address of the given user."""
        partner = user
        if user.child_ids:
            for address in user.child_ids:
                if address.type == 'invoice':
                    partner = address
        return partner.write(values)

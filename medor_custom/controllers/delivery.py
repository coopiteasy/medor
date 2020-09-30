# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import http
from openerp.http import request
from openerp.addons.medor_custom.controllers.delivery_form import DeliveryForm


class MedorDelivery(http.Controller):
    @http.route(
        "/edit/delivery_method", type="http", auth="user", website=True
    )
    def delivery_form(self, **kw):
        user = request.env.user
        sub_obj = request.env["product.subscription.object"]
        partner_obj = request.env["res.partner"]
        form = self.delivery_form_validation()
        if (
            "error" not in request.params
            and request.httprequest.method == "POST"
        ):
            sub = sub_obj.sudo().browse(
                request.params["delivery_subscription"]
            )
            if request.params["delivery_method"] == "me":
                sub.subscriber = user.partner_id
            elif request.params["delivery_method"] == "friend":
                values = {
                    key[7:]: request.params[key]
                    for key in request.params
                    if key in form.friend_address_fields
                }
                if sub.subscriber != sub.request.websubscriber:
                    sub.subscriber.write(values)
                else:
                    friend = partner_obj.sudo().create(values)
                    sub.subscriber = friend
            else:
                # TODO: Need reference to unknow user.
                pass
            return request.redirect(request.params.get("redirect", ""))
        return request.website.render(
            "medor_custom.delivery_form", request.params
        )

    def delivery_form_validation(self):
        """Execute form check and validation"""
        user = None
        if request.session.uid:
            user = request.env["res.users"].browse(request.session.uid)
        form = DeliveryForm(request.params, user=user)
        form.normalize_form_data()
        form.validate_form()
        if request.httprequest.method == "GET":
            form.init_form_data()
            form.set_form_defaults()
        return form

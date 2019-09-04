# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import http
from openerp.http import request
from openerp.tools.translate import _

from openerp.addons.medor_custom.controllers.delivery_form import DeliveryForm
from openerp.addons.website_product_subscription.controllers.main import WebsiteProductSubscription


class WebsiteProductSubscription(WebsiteProductSubscription):

    def fill_values(self, values, load_from_user=False):
        values = super(
            WebsiteProductSubscription, self
        ).fill_values(values, load_from_user=False)
        form = DeliveryForm(values)
        form.normalize_form_data()
        form.validate_form()
        form.init_form_data()
        form.set_form_defaults()
        return values

    def product_subscription(self, **kwargs):
        response = super(
            WebsiteProductSubscription, self
        ).product_subscription(**kwargs)
        # TODO: write data from the delivery method part of the form to
        # the right partner. Maybe the
        return response

# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs <http://coopiteasy.be>
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import tools
from openerp.exceptions import ValidationError
from openerp.http import request
from openerp.tools.translate import _


class DeliveryForm():

    def __init__(self, qcontext, user=None):
        # Copy reference. Qcontext will be modified in place.
        self.qcontext = qcontext
        self.user = user

    def normalize_form_data(self):
        """
        Normalize data encoded by the user.
        """
        # The keyword zip is overwrite in the template by the zip
        # standard class of python. So we converted it into 'zip_code'
        # As this happens only in template, we can continue to use 'zip'
        # in the controller.
        if 'friend_zip_code' in self.qcontext:
            self.qcontext['friend_zip'] = self.qcontext['friend_zip_code']
        # Strip all str values
        for key, val in self.qcontext.items():
            if isinstance(val, str):
                self.qcontext[key] = val.strip()
        # Convert to int when needed
        if 'friend_country_id' in self.qcontext:
            self.qcontext['friend_country_id'] = int(
                self.qcontext['friend_country_id']
            )

    def validate_form(self):
        """
        Populate qcontext with errors if the values given by the user
        are not correct.
        """
        # TODO: Ensure that required fields are filled in.
        pass

    def init_form_data(self):
        """
        Populate qcontext with generic data needed to render the form.
        See also set_form_defaults to set default value to each fields
        of the form.
        """
        subs = []
        if self.user:
            reqs = (
                request.env['product.subscription.request']
                .sudo()
                .search([('webaccess', '=', self.user.partner_id.id)])
            )
            subs = (
                request.env['product.subscription.object']
                .sudo()
                .search([('request', '=', reqs.ids)])
            )
        self.qcontext.update({
            'countries': request.env['res.country'].sudo().search([]),
            'delivery_subscriptions': subs,
        })

    def set_form_defaults(self, force=False):
        """
        Populate qcontext with the default value for the form. If user
        is set the default values are values of the user.
        """
        sub = None
        if self.qcontext['delivery_subscriptions']:
            sub = self.qcontext['delivery_subscriptions'][0]
            self.qcontext['delivery_subscription'] = sub.id
        if self.user and sub:
            if 'delivery_method' not in self.qcontext or force:
                # TODO: if sub.subscriber == suspended gay.
                if sub.subscriber != sub.request.webaccess:
                    friend_address = sub.subscriber
                    self.qcontext['delivery_method'] = 'friend'
                    if 'friend_country_id' not in self.qcontext or force:
                        self.qcontext['friend_country_id'] = (
                            friend_address.country_id.id
                        )
                    for key in self.friend_address_fields:
                        if key not in self.qcontext or force:
                            self.qcontext[key] = getattr(
                                friend_address, key[7:]
                            )
                    self.qcontext['friend_zip_code'] = (
                        self.qcontext['friend_zip']
                    )
                else:
                    self.qcontext['delivery_method'] = 'me'
        else:
            if 'delivery_method' not in self.qcontext or force:
                self.qcontext['delivery_method'] = 'me'
            if 'friend_country_id' not in self.qcontext or force:
                self.qcontext['friend_country_id'] = (
                    request
                    .env['res.company']
                    ._company_default_get()
                    .country_id.id
                )

    @property
    def friend_address_fields(self):
        """
        Return names of the fields of a res_user object that are in the
        form.
        """
        return [
            'friend_name',
            'friend_street',
            'friend_zip',
            'friend_city',
            'friend_country_id',
        ]

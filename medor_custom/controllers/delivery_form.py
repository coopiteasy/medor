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
        self.qcontext.update({
            'countries': request.env['res.country'].sudo().search([]),
        })

    def set_form_defaults(self, force=False):
        """
        Populate qcontext with the default value for the form. If user
        is set the default values are values of the user.
        """
        if self.user:
            if self.user.parent_id and self.user.type == 'representative':
                user = self.user.parent_id
            else:
                user = self.user
            friend_address = None
            for partner in user.child_ids:
                if partner.type == 'delivery':
                    friend_address = partner
            if 'delivery_method' not in self.qcontext or force:
                if friend_address:
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

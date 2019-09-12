# -*- coding: utf-8 -*-
# Copyright 2019-     Coop IT Easy SCRLfs <http://coopiteasy.be>
#     - Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import tools
from openerp.exceptions import ValidationError
from openerp.http import request
from openerp.tools.translate import _


class UserForm():

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
        if 'zip_code' in self.qcontext:
            self.qcontext['zip'] = self.qcontext['zip_code']
        if 'inv_zip_code' in self.qcontext:
            self.qcontext['inv_zip'] = self.qcontext['inv_zip_code']
        # Strip all str values
        for key, val in self.qcontext.items():
            if isinstance(val, str):
                self.qcontext[key] = val.strip()
        # Convert to int when needed
        if 'country_id' in self.qcontext:
            self.qcontext['country_id'] = int(self.qcontext['country_id'])
        if 'inv_country_id' in self.qcontext:
            self.qcontext['inv_country_id'] = int(
                self.qcontext['inv_country_id']
            )
        # Checkbox to boolean
        if 'invoice_address' in self.qcontext:
            self.qcontext['invoice_address'] = (
                self.qcontext['invoice_address'] == 'on'
            )

    def validate_form(self):
        """
        Populate qcontext with errors if the values given by the user
        are not correct.
        """
        if self.qcontext.get('login', False):
            if not tools.single_email_re.match(
                self.qcontext.get('login', '')
            ):
                self.qcontext['error'] = _(
                    "That does not seem to be an email address."
                )

    def init_form_data(self):
        """
        Populate qcontext with generic data needed to render the form.
        See also set_form_defaults to set default value to each fields
        of the form.
        """
        self.qcontext.update({
            'countries': request.env['res.country'].sudo().search([]),
            'langs': request.env['res.lang'].sudo().search([]),
            'is_company': bool(self.user.parent_id)
        })

    def set_form_defaults(self, force=False):
        """
        Populate qcontext with the default value for the form. If user
        is set the default values are values of the user.
        """
        if self.user:
            if self.user.parent_id:
                if 'company_name' not in self.qcontext or force:
                    self.qcontext['company_name'] = self.user.parent_id.name
                if 'invoice_address' not in self.qcontext or force:
                    inv_add = False
                    for partner in self.user.child_ids:
                        if partner.type == 'invoice':
                            inv_add = partner
                    self.qcontext['invoice_address'] = bool(inv_add)
                    if 'inv_country_id' not in self.qcontext or force:
                        self.qcontext['inv_country_id'] = (
                            inv_add.country_id.id
                        )
                    for key in self.user_inv_fields:
                        if key not in self.qcontext or force:
                            self.qcontext[key] = getattr(inv_add, key[4:])
                    self.qcontext['inv_zip_code'] = self.qcontext['inv_zip']
            if 'country_id' not in self.qcontext or force:
                self.qcontext['country_id'] = self.user.country_id.id
            for key in self.user_fields:
                if key not in self.qcontext or force:
                    self.qcontext[key] = getattr(self.user, key)
            self.qcontext['zip_code'] = self.qcontext['zip']

    @staticmethod
    def generate_name_field(firstname, lastname):
        """
        Generate a name based on firstname and lastname.
        """
        return ("%s %s" % (firstname, lastname)).strip()

    @property
    def user_fields(self):
        """
        Return names of the fields of a res_user object that are in the
        form.
        """
        return [
            'firstname',
            'lastname',
            'login',
            'birthdate_date',
            'street',
            'city',
            'zip',
            'country_id',
        ]

    @property
    def user_inv_fields(self):
        """
        Return names of the fields of a res_user object that are in the
        form.
        """
        return [
            'inv_street',
            'inv_zip',
            'inv_city',
            'inv_country_id',
        ]

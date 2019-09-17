# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tools.translate import _


def check_recaptcha(request, **kwargs):
    if 'g-recaptcha-response' not in kwargs or not request.website.is_captcha_valid(kwargs['g-recaptcha-response']):
        return _('the captcha has not been validated, '
                 'please fill in the captcha')
    else:
        return None


def check_email_confirmation_matches(**kwargs):
    is_logged = kwargs.get('logged') == 'on'
    if not is_logged and kwargs.get('email') != kwargs.get('email_confirmation'):
        return _("email and confirmation email don't match")
    else:
        return None


def check_email_not_in_database(request, **kwargs):
    is_logged = kwargs.get('logged') == 'on'
    if not is_logged:
        user = request.env['res.users'].sudo().search([('login', '=', kwargs.get('email'))])
        if user:
            return _('There is an existing account for '
                     'this mail address. Please log in '
                     'before fill in the form')
    return None


def generic_form_checks(request, template, **kwargs):
    wrong_recaptcha_error = check_recaptcha(request, **kwargs)
    if wrong_recaptcha_error:
        kwargs['error_msg'] = wrong_recaptcha_error
        return request.website.render(template, kwargs)

    email_missmatch_error = check_email_confirmation_matches(**kwargs)
    if email_missmatch_error:
        kwargs['error_msg'] = email_missmatch_error
        return request.website.render(template, kwargs)

    # email_in_db_error = check_email_not_in_database(request, **kwargs)
    # if email_in_db_error:
    #     kwargs['error_msg'] = email_in_db_error
    #     return request.website.render(template, kwargs)

# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ProductSubscriptionObject(models.Model):
    _inherit = 'product.subscription.object'

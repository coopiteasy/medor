# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ProductSubscriptionObject(models.Model):
    _inherit = 'product.subscription.object'

    @api.model
    def cron_fix_historical_subscription_start_date(self):
        subscriptions = self.search([])

        for i, subscription in enumerate(subscriptions):
            if subscription.request:
                new_start_date = subscription.request.subscription_date
                _logger.info(
                    "{}/{} {} - setting start_date from {} to {}".format(
                        i + 1, len(subscriptions),
                        subscription.name,
                        subscription.start_date,
                        new_start_date
                ))
                subscription.start_date = new_start_date
            else:
                _logger.info('{}/{} {} - skipping'.format(
                    i + 1, len(subscriptions),
                    subscription.name
                ))

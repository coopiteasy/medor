# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#     Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Medor Website Product Subscription',

    'summary': """
        Add Medor specific change to Website Product Subscription.
    """,
    'description': """
    """,

    'author': 'Coop IT Easy SCRLfs',
    'website': "https://coopiteasy.be",

    'license': "AGPL-3",
    'category': "Website",
    'version': '9.0.1.0',

    'depends': [
        'oauth_provider',
        'easy_my_coop',
        'delivery_distribution_list',
        'product_subscription',
        'product_subscription_delivery',
        'product_subscription_web_access',
        'website_product_subscription',
        'medor_website_product_subscription',
        'l10n_be_invoice_bba',
    ],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/medor_api_user.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
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
        'website_product_subscription',
    ],

    'data': [
        'views/website_product_subscription_templates.xml',
        'views/medor_website_ps_templates.xml',
    ]
}

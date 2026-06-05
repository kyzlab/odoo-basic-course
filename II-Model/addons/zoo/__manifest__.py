# -*- coding: utf-8 -*-
# https://www.odoo.com/documentation/19.0/developer/reference/backend/module.html
{
    'name': 'Zoo',
    'summary': """Zoo Management""",
    'description': """Manage zoo city with Odoo 19""",
    'author': 'minhng.info',
    'maintainer': 'minhng.info',
    'website': 'https://minhng.info',
    'category': 'Uncategorized', # https://github.com/odoo/odoo/blob/19.0/odoo/addons/base/data/ir_module_category_data.xml
    'version': '19.0.0.1',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/zoo_animal_views.xml',
        'views/zoo_creature_views.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
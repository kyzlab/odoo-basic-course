# -*- coding: utf-8 -*-
# https://www.odoo.com/documentation/19.0/developer/reference/backend/module.html
{
    'name': 'Foo',
    'summary': """Foo custom addon""",
    'description': """Foo module description""",
    'author': 'minhng.info',
    'maintainer': 'minhng.info',
    'website': 'https://minhng.info',
    'category': 'Uncategorized', # https://github.com/odoo/odoo/blob/19.0/odoo/addons/base/data/ir_module_category_data.xml
    'version': '19.0.0.1',
    'depends': [
        'sale',
        'hr',
    ],
    'data': [],
    'demo': [],
    'css': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

# -*- coding: utf-8 -*-
# https://www.odoo.com/documentation/19.0/developer/reference/backend/module.html
{
    'name': 'Petshop',
    'summary': """Petshop Management""",
    'description': """Manage your pet shop with Odoo 19""",
    'author': 'minhng.info',
    'maintainer': 'minhng.info',
    'website': 'https://minhng.info',
    'category': 'Uncategorized', # https://github.com/odoo/odoo/blob/19.0/odoo/addons/base/data/ir_module_category_data.xml
    'version': '19.0.0.1',
    'depends': [
	    'base',    # ← add
	    'product', # ← add
    ],
    'data': [
        'security/ir.model.access.csv',
        #'data/petshop_data.xml',          # ← sample data records
        'views/petshop_pet_views.xml',       # ← declare view
        'views/petshop_species_views.xml',   # ← declare view
        'views/petshop_cage_views.xml',
        'views/petshop_pet_meal_views.xml',
        'views/petshop_vaccine_views.xml',
        'wizard/toy_add_wizard_views.xml',    # ← add this line
        'wizard/toy_unlink_wizard_views.xml',
        'wizard/cage_assign_wizard_views.xml',
        'wizard/meal_batch_wizard_views.xml',
        'views/petshop_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'petshop/static/src/components/counter/*',
            'petshop/static/src/components/mytable/*',   # add this line
            'petshop/static/src/components/petstatebadge/*',   # add this line
            'petshop/static/src/components/dashboard/*',   # add this line
        ],
    },
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
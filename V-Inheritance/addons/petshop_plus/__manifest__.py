{
    'name': 'Petshop Plus',
    'summary': 'Extension module for Petshop',
    'author': 'course.minhng.info',
    'version': '19.0.0.1',
    'depends': ['petshop'],   # required: depends on petshop
    'data': [
        'security/ir.model.access.csv',
        'views/petshop_pet_views.xml',   # <- add view file
        'views/petshop_species_views.xml',
        'views/petshop_cage_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

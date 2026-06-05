# -*- coding: utf-8 -*-
from odoo import fields, models

class ZooCreature(models.Model):
    _name = "zoo.creature"
    _description = "Zoo Creature"

    name = fields.Char('Name', required=True)
    environment = fields.Selection([
        ('water',  'Underwater'),
        ('ground', 'On Land'),
        ('sky',    'In the Sky'),
    ], string='Habitat', default='ground')
    
    # One2many — reverse of creature_id in zoo.animal
    animal_ids = fields.One2many(
        comodel_name='zoo.animal',
        inverse_name='creature_id',
        string='Animals'
    )

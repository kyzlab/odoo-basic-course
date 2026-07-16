# -*- coding: utf-8 -*-
from odoo import fields, models

class PetshopSpecies(models.Model):
    _name = "petshop.species"
    _description = "Pet Species"

    name = fields.Char('Species Name', required=True)
    environment = fields.Selection([
        ('water',  'Underwater'),
        ('ground', 'On Land'),
        ('sky',    'In the Sky'),
    ], string='Habitat', default='ground')
    is_rare = fields.Boolean('Rare Species', default=False)
    # One2many — reverse of species_id in petshop.pet
    pet_ids = fields.One2many(
        comodel_name='petshop.pet',
        inverse_name='species_id',
        string='Pets'
    )
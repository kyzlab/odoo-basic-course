# -*- coding: utf-8 -*-
from odoo import fields, models

class PetshopCage(models.Model):
    _name = "petshop.cage"
    _description = "Cage"

    name = fields.Char('Cage Name', required=True)
    code = fields.Char('Cage Code')
    length = fields.Float('Length (m)')
    width = fields.Float('Width (m)')
    height = fields.Float('Height (m)')
    description = fields.Text('Description')

    # One2many — reverse of cage_id in petshop.pet
    pet_ids = fields.One2many(
        comodel_name='petshop.pet',
        inverse_name='cage_id',
        string='Pets'
    )

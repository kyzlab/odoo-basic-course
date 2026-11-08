# -*- coding: utf-8 -*-
from odoo import fields, models

class PetshopVaccine(models.Model):
    _name = "petshop.vaccine"
    _description = "Pet Vaccine"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    pet_ids = fields.Many2many(comodel_name='petshop.pet',
        string='Pets',
        relation='pet_vaccine_rel',
        column1='col_vaccine_pet_id',
        column2='col_pet_vaccine_id'
    )

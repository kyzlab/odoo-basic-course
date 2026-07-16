# -*- coding: utf-8 -*-
from odoo import fields, models

class PetshopPetMeal(models.Model):
    _name = "petshop.pet.meal"
    _description = "Pet Meal"

    pet_id = fields.Many2one(
        comodel_name='petshop.pet',
        string='Pet',
        required=True,
        ondelete='cascade'  # delete meal when pet is deleted
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Food',
        required=True
    )
    volume = fields.Float('Volume (g)', required=True)
    meal_time = fields.Selection([
        ('morning',   'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening',   'Evening'),
        ('midnight',  'Midnight'),
    ], string='Meal Time', default='morning')
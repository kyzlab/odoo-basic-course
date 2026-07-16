# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ToyAddWizard(models.TransientModel):
    _name = "petshop.toy.add.wizard"
    _description = "Add Toy to Pet"

    product_id = fields.Many2one('product.product', string='Toy', required=True)

    def action_add_toy(self):
        active_ids = self.env.context.get('active_ids', [])   # get active record (petshop.pet) ids
        pets = self.env['petshop.pet'].browse(active_ids)
        # Append toy to pets
        # Read "Tut 6 - Commands on relational fields" for more details
        pets.write({'toy_ids': [(4, self.product_id.id, 0)]})

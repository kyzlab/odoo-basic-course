# -*- coding: utf-8 -*-
from odoo import api, fields, models

class MealBatchWizard(models.TransientModel):
    _name = "petshop.meal.batch.wizard"
    _description = "Batch Create Meals for Pets"

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Food',
        required=True
    )
    volume = fields.Float('Volume (g)', required=True)
    meal_time = fields.Selection([
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('midnight', 'Midnight'),
    ], string='Meal Time', default='morning', required=True)
    pet_ids = fields.Many2many(
        comodel_name='petshop.pet',
        string='Pets',
        required=True
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids', [])
        active_model = self.env.context.get('active_model')
        if active_model == 'petshop.pet' and active_ids:
            defaults['pet_ids'] = [(6, 0, active_ids)]
        return defaults

    def action_create_meals(self):
        self.pet_ids.write({
            'meal_ids': [
                (0, 0, {
                    'product_id': self.product_id.id,
                    'volume': self.volume,
                    'meal_time': self.meal_time,
                })
            ]
        })
        # OR fields.Command
        # self.pet_ids.write({
        #     'meal_ids': [fields.Command.create({
        #         'product_id': self.product_id.id,
        #         'volume': self.volume,
        #         'meal_time': self.meal_time,
        #     })]
        # })

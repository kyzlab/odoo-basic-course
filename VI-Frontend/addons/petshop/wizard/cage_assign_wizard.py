# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ToyAssignWizard(models.TransientModel):
    _name = "petshop.cage.assign.wizard"
    _description = "Assign Cage to Pets"

    cage_id = fields.Many2one('petshop.cage', string='Cage', required=True)

    def action_cage_assign(self):
        active_ids = self.env.context.get('active_ids', [])   # get active record (petshop.pet) ids
        pets = self.env['petshop.pet'].browse(active_ids)
        pets.write({'cage_id': self.cage_id.id})

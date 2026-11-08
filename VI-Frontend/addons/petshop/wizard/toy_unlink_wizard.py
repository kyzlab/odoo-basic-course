# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ToyUnlinkWizard(models.TransientModel):
    _name = "petshop.toy.unlink.wizard"
    _description = "Unlink Toys of Pet"

    def action_toy_unlink(self):
        active_ids = self.env.context.get('active_ids', [])   # get active record (petshop.pet) ids
        pets = self.env['petshop.pet'].browse(active_ids)
        pets.write({'toy_ids': [(5, 0, 0)]})

from odoo import api, fields, models

class PetshopSpeciesPlus(models.Model):
    """In-place extension of petshop.species.
    Adds a rich-text description and a computed counter for the total number
    of pets belonging to each species.
    """
    _inherit = 'petshop.species'

    description = fields.Html('Description')
    total_pets = fields.Integer('Total Pets', compute='_compute_total_pets', store=True, help='Total number of pets currently linked to this species.')

    @api.depends('pet_ids')
    def _compute_total_pets(self):
        """Count pets linked to this species record."""
        for species in self:
            species.total_pets = len(species.pet_ids)

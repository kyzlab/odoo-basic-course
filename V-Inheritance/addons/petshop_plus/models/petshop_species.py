from odoo import api, fields, models

class PetshopSpeciesPlus(models.Model):
    """In-place extension of petshop.species.
    Adds a rich-text description, a short note, an avatar image, and a computed
    counter for the total number of pets belonging to each species.
    """
    _inherit = 'petshop.species'

    image = fields.Binary('Image', attachment=True, help='Avatar or representative image for this species.')
    short_note = fields.Char('Short Note', help='A brief summary or tagline for this species.')
    description = fields.Html('Description')
    total_pets = fields.Integer('Total Pets', compute='_compute_total_pets', store=True, help='Total number of pets currently linked to this species.')

    @api.depends('pet_ids')
    def _compute_total_pets(self):
        """Count pets linked to this species record."""
        for species in self:
            species.total_pets = len(species.pet_ids)

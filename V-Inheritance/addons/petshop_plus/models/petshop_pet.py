from odoo import api, fields, models

class PetshopPetPlus(models.Model):
    _inherit = 'petshop.pet'   # same name = extend in-place, same DB table

    is_vaccinated = fields.Boolean('Vaccinated', default=False)
    vaccine_note  = fields.Char('Vaccine Note', default='')

    @api.onchange('is_vaccinated')
    def _onchange_is_vaccinated(self):
        if self.is_vaccinated:
            self.vaccine_note = 'All vaccine doses completed.'
        else:
            self.vaccine_note = 'Not vaccinated — please schedule an appointment.'
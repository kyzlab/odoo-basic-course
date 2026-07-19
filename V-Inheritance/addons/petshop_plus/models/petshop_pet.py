from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

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

    def action_open_cage_detail(self):
        self.ensure_one()
        if not self.cage_id:
            raise ValidationError(_('Cage not found!'))
        return {
            'res_model': self.env["petshop.cage"]._name,
            'type': 'ir.actions.act_window',
            'views': [[False, 'form']],
            'res_id': self.cage_id.id,
        }

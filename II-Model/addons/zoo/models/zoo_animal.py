# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class ZooAnimal(models.Model):
    _name = "zoo.animal"
    _description = "Zoo Animal"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    dob = fields.Date('Date of Birth', required=False)
    gender = fields.Selection([
        ('male',   'Male'),
        ('female', 'Female'),
    ], string='Gender', default='male', required=True)
    image = fields.Binary('Image', attachment=True, help='Animal photo')

    # Many2one — an animal belongs to one creature
    creature_id = fields.Many2one(
        comodel_name='zoo.creature',
        string='Creature',
        ondelete='set null'  # 'set null' | 'restrict' | 'cascade'
    )
    # Related field — reads name from the linked creature record
    creature_name = fields.Char('Creature Name', related='creature_id.name')

    # --------------------
	# | Field validation |
	# --------------------
    @api.constrains('dob')
    def _check_dob(self):
        for record in self:
            if record.dob and record.dob.year < 2000:
                raise ValidationError(_('Year of birth must be ≥ 2000'))

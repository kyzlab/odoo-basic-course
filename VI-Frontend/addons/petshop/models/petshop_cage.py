# -*- coding: utf-8 -*-
from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class PetshopCage(models.Model):
    _name = "petshop.cage"
    _description = "Cage"

    name = fields.Char('Cage Name', required=True)
    code = fields.Char('Cage Code')
    capacity = fields.Integer(
        'Maximum Pets',
        help='Maximum number of pets this cage can hold.',
        default=1,
    )
    length = fields.Float('Length (m)')
    width = fields.Float('Width (m)')
    height = fields.Float('Height (m)')
    description = fields.Text('Description')

    # One2many — reverse of cage_id in petshop.pet
    pet_ids = fields.One2many(
        comodel_name='petshop.pet',
        inverse_name='cage_id',
        string='Pets'
    )

    # "size" supports both read and write
    size = fields.Char(
        'Size WxHxL',
        compute='_compute_size',
        inverse='_inverse_size',
        help='Width (m) x Height (m) x Length (m)'
    )

    @api.depends('width', 'height', 'length')
    def _compute_size(self):
        for record in self:
            record.size = f"{record.width} x {record.height} x {record.length}"
    
    def _inverse_size(self):
        for record in self:
            try:
                # Parse "W x H x L" → extract float "width", "height", "length"
                size_items = [si.strip() for si in record.size.split("x")] # ["W", "H", "L"]
                for sidx, sitem in enumerate(size_items):
                    if sidx == 0:
                        record.width = float(sitem)
                    elif sidx == 1:
                        record.height = float(sitem)
                    elif sidx == 2:
                        record.length = float(sitem)
            except Exception as e:
                _logger.error(f"Cannot parse size ({record.size}) properly. Error: {e}")
                pass

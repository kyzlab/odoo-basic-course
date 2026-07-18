from odoo import fields, models


class PetshopCageArchive(models.Model):
    """Prototype inheritance from petshop.cage.

    Creates a brand new model/table that inherits all fields and methods of
    petshop.cage and adds extra fields that only make sense for retired
    cages (retirement date and reason).
    """
    _name = 'petshop.cage.archive'
    _inherit = 'petshop.cage'
    _description = 'Cage Archive'

    retirement_date = fields.Date('Retirement Date', default=fields.Date.today, help='Date when the cage was retired from active use.')
    retirement_reason = fields.Char('Retirement Reason', help='Brief reason why the cage was retired (e.g., damaged, replaced).')

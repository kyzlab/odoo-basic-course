from odoo import fields, models

class PetshopStaff(models.Model):
    """Delegation inheritance from res.partner.
    A staff record delegates common partner fields (name, email, phone,
    address, etc.) to an underlying res.partner record while adding its own
    employee-specific fields (employee code and hire date).
    """
    _name = 'petshop.staff'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Petshop Staff'

    partner_id = fields.Many2one('res.partner', string='Related Partner', required=True, ondelete='cascade', auto_join=True)
    employee_code = fields.Char('Employee Code', required=True)
    hire_date = fields.Date('Hire Date')

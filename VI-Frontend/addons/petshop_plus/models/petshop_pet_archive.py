from odoo import fields, models

class PetshopPetArchive(models.Model):
    _name = 'petshop.pet.archive'   # new name = new DB table
    _inherit = 'petshop.pet'        # copy all fields & methods
    _description = 'Pet Archive'

    archive_code = fields.Char('Archive Code', required=True)
    archived_date = fields.Date('Archive Date', default=fields.Date.today)
    archive_reason = fields.Selection([
        ('deceased', 'Deceased'),
        ('sold',     'Sold'),
        ('rehomed',  'Rehomed'),
    ], string='Archive Reason', default='deceased', required=True)

    # Must override Many2many to avoid DB relation name conflict with petshop.pet. Avoid error:
    # TypeError: Many2many fields petshop.pet.archive.toy_ids and petshop.pet.toy_ids use the same table and columns
    toy_ids = fields.Many2many(
        comodel_name='product.product',
        string='Toys',
        relation='pet_archive_product_rel',   # unique relation table name
        column1='pet_archive_id',
        column2='product_id',
    )

    # Uncomment if model "petshop.vaccine" is implemented
    vaccine_ids = fields.Many2many(
        comodel_name='petshop.vaccine',
        string='Vaccines',
        relation='pet_archive_vaccine_rel',   # unique relation table name
        column1='col_pet_vaccine_id',
        column2='col_vaccine_pet_id'
    )
    
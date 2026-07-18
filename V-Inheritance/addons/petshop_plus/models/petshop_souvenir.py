from odoo import fields, models

class PetshopSouvenir(models.Model):
    _name = 'petshop.souvenir'
    _inherits = {'petshop.pet': 'pet_id'}   # delegate field access to petshop.pet
    _description = 'Pet Souvenir'

    pet_id = fields.Many2one('petshop.pet', required=True, ondelete='cascade', auto_join=True)
    souvenir_type = fields.Selection([
        ('toy', 'Toy'),
        ('photo', 'Photo'),
        ('keychain', 'Keychain'),
        ('plush', 'Plush Toy'),
    ], string='Type', default='plush', required=True)
    souvenir_color = fields.Selection([
        ('white', 'White'),
        ('black', 'Black'),
        ('brown', 'Brown'),
        ('rainbow', 'Rainbow'),
    ], string='Color', default='white', required=True)
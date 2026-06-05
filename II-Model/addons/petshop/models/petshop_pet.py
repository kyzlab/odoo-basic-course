# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import datetime

class PetshopPet(models.Model):
    _name = "petshop.pet"
    _description = "Pet"

    name = fields.Char('Pet Name', required=True)
    description = fields.Text('Description')
    dob = fields.Date('Date of Birth', required=False)
    gender = fields.Selection([
        ('male',   'Male'),
        ('female', 'Female'),
    ], string='Gender', default='male', required=True)
    feed_time = fields.Datetime('Last Feed Time', copy=False)
    is_alive = fields.Boolean('Alive', default=True)
    image = fields.Binary('Image', attachment=True, help='Pet photo')
    weight = fields.Float('Weight (kg)')
    weight_pound = fields.Float('Weight (lbs)')
    introduction = fields.Html('Introduction (EN)')

    # ------------------
	# | Computed field |
	# ------------------
    age = fields.Integer('Age', compute='_compute_age')

    # Many2one — a pet belongs to one species
    species_id = fields.Many2one(
        comodel_name='petshop.species',
        string='Species',
        ondelete='set null'  # 'set null' | 'restrict' | 'cascade'
    )
    # Related field — reads name from the linked species record
    species_name = fields.Char('Species Name', related='species_id.name')

    # --- Many2one: Cage, Doctor ---
    cage_id = fields.Many2one(
        comodel_name='petshop.cage',
        string='Cage',
        ondelete='set null'
    )
    doctor_id = fields.Many2one(
        comodel_name='res.partner',
        string='Attending Doctor'
    )

    # --- Self-referential: Mother & Father ---
    mother_id = fields.Many2one(
        comodel_name='petshop.pet',
        string='Mother',
        ondelete='set null'
    )
    father_id = fields.Many2one(
        comodel_name='petshop.pet',
        string='Father',
        ondelete='set null'
    )
    female_children_ids = fields.One2many(
        comodel_name='petshop.pet',
        inverse_name='mother_id',
        string='Female Children'
    )
    male_children_ids = fields.One2many(
        comodel_name='petshop.pet',
        inverse_name='father_id',
        string='Male Children'
    )
    
    # --- One2many: Meals ---
    meal_ids = fields.One2many(
        comodel_name='petshop.pet.meal',
        inverse_name='pet_id',            # ← will create this field in the target model petshop.pet.meal
        string='Meals'
    )
    
    # --- Many2many: Toys ---
    toy_ids = fields.Many2many(
        comodel_name='product.product',
        string='Toys',
        relation='pet_product_toy_rel',  # intermediate table name
        column1='col_pet_id',            # FK column pointing to petshop.pet
        column2='col_product_id'         # FK column pointing to product.product
    )   
    
    # --- Related field: Mother's name ---
    mother_name = fields.Char('Mother Name', related='mother_id.name')

    @api.depends('dob')
    def _compute_age(self):
        now = datetime.datetime.now()
        for record in self:
            if record.dob:
                delta = now.year - record.dob.year
                if delta < 0:
                    raise ValidationError(_('Invalid age: birth year is greater than current year!'))
                record.age = delta
            else:
                record.age = 0
		
	# --------------------
	# | Field validation |
	# --------------------
    @api.constrains('dob')
    def _check_dob(self):
        for record in self:
            if record.dob and record.dob.year < 1900:
                raise ValidationError(_('Invalid date of birth!'))
		
	# ------------------
	# | Field onchange |
	# ------------------
    @api.onchange('weight')
    def _update_weight_pound(self):
        self.weight_pound = self.weight * 2.204623

    @api.onchange('weight_pound')
    def _update_weight_kg(self):
        self.weight = self.weight_pound / 2.204623

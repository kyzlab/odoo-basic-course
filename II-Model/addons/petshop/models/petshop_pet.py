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

    owner_id = fields.Many2one(comodel_name='res.partner', string='Owner', ondelete='set null')
    vaccine_ids = fields.Many2many(comodel_name='petshop.vaccine',
        string='Vaccines',
        relation='pet_vaccine_rel',
        column1='col_pet_vaccine_id',
        column2='col_vaccine_pet_id'
    )

    number_of_children = fields.Integer('Number of Children', compute='_compute_number_of_children', store=True)

    @api.depends('female_children_ids', 'male_children_ids')
    def _compute_number_of_children(self):
        for record in self:
            record.number_of_children = len(record.female_children_ids) + len(record.male_children_ids)

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

    @api.constrains('mother_id', 'father_id')
    def _check_parent(self):
        """Ensure mother and father are valid and different."""
        for record in self:
            if record.mother_id and record.father_id:
                if record.mother_id.id == record.father_id.id:
                    raise ValidationError(
                        _('Mother and father cannot be the same animal!')
                    )
            if record.mother_id and record.mother_id.id == record.id:
                raise ValidationError(
                    _('The mother cannot be the animal itself!')
                )
            if record.father_id and record.father_id.id == record.id:
                raise ValidationError(
                    _('The father cannot be the animal itself!')
                )

    @api.constrains('gender', 'female_children_ids', 'male_children_ids')
    def _check_gender_children(self):
        """Ensure gender matches children types."""
        for record in self:
            if record.gender == 'male' and record.female_children_ids:
                raise ValidationError(
                    _('A male pet cannot have female children!')
                )
            if record.gender == 'female' and record.male_children_ids:
                raise ValidationError(
                    _('A female pet cannot have male children!')
                )

    # ------------------
    # | Field onchange |
    # ------------------
    @api.onchange('weight')
    def _update_weight_pound(self):
        self.weight_pound = self.weight * 2.204623

    @api.onchange('weight_pound')
    def _update_weight_kg(self):
        self.weight = self.weight_pound / 2.204623

    @api.onchange('species_id')
    def _onchange_species_id(self):
        """When species changes, reset cage and suggest a domain."""
        if self.species_id:
            # Suggest a warning message (optional)
            return {
                'warning': {
                    'title': 'Species Changed',
                    'message': f'Species set to: {self.species_id.name}. Please verify the cage assignment.',
                }
            }
        else:
            # Clear cage if no species selected
            self.cage_id = False

    @api.model
    def default_get(self, fields_list):
        """Override to set smart default values when opening a new form."""
        defaults = super().default_get(fields_list)
        # Always default to alive
        if 'is_alive' in fields_list:
            defaults['is_alive'] = True
        # Default gender to male
        if 'gender' in fields_list:
            defaults['gender'] = 'female'
        return defaults

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to run custom logic before/after record creation."""
        for vals in vals_list:
            # Auto-generate a nickname if not provided
            if not vals.get('nickname') and vals.get('name'):
                vals['nickname'] = vals['name'].split()[0]  # first word of name
        records = super().create(vals_list)
        # Post-creation logic: log a message
        for record in records:
            record.message_post(
                body=f"Pet '{record.name}' has been created.",
                message_type='comment'
            ) if hasattr(record, 'message_post') else None
        return records

    @api.private
    def _compute_internal_stats(self):
        """
        Private method — cannot be called via RPC.
        Only accessible from Python code on the server.
        """
        return {
            'total_toys': len(self.toy_ids),
            'total_meals': len(self.meal_ids),
            'age': self.age,
        }

import odoo
from odoo.http import request
import json as _json
# Import the original controller from petshop
from odoo.addons.petshop.controllers.main import PetshopController

import logging
_logger = logging.getLogger(__name__)

class PetshopPlusController(odoo.http.Controller):
    @odoo.http.route('/api/petshop/stats', type='http', auth='none', methods=['GET'], cors='*', csrf=False)
    def get_stats(self, **kw):
        """GET /api/petshop/stats — overall petshop statistics."""
        pets = request.env['petshop.pet'].sudo().search([])
        total = len(pets)
        male = len(pets.filtered(lambda p: p.gender == 'male'))
        female = len(pets.filtered(lambda p: p.gender == 'female'))
        vaccinated = len(pets.filtered(lambda p: p.is_vaccinated))
        return request.make_json_response({
            'total_pets': total,
            'male': male,
            'female': female,
            'vaccinated': vaccinated,
            'unvaccinated': total - vaccinated,
        }, status=200)

class PetshopControllerOverride(PetshopController):
    """Override existing petshop routes to add vaccine info."""
    @odoo.http.route('/api/petshop/pet/<int:pet_id>', type='http', auth='none', methods=['GET'], cors='*', csrf=False)
    def get_pet_by_id(self, pet_id, **kw):
        """Override: enrich original response with is_vaccinated field."""
        # Call original implementation first
        original = super().get_pet_by_id(pet_id, **kw)
        try:
            data = _json.loads(original.data)
            pet  = request.env['petshop.pet'].sudo().browse(pet_id)
            if pet.exists():
                data['is_vaccinated'] = pet.is_vaccinated
                data['vaccine_note']  = pet.vaccine_note
            return request.make_json_response(data, status=200)
        except Exception as e:
            _logger.error(e)
            return original   # fallback to original if anything fails

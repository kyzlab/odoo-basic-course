import odoo
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.http import request
import datetime
import logging
_logger = logging.getLogger(__name__)

def _convert_datetime(d):
    """Convert datetime/date object to string for JSON serialization."""
    if not d:
        return False
    if isinstance(d, datetime.datetime):
        return d.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
    return d.strftime(DEFAULT_SERVER_DATE_FORMAT)

class PetshopController(odoo.http.Controller):
    @odoo.http.route(route='/api/petshop/pets', type='http', auth='none', methods=['GET'], cors='*', csrf=False)
    def get_all_pets(self, **kw):
        """GET /api/petshop/pets — return all pets, with optional filters"""
        # Read optional query params from URL
        limit = int(request.httprequest.args.get('limit', 0)) or None
        species_id = request.httprequest.args.get('species_id')

        domain = []
        if species_id:
            domain.append(('species_id', '=', int(species_id)))

        pets = request.env['petshop.pet'].sudo().search(domain, limit=limit)
        result = []
        for p in pets:
            result.append({
                'id':        p.id,
                'name':      p.name,
                'gender':    p.gender,
                'weight':    p.weight,
                'species':   p.species_id.name if p.species_id else None,
                'feed_time': _convert_datetime(p.feed_time),
            })
        return request.make_json_response(result, status=200)

    @odoo.http.route('/api/petshop/pet/<int:pet_id>', type='http', auth='none', methods=['GET'], cors='*', csrf=False)
    def get_pet_by_id(self, pet_id, **kw):
        """GET /api/petshop/pet/<id> — return one pet or 404"""
        try:
            pet = request.env['petshop.pet'].sudo().browse(pet_id)
            if not pet.exists():
                return request.make_json_response(
                    {'error': 'Pet not found', 'id': pet_id}, status=404
                )
            return request.make_json_response({
                'id':        pet.id,
                'name':      pet.name,
                'gender':    pet.gender,
                'weight':    pet.weight,
                'dob':       _convert_datetime(pet.dob),
                'feed_time': _convert_datetime(pet.feed_time),
                'species':   pet.species_id.name if pet.species_id else None,
                'cage':      pet.cage_id.name if pet.cage_id else None,
            }, status=200)
        except Exception as e:
            _logger.error("get_pet_by_id error: %s", e)
            return request.make_json_response(
                {'error': 'Internal server error'}, status=500
            )

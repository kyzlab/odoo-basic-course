import odoo
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.http import request
import datetime
import json as _json
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

    # ------------------------------------------------------------------
    # Exercise 1: GET /api/petshop/species
    # ------------------------------------------------------------------
    @odoo.http.route(
        '/api/petshop/species', type='http', auth='none',
        methods=['GET'], cors='*', csrf=False)
    def get_all_species(self, **kw):
        """GET /api/petshop/species — return all species records.

        Response: list of {id, name, environment, is_rare}
        """
        try:
            species_records = request.env['petshop.species'].sudo().search([])
            result = []
            for species in species_records:
                result.append({
                    'id':          species.id,
                    'name':        species.name,
                    'environment': species.environment,
                    'is_rare':     species.is_rare,
                })
            _logger.info("get_all_species: returned %d records", len(result))
            return request.make_json_response(result, status=200)
        except Exception as e:
            _logger.error("get_all_species error: %s", e)
            return request.make_json_response(
                {'error': 'Internal server error'}, status=500
            )

    # ------------------------------------------------------------------
    # Exercise 2: GET /api/petshop/pet/<int:pet_id>/meals
    # ------------------------------------------------------------------
    @odoo.http.route(
        '/api/petshop/pet/<int:pet_id>/meals', type='http', auth='none',
        methods=['GET'], cors='*', csrf=False)
    def get_pet_meals(self, pet_id, **kw):
        """GET /api/petshop/pet/<id>/meals — return all meals of a pet.

        Response: {pet_id, pet_name, meals: [{product, volume, meal_time}]}
        Returns 404 when the pet does not exist.
        """
        try:
            pet = request.env['petshop.pet'].sudo().browse(pet_id)
            if not pet.exists():
                _logger.warning("get_pet_meals: pet_id=%s not found", pet_id)
                return request.make_json_response(
                    {'error': 'Pet not found', 'pet_id': pet_id}, status=404
                )

            meals_data = []
            for meal in pet.meal_ids:
                meals_data.append({
                    'product':   meal.product_id.name if meal.product_id else None,
                    'volume':    meal.volume,
                    'meal_time': meal.meal_time,
                })

            result = {
                'pet_id':   pet.id,
                'pet_name': pet.name,
                'meals':    meals_data,
            }
            _logger.info("get_pet_meals: pet_id=%s, meals=%d", pet_id, len(meals_data))
            return request.make_json_response(result, status=200)
        except Exception as e:
            _logger.error("get_pet_meals error: %s", e)
            return request.make_json_response(
                {'error': 'Internal server error'}, status=500
            )

    # ------------------------------------------------------------------
    # Exercise 3: GET /api/petshop/cage/<int:cage_id>/pets
    # ------------------------------------------------------------------
    @odoo.http.route(
        '/api/petshop/cage/<int:cage_id>/pets', type='http', auth='none',
        methods=['GET'], cors='*', csrf=False)
    def get_cage_pets(self, cage_id, **kw):
        """GET /api/petshop/cage/<id>/pets — return all pets in a cage.

        Response: list of {id, name, species, weight}
        Returns 404 when the cage does not exist.
        """
        try:
            cage = request.env['petshop.cage'].sudo().browse(cage_id)
            if not cage.exists():
                _logger.warning("get_cage_pets: cage_id=%s not found", cage_id)
                return request.make_json_response(
                    {'error': 'Cage not found', 'cage_id': cage_id}, status=404
                )

            pets_data = []
            for pet in cage.pet_ids:
                pets_data.append({
                    'id':      pet.id,
                    'name':    pet.name,
                    'species': pet.species_id.name if pet.species_id else None,
                    'weight':  pet.weight,
                })

            _logger.info("get_cage_pets: cage_id=%s, pets=%d", cage_id, len(pets_data))
            return request.make_json_response(pets_data, status=200)
        except Exception as e:
            _logger.error("get_cage_pets error: %s", e)
            return request.make_json_response(
                {'error': 'Internal server error'}, status=500
            )

    @odoo.http.route('/api/petshop/pet/create', type='http', auth='user', methods=['POST'], cors='*', csrf=False)
    def create_pet(self, **kw):
        """POST /api/petshop/pet/create — create a new pet (requires login)"""
        try:
            body = request.httprequest.get_data(as_text=True)
            data = _json.loads(body)
        except Exception:
            return request.make_json_response({'error': 'Invalid JSON body'}, status=400)

        name = data.get('name')
        if not name:
            return request.make_json_response({'error': 'Field "name" is required'}, status=400)

        vals = {
            'name':   name,
            'gender': data.get('gender', 'male'),
            'weight': float(data.get('weight', 0)),
        }
        if data.get('species_id'):
            vals['species_id'] = int(data['species_id'])

        try:
            pet = request.env['petshop.pet'].create(vals)
            return request.make_json_response(
                {'success': True, 'id': pet.id, 'name': pet.name}, status=201
            )
        except Exception as e:
            _logger.error("create_pet error: %s", e)
            return request.make_json_response({'error': str(e)}, status=500)

    @odoo.http.route('/api/petshop/pet/<int:pet_id>/update', type='http', auth='user', methods=['PUT'], cors='*', csrf=False)
    def update_pet(self, pet_id, **kw):
        """PUT /api/petshop/pet/<id>/update — update pet fields"""
        pet = request.env['petshop.pet'].browse(pet_id)
        if not pet.exists():
            return request.make_json_response({'error': 'Pet not found'}, status=404)

        try:
            body = request.httprequest.get_data(as_text=True)
            data = _json.loads(body)
        except Exception:
            return request.make_json_response({'error': 'Invalid JSON body'}, status=400)

        vals = {}
        if 'weight' in data:
            vals['weight'] = float(data['weight'])
        if 'gender' in data:
            vals['gender'] = data['gender']

        pet.write(vals)
        return request.make_json_response({'success': True, 'id': pet.id}, status=200)

    @odoo.http.route('/api/petshop/pet/<int:pet_id>/delete', type='http', auth='user', methods=['DELETE'], cors='*', csrf=False)
    def delete_pet(self, pet_id, **kw):
        """DELETE /api/petshop/pet/<id>/delete — unlink a pet record"""
        pet = request.env['petshop.pet'].browse(pet_id)
        if not pet.exists():
            return request.make_json_response({'error': 'Pet not found'}, status=404)
        pet.unlink()
        return request.make_json_response({'success': True}, status=200)

    @odoo.http.route(
	    '/api/petshop/species/create',
        type='jsonrpc',   # Odoo 19: 'jsonrpc' replaces 'json' from Odoo 18
        auth='user',
        csrf=False
    )
    def create_species(self, name, **kw):
        """
        POST /api/petshop/species/create
        Body (JSON-RPC format):
          {"jsonrpc": "2.0", "method": "call", "params": {"name": "Hamster", "environment": "ground"}}
        """
        if not name:
            return {'error': 'Field "name" is required'}
        environment = kw.get('environment', 'ground')
        species = request.env['petshop.species'].create({
            'name': name,
            'environment': environment,
        })
        return {'success': True, 'id': species.id, 'name': species.name}
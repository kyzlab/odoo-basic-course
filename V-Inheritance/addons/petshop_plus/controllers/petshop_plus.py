import odoo
from odoo.http import request

# Base controller of the `petshop` addon (routes to be overridden)
from odoo.addons.petshop.controllers.main import PetshopController, _convert_datetime

import logging
_logger = logging.getLogger(__name__)

class PetshopPlusController(odoo.http.Controller):
    """Extend the petshop_plus controller with additional read-only routes."""

    # ------------------------------------------------------------------
    # Exercise 1: GET /api/petshop/species/<int:species_id>/pets
    # ------------------------------------------------------------------
    @odoo.http.route('/api/petshop/species/<int:species_id>/pets', type='http', auth='none', methods=['GET'], cors='*', csrf=False)
    def get_species_pets(self, species_id, **kw):
        """GET /api/petshop/species/<id>/pets — return all pets of a species.

        Response: list of {id, name, gender, weight, cage}
        Returns 404 when the species does not exist.
        """
        try:
            species = request.env['petshop.species'].sudo().browse(species_id)
            if not species.exists():
                _logger.warning("get_species_pets: species_id=%s not found", species_id)
                return request.make_json_response({'error': 'Species not found', 'species_id': species_id}, status=404)

            pets = request.env['petshop.pet'].sudo().search([('species_id', '=', species.id)])
            result = [{
                'id': pet.id,
                'name': pet.name,
                'gender': pet.gender,
                'weight': pet.weight,
                'cage': pet.cage_id.name if pet.cage_id else None,
            } for pet in pets]

            _logger.info("get_species_pets: species_id=%s, pets=%d", species_id, len(result))
            return request.make_json_response(result, status=200)
        except Exception as e:
            _logger.error("get_species_pets error: %s", e)
            return request.make_json_response({'error': 'Internal server error'}, status=500)

    # ------------------------------------------------------------------
    # Exercise 3: GET /api/petshop/leaderboard
    # ------------------------------------------------------------------
    @odoo.http.route('/api/petshop/leaderboard', type='http', auth='none', methods=['GET'], cors='*', csrf=False)
    def get_leaderboard(self, **kw):
        """GET /api/petshop/leaderboard — top 5 heaviest pets.

        Response: list of {id, name, weight, species} ordered by weight DESC.
        """
        try:
            pets = request.env['petshop.pet'].sudo().search([], order='weight desc', limit=5)
            result = [{
                'id':      pet.id,
                'name':    pet.name,
                'weight':  pet.weight,
                'species': pet.species_id.name if pet.species_id else None,
            } for pet in pets]

            _logger.info("get_leaderboard: returned %d records", len(result))
            return request.make_json_response(result, status=200)
        except Exception as e:
            _logger.error("get_leaderboard error: %s", e)
            return request.make_json_response({'error': 'Internal server error'}, status=500)


class PetshopPetsListOverride(PetshopController):
    """Override the `petshop` pets list route to expose extra pet details."""

    # ------------------------------------------------------------------
    # Exercise 2: GET /api/petshop/pets (override)
    # ------------------------------------------------------------------
    @odoo.http.route('/api/petshop/pets', type='http', auth='none', methods=['GET'], cors='*', csrf=False)
    def get_all_pets(self, **kw):
        """Override: add is_vaccinated, description, state and age to each item."""
        try:
            limit = int(request.httprequest.args.get('limit', 0)) or None
            species_id = request.httprequest.args.get('species_id')

            domain = []
            if species_id:
                domain.append(('species_id', '=', int(species_id)))

            pets = request.env['petshop.pet'].sudo().search(domain, limit=limit)
            result = [{
                # --- Fields returned by the original controller ---
                'id':            pet.id,
                'name':          pet.name,
                'gender':        pet.gender,
                'weight':        pet.weight,
                'species':       pet.species_id.name if pet.species_id else None,
                'feed_time':     _convert_datetime(pet.feed_time),
                # --- Fields added by petshop_plus ---
                'is_vaccinated': pet.is_vaccinated,
                'description':   pet.description,
                'state':         pet.state,
                'age':           pet.age,
            } for pet in pets]

            _logger.info("get_all_pets (plus): returned %d records", len(result))
            return request.make_json_response(result, status=200)
        except Exception as e:
            _logger.error("get_all_pets (plus) error: %s", e)
            return request.make_json_response({'error': 'Internal server error'}, status=500)

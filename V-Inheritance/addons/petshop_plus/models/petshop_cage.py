from odoo import _, models
from odoo.exceptions import ValidationError

class PetshopCagePlus(models.Model):
    """In-place extension of petshop.cage.
    Adds a header button action that validates the current pet count against
    the cage's configured capacity.
    """
    _inherit = 'petshop.cage'

    def action_verify_capacity(self):
        """Check whether the number of assigned pets exceeds the cage capacity.
        Raises:
            ValidationError: when the pet count is greater than the capacity.
        """
        for cage in self:
            if cage.capacity > 0 and len(cage.pet_ids) > cage.capacity:
                raise ValidationError(_(
                    "The number of pets in cage '%(cage)s' (%(pets)d) exceeds its configured capacity (%(capacity)d).",
                    cage=cage.name,
                    pets=len(cage.pet_ids),
                    capacity=cage.capacity,
                ))
        return True

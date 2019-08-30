from .common import TestMealMenuBase
from odoo.tools import mute_logger
from psycopg2 import IntegrityError


class TestMealLocation(TestMealMenuBase):
    """ Location related tests
    """

    def test_required_fields(self):
        """Check if the required flag is set. No need to test if it works,
        odoo does that.
        """
        REQUIRED = ['name', 'key']

        Fields = self.env['ir.model.fields']
        MODEL = 'meal.location'

        for fld in REQUIRED:
            frecord = Fields.search([('model', '=', MODEL), ('name', '=', fld)])
            self.assertTrue(frecord.required)

    def test_has_images(self):
        vals = self.location_1_vals
        self.location_1 = self.env['meal.location'].create(vals)

        self.assertTrue(self.location_1.image)
        self.assertTrue(self.location_1.image_small)
        self.assertTrue(self.location_1.image_medium)


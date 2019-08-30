from odoo.tests.common import SavepointCase


class TestMealMenuBase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestMealMenuBase, cls).setUpClass()

        cls.location_1_vals = {
            'name': 'Cafeteria 1',
            'key': 'cafeteria_1',
            'description': 'Test description',
            'image': cls.env.ref('base.res_partner_address_1').image,
        }

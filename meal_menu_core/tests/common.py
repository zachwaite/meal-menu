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

        cls.location_2_vals = {
            'name': 'Cafeteria 2',
            'key': 'cafeteria_2',
            'description': 'Test description',
            'image': cls.env.ref('base.res_partner_address_1').image,
        }

        cls.time_1_vals = {
            'name': 'Breakfast',
            'key': 'breakfast',
        },

        cls.time_2_vals = {
            'name': 'Lunch',
            'key': 'lunch',
        },

        cls.time_3_vals = {
            'name': 'Supper',
            'key': 'supper',
        },


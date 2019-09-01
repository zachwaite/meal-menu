import datetime
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

    @classmethod
    def make_meal(cls):
        location = cls.env['meal.location'].create(cls.location_1_vals)
        breakfast = cls.env['meal.time'].create(cls.time_1_vals)
        Meal = cls.env['meal.meal']
        return Meal.create({
            'meal_date': datetime.date(2019, 11, 1),
            'meal_location_id': location.id,
            'meal_time_id': breakfast.id,
        })


    @classmethod
    def make_cycle(cls):
        location = cls.env['meal.location'].create(cls.location_1_vals)
        breakfast = cls.env['meal.time'].create(cls.time_1_vals)
        lunch = cls.env['meal.time'].create(cls.time_2_vals)
        dinner = cls.env['meal.time'].create(cls.time_3_vals)
        time_ids = [breakfast.id, lunch.id, dinner.id]
        cycle = cls.env['meal.cycle'].create([{
            'start_date': datetime.date(2019, 11, 1),
            'duration': 1,
            'meal_location_ids': [(6, 0, location.ids)],
            'meal_time_ids': [(6, 0, time_ids)],
        }])
        cycle.generate_meals()
        return cycle

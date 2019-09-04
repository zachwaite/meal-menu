import datetime
import re

from .common import TestMealMenuBase
from unittest.mock import MagicMock

from odoo.exceptions import UserError
from odoo.addons.meal_menu_core.models.meal_meal import Meal


class TestMealCycle(TestMealMenuBase):
    """Meal cycle tests
    """

    def test_required_fields(self):
        """Check if the required flag is set. No need to test if it works,
        odoo does that.
        """
        REQUIRED = ['start_date', 'duration']

        Fields = self.env['ir.model.fields']
        MODEL = 'meal.cycle'

        for fld in REQUIRED:
            frecord = Fields.search([('model', '=', MODEL), ('name', '=', fld)])
            self.assertTrue(frecord.required)

    def test_default_dates(self):
        """ check if default values are applying
        """
        vals = {}
        cycle = self.env['meal.cycle'].create(vals)
        self.assertEqual(cycle.start_date, cycle.get_default_cycle_start_date())
        self.assertEqual(cycle.duration, 21)

    def test_default_meal_locations(self):
        location = self.env['meal.location'].create(self.location_1_vals)
        cycle = self.env['meal.cycle'].create({})
        self.assertIn(location.id, cycle.meal_location_ids.ids)

    def test_default_meal_timess(self):
        time = self.env['meal.time'].create(self.time_1_vals)
        cycle = self.env['meal.cycle'].create({})
        self.assertIn(time.id, cycle.meal_time_ids.ids)

    def test_get_default_cycle_start_date(self):
        """ Mock the Meal.get_last_scheduled_meal_date() method for SOC
        """
        # test 1 fallback to tomorrow
        # clean meals for test
        # TODO: patch this to handle pre-existing data
        self.env['meal.meal'].search([]).unlink()
        MealCycle = self.env['meal.cycle']
        out = MealCycle.get_default_cycle_start_date()
        expected_out = datetime.date.today() + datetime.timedelta(days=1)
        self.assertEqual(out, expected_out)

        # test 2 existing meal history
        # setup
        mocked_last_meal_date = datetime.date(2019, 11, 1)
        next_expected_meal_date = datetime.date(2019, 11, 2)
        # mock method
        Meal.get_last_scheduled_meal_date = MagicMock(return_value=mocked_last_meal_date)
        # sanity check
        last_meal_date = Meal.get_last_scheduled_meal_date()
        self.assertEqual(last_meal_date, mocked_last_meal_date)

        # test
        expected_out = next_expected_meal_date
        out = MealCycle.get_default_cycle_start_date()
        self.assertEqual(out, expected_out)

    def test_meal_sequence(self):
        vals = {
            'start_date': datetime.date(2019, 12, 1),
            'duration': 1,
        }
        cycle = self.env['meal.cycle'].create(vals)
        pat = re.compile('CYCLE-[0-9]+')
        self.assertTrue(pat.match(cycle.name))

    def test_get_meal_count(self):
        cycle = self.make_cycle()
        get_ct = cycle.get_meal_count()
        self.assertEqual(get_ct, 3)

    def test_generate_meals_01(self):
        """ Test that generate_meals() gives the right number of unique dates
        """
        cafeteria_1 = self.env['meal.location'].create(self.location_1_vals)
        breakfast = self.env['meal.time'].create(self.time_1_vals)
        MealCycle = self.env['meal.cycle']
        vals = {
            'start_date': datetime.date(2019, 11, 2),
            'meal_location_ids': [(6, 0, cafeteria_1.ids)],
            'meal_time_ids': [(6, 0, breakfast.ids)],
        }
        cycle = MealCycle.create([vals])

        # sanity checks
        self.assertEqual(cycle.start_date, datetime.date(2019, 11, 2))
        self.assertEqual(cycle.duration, 21)
        self.assertEqual(cycle.end_date, datetime.date(2019, 11, 22))

        # test correct number of unique dates
        cycle.generate_meals()
        meals = cycle.meal_ids
        unique_meal_dates = set(meals.mapped('meal_date'))
        self.assertEqual(len(unique_meal_dates), 21)

    def test_generate_meals_02(self):
        """When I give 1 location (cafeteria_1) and 1 times (breakfast) and duration 3
           Then generate_meals() should give 3 meals
           And each meal should have location cafeteria_1
           And each meal should have time breakfast
        """
        cafeteria_1 = self.env['meal.location'].create(self.location_1_vals)
        breakfast = self.env['meal.time'].create(self.time_1_vals)
        MealCycle = self.env['meal.cycle']
        vals = {
            'start_date': datetime.date(2019, 11, 2),
            'duration': 3,
            'meal_location_ids': [(6, 0, cafeteria_1.ids)],
            'meal_time_ids': [(6, 0, breakfast.ids)],
        }
        cycle = MealCycle.create([vals])
        cycle.generate_meals()
        meals = cycle.meal_ids

        # 4 meals
        self.assertEqual(len(meals), 3)

        # cafeteria_1
        locations = meals.mapped('meal_location_id')
        self.assertEqual(locations, cafeteria_1)

        # breakfast
        times = meals.mapped('meal_time_id')
        self.assertEqual(times, breakfast)

    def test_generate_meals_03(self):
        """When I give 2 location (cafeteria_1, cafeteria_2) and 2 times (breakfast, lunch) and duration 3
           Then generate_meals() should give 12 meals
           And 3 meals should be (cafeteria_1, breakfast)
           And 3 meals should be (cafeteria_1, lunch)
           And 3 meals should be (cafeteria_2, breakfast)
           And 3 meals should be (cafeteria_2, lunch)
        """
        cafeteria_1 = self.env['meal.location'].create(self.location_1_vals)
        cafeteria_2 = self.env['meal.location'].create(self.location_2_vals)
        breakfast = self.env['meal.time'].create(self.time_1_vals)
        lunch = self.env['meal.time'].create(self.time_2_vals)
        MealCycle = self.env['meal.cycle']
        vals = {
            'start_date': datetime.date(2019, 11, 2),
            'duration': 3,
            'meal_location_ids': [(6, 0, [cafeteria_1.id, cafeteria_2.id])],
            'meal_time_ids': [(6, 0, [breakfast.id, lunch.id])],
        }
        cycle = MealCycle.create([vals])
        cycle.generate_meals()
        meals = cycle.meal_ids

        # 12 meals
        self.assertEqual(len(meals), 12)

        # 3 cafeteria_1, breakfast
        rs = meals.filtered(lambda m: m.meal_location_id == cafeteria_1 and m.meal_time_id == breakfast)
        self.assertEqual(len(rs), 3)

        # 3 cafeteria_2, breakfast
        rs = meals.filtered(lambda m: m.meal_location_id == cafeteria_2 and m.meal_time_id == breakfast)
        self.assertEqual(len(rs), 3)

        # 3 cafeteria_1, lunch
        rs = meals.filtered(lambda m: m.meal_location_id == cafeteria_1 and m.meal_time_id == lunch)
        self.assertEqual(len(rs), 3)

        # 3 cafeteria_2, lunch
        rs = meals.filtered(lambda m: m.meal_location_id == cafeteria_2 and m.meal_time_id == lunch)
        self.assertEqual(len(rs), 3)

    def test_generate_meals_04(self):
        """When I give 1 location (cafeteria_1) and 3 times (breakfast, lunch, supper) and duration 21
           Then generate_meals() should give 63 meals
           And 21 meals should be (cafeteria_1, breakfast)
           And 21 meals should be (cafeteria_1, lunch)
           And 21 meals should be (cafeteria_1, supper)
        """
        cafeteria_1 = self.env['meal.location'].create(self.location_1_vals)
        breakfast = self.env['meal.time'].create(self.time_1_vals)
        lunch = self.env['meal.time'].create(self.time_2_vals)
        supper = self.env['meal.time'].create(self.time_3_vals)
        MealCycle = self.env['meal.cycle']
        vals = {
            'start_date': datetime.date(2019, 11, 2),
            'duration': 21,
            'meal_location_ids': [(6, 0, [cafeteria_1.id])],
            'meal_time_ids': [(6, 0, [breakfast.id, lunch.id, supper.id])],
        }
        cycle = MealCycle.create([vals])
        cycle.generate_meals()
        meals = cycle.meal_ids

        # 63 meals
        self.assertEqual(len(meals), 63)

        # 21 breakfast
        rs = meals.filtered(lambda m: m.meal_location_id == cafeteria_1 and m.meal_time_id == breakfast)
        self.assertEqual(len(rs), 21)

        # 21 lunch
        rs = meals.filtered(lambda m: m.meal_location_id == cafeteria_1 and m.meal_time_id == lunch)
        self.assertEqual(len(rs), 21)

        # 21 supper
        rs = meals.filtered(lambda m: m.meal_location_id == cafeteria_1 and m.meal_time_id == supper)
        self.assertEqual(len(rs), 21)

    def test_publish_cascade(self):
        cycle = self.make_cycle()
        # sanity check
        self.assertEqual(cycle.state, 'draft')
        meal_states = cycle.meal_ids.mapped('state')
        self.assertEqual(set(['draft']), set(meal_states))

        # test 
        cycle.write({'state': 'published'})
        self.assertEqual(cycle.state, 'published')
        meal_states = cycle.meal_ids.mapped('state')
        self.assertEqual(set(['published']), set(meal_states))

    def test_action_publish_cycle(self):
        cycle = self.make_cycle()
        # test 
        cycle.action_publish_cycle()
        self.assertEqual(cycle.state, 'published')
        meal_states = cycle.meal_ids.mapped('state')
        self.assertEqual(set(['published']), set(meal_states))

    def test_no_unlink_published(self):
        cycle = self.make_cycle()
        cycle.action_publish_cycle()
        with self.assertRaises(UserError):
            cycle.unlink()


    def test_fkeys(self):
        cycle = self.make_cycle()
        meals = cycle.meal_ids
        meals.write({
            'meal_location_id': False,
            'meal_time_id': False,
        })

        cycle.unlink()
        # per /odoo/odoo/addons/tests/test_orm.py, read on a deleted record should come back empty
        # so use that for this test
        self.assertFalse(meals.read())


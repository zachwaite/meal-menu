import datetime
import json
from unittest.mock import MagicMock, patch
from psycopg2 import IntegrityError, InternalError

from odoo.exceptions import UserError
from odoo.tools import mute_logger
from odoo.addons.meal_menu_core.models.meal_meal import Meal
from .common import TestMealMenuBase


class TestMealMeal(TestMealMenuBase):
    """Meal tests
    """

    def setUp(self):
        super(TestMealMeal, self).setUp()

        # data
        self.mocked_last_meal_date = datetime.date(2019, 11, 1)
        self.next_expected_meal_date = datetime.date(2019, 11, 2)

        # mock method
        Meal.get_last_scheduled_meal_date = MagicMock(return_value=self.mocked_last_meal_date)

        # sanity check
        last_meal_date = Meal.get_last_scheduled_meal_date()
        self.assertEqual(last_meal_date, self.mocked_last_meal_date)


    def test_required_fields(self):
        """Check if the required flag is set. No need to test if it works,
        odoo does that.
        """
        # REQUIRED = ['meal_date', 'meal_location_id', 'meal_time_id']
        REQUIRED = []

        Fields = self.env['ir.model.fields']
        MODEL = 'meal.meal'

        for fld in REQUIRED:
            frecord = Fields.search([('model', '=', MODEL), ('name', '=', fld)])
            self.assertTrue(frecord.required)

    def test_get_last_scheduled_meal_date(self):
        """
        """
        pass


    def test_generate_meal_data(self):
        data = [
            {
                'meal_cycle_id': 1,
                'meal_location_ids': [1],
                'meal_time_ids': [1],
                'date_series': [
                    datetime.date(2019, 11, 1),
                    datetime.date(2019, 11, 2),
                    datetime.date(2019, 11, 3),
                    datetime.date(2019, 11, 4),
                ],
                'expected': [
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 1), 'meal_location_id': 1, 'meal_time_id': 1},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 2), 'meal_location_id': 1, 'meal_time_id': 1},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 3), 'meal_location_id': 1, 'meal_time_id': 1},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 4), 'meal_location_id': 1, 'meal_time_id': 1},
                ],
            },
            {
                'meal_cycle_id': 1,
                'meal_location_ids': [1, 2],
                'meal_time_ids': [1, 2],
                'date_series': [
                    datetime.date(2019, 11, 1),
                    datetime.date(2019, 11, 2),
                    datetime.date(2019, 11, 3),
                    datetime.date(2019, 11, 4),
                ],
                'expected': [
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 1), 'meal_location_id': 1, 'meal_time_id': 1},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 1), 'meal_location_id': 1, 'meal_time_id': 2},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 1), 'meal_location_id': 2, 'meal_time_id': 1},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 1), 'meal_location_id': 2, 'meal_time_id': 2},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 2), 'meal_location_id': 1, 'meal_time_id': 1},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 2), 'meal_location_id': 1, 'meal_time_id': 2},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 2), 'meal_location_id': 2, 'meal_time_id': 1},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 2), 'meal_location_id': 2, 'meal_time_id': 2},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 3), 'meal_location_id': 1, 'meal_time_id': 1},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 3), 'meal_location_id': 1, 'meal_time_id': 2},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 3), 'meal_location_id': 2, 'meal_time_id': 1},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 3), 'meal_location_id': 2, 'meal_time_id': 2},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 4), 'meal_location_id': 1, 'meal_time_id': 1},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 4), 'meal_location_id': 1, 'meal_time_id': 2},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 4), 'meal_location_id': 2, 'meal_time_id': 1},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 4), 'meal_location_id': 2, 'meal_time_id': 2},
                ],
            }
        ]
        Meal = self.env['meal.meal']
        for case in data:
            rs = Meal.generate_meal_data(case['meal_cycle_id'], case['meal_location_ids'], case['meal_time_ids'], case['date_series'])
            for rs_item, expected_item in zip(rs, case['expected']):
                self.assertDictEqual(rs_item, expected_item)

    def test_meal_label(self):
        meal = self.make_meal()
        # date = Friday, 11/1/19
        self.assertEqual(meal.meal_label, 'Fri')

    @mute_logger('odoo.sql_db')
    def test_fkeys_01(self):
        meal = self.make_meal()

        with self.assertRaises((IntegrityError, InternalError)):
            meal.meal_location_id.unlink()

    @mute_logger('odoo.sql_db')
    def test_fkeys_02(self):
        meal = self.make_meal()

        with self.assertRaises((IntegrityError, InternalError)):
            meal.meal_time_id.unlink()

    def test_no_unlink_published(self):
        meal = self.make_meal()
        meal.write({'state': 'published'})
        with self.assertRaises(UserError):
            meal.unlink()

    def test_get_meal_data_01(self):
        with patch('odoo.addons.meal_menu_core.models.meal_meal.today') as mocked_today:
            mocked_today.return_value = datetime.date(2019, 11, 1)
            assert mocked_today() == datetime.date(2019, 11, 1)
            Meal = self.env['meal.meal']
            cycle = self.make_cycle()
            cycle.action_publish_cycle()

            flds = ['meal_date', 'state']
            data = Meal._get_meal_data(delta=0, time_key='lunch', location_key='cafeteria_1', fields=flds)
            for rec in data:
                del rec['id']
            self.assertDictEqual(data[0], {
                'meal_date': datetime.date(2019, 11, 1),
                'state': 'published',
            })

    def test_get_meal_data_02(self):
        with patch('odoo.addons.meal_menu_core.models.meal_meal.today') as mocked_today:
            mocked_today.return_value = datetime.date(2019, 11, 1)
            assert mocked_today() == datetime.date(2019, 11, 1)
            Meal = self.env['meal.meal']
            cycle = self.make_cycle()
            cycle.action_publish_cycle()

            flds = ['meal_date', 'state']
            data = Meal.get_meal_data(delta=0, time_key='lunch', location_key='cafeteria_1', fields=flds)
            reloaded = json.loads(data)
            for rec in reloaded:
                del rec['id']
                self.assertDictEqual(rec, {
                    'meal_date': '2019-11-01',
                    'state': 'published',
                })

    def test_group_by_week(self):
        cycle = self.make_cycle()
        grouped = cycle.meal_ids.group_by_week()
        for k, v in grouped.items():
            self.assertEqual(len(v), 3)

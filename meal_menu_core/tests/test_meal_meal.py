import datetime
from .common import TestMealMenuBase
from unittest.mock import MagicMock

from odoo.addons.meal_menu_core.models.meal_meal import Meal


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
        REQUIRED = ['meal_date', 'meal_cycle_id']

        Fields = self.env['ir.model.fields']
        MODEL = 'meal.meal'

        for fld in REQUIRED:
            frecord = Fields.search([('model', '=', MODEL), ('name', '=', fld)])
            self.assertTrue(frecord.required)

    def test_generate_meal_data(self):
        data = [
            {
                'meal_cycle_id': 1,
                'date_series': [
                    datetime.date(2019, 11, 1),
                    datetime.date(2019, 11, 2),
                    datetime.date(2019, 11, 3),
                    datetime.date(2019, 11, 4),
                ],
                'expected': [
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 1)},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 2)},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 3)},
                    {'meal_cycle_id': 1, 'meal_date': datetime.date(2019, 11, 4)},
                ],
            }
        ]
        Meal = self.env['meal.meal']
        for case in data:
            rs = Meal.generate_meal_data(case['meal_cycle_id'], case['date_series'])
            for rs_item, expected_item in zip(rs, case['expected']):
                self.assertDictEqual(rs_item, expected_item)


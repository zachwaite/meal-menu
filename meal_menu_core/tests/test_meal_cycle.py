import datetime
from .common import TestMealMenuBase
from unittest.mock import MagicMock

from odoo.addons.meal_menu_core.models.meal_meal import Meal


class TestMealCycle(TestMealMenuBase):
    """Meal cycle tests
    """

    def setUp(self):
        super(TestMealCycle, self).setUp()

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
        REQUIRED = ['start_date', 'duration']

        Fields = self.env['ir.model.fields']
        MODEL = 'meal.cycle'

        for fld in REQUIRED:
            frecord = Fields.search([('model', '=', MODEL), ('name', '=', fld)])
            self.assertTrue(frecord.required)

    def test_get_default_cycle_start_date(self):
        """ Mock the Meal.get_last_scheduled_meal_date() method for SOC
        """
        expected_out = self.next_expected_meal_date
        last_meal_date = Meal.get_last_scheduled_meal_date()
        MealCycle = self.env['meal.cycle']
        out = MealCycle.get_default_cycle_start_date()
        self.assertEqual(out, expected_out)

    def test_generate_meals(self):
        """
        """
        raise NotImplementedError()

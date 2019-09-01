import datetime
from odoo import models, fields, api, _ 


class MealCycle(models.Model):
    _name = 'meal.cycle'
    _description = 'Collection of meals'
    _inherit = ['daterange.mixin']

    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
    ], default='draft',
        help='Published = visible to external clients',
    )

    active = fields.Boolean(
        default=True,
    )

    meal_ids = fields.One2many(
        comodel_name='meal.meal',
        inverse_name='meal_cycle_id',
    )
    # meal_location_ids
    # meal_time_ids

    def get_default_cycle_start_date(self):
        """Use the history to get the next upcoming cycle start
        """
        Meal = self.env['meal.meal']
        last_meal_date = Meal.get_last_scheduled_meal_date()
        return last_meal_date + datetime.timedelta(days=1)

    @api.multi
    def generate_meals(self):
        """Generate a collection of meals based on the other attributes.

        This should be fired on button click, perhaps in wizard

        Ensure one to prevent confusion in finding default start date
        """
        self.ensure_one()
        Meal = self.env['meal.meal']
        vals_list = []
        date_series = self.get_date_series(self.start_date, self.end_date)
        # TODO: This will need additional params for meal_time_ids, meal_location_ids
        meal_data = Meal.generate_meal_data(self.id, date_series)
        return Meal.create(meal_data)

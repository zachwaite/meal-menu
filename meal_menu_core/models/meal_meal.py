from odoo import models, fields, api, _ 

from .mixins import OrmExtensions


class Meal(models.Model, OrmExtensions):
    _name = 'meal.meal'
    _description = 'A single meal'

    meal_date = fields.Date(
        required=True,
        help='The scheduled date of the meal',
    )

    meal_label = fields.Char(
        string='Meal Day Label',
        compute='_compute_meal_label',
    )

    active = fields.Boolean(
        default=True,
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
    ], default='draft',
        help='Published = visible to external clients',
    )

    meal_cycle_id = fields.Many2one(
        comodel_name='meal.cycle',
    )

    meal_location_id = fields.Many2one(
        comodel_name='meal.location',
        required=True,
    )

    meal_time_id = fields.Many2one(
        comodel_name='meal.time',
        required=True,
    )

    def generate_meal_data(self, meal_cycle_id, meal_location_ids, meal_time_ids, date_series):
        data = []
        for dat in date_series:
            vals = {
                'meal_cycle_id': meal_cycle_id,
                'meal_date': dat,
            }
            for loc in meal_location_ids:
                vals.update({'meal_location_id': loc})
                for t in meal_time_ids:
                    vals.update({'meal_time_id': t})
                    # have to create a new dict, else reference semantics apply
                    data.append(dict(vals))
        return data

    def get_last_scheduled_meal_date(self):
        """Search the meal history for the last meal
        """
        last_meal = self.search([], limit=1, order='meal_date')
        if last_meal:
            return last_meal.meal_date
        else:
            return False

    def get_meal_weekday(self, meal_date):
        return meal_date.strftime('%a')

    def get_meal_label(self, meal_date, special_label):
        """Designed to allow injecting a special label instead of normal weekday
        """
        if special_label:
            return special_label
        else:
            return self.get_meal_weekday(meal_date)

    @api.multi
    def _compute_meal_label(self):
        # TODO: use special labels
        for record in self:
            record.meal_label = record.get_meal_label(record.meal_date, False)


from odoo import models, fields, api, _ 


class Meal(models.Model):
    _name = 'meal.meal'
    _description = 'A single meal'

    meal_date = fields.Date(
        required=True,
        help='The scheduled date of the meal',
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
        required=True,
    )

    # TODO: add params for meal_time_ids, meal_location_ids
    def generate_meal_data(self, meal_cycle_id, date_series):
        data = []
        for dat in date_series:
            vals = {
                'meal_cycle_id': meal_cycle_id,
                'meal_date': dat,
            }
            data.append(vals)
        return data


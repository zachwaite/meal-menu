from odoo import models, fields, api

from .mixins import OrmExtensions


class MealTime(models.Model, OrmExtensions):
    """A meal time

    Note: create multi
    """
    _name = 'meal.time'
    _description = 'The time details for the meal'
    _inherit = ['descriptor.mixin', 'image.mixin', 'timespan.mixin']

    color = fields.Integer()

    _sql_constraints = [
        ('meal_time_key_unique', 'unique (key)', 'The name of this record should be unique'),
    ]


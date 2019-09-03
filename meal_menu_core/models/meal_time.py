from odoo import models, fields, api

from .mixins import OrmExtensions


class MealTime(models.Model, OrmExtensions):
    """A meal time

    Note: create multi
    """
    _name = 'meal.time'
    _description = 'The time details for the meal'
    _inherit = ['descriptor.mixin', 'image.mixin', 'timespan.mixin']


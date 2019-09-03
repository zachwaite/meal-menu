from odoo import models, fields, api
from .mixins import OrmExtensions


class MealLocation(models.Model, OrmExtensions):
    """ A dining location

    Note: create multi
    """
    _name = 'meal.location'
    _description = 'The location where a meal will be served'
    _inherit = ['descriptor.mixin', 'image.mixin']


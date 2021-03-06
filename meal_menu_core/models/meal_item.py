from odoo import models, fields, api, _ 

from .mixins import OrmExtensions

class MealItem(models.Model, OrmExtensions):
    """ A single food offering

    Note: create multi
    """
    _name = 'meal.item'
    _description = 'A single food offering'
    _inherit = ['descriptor.mixin', 'image.mixin']

    category_id = fields.Many2one(
        comodel_name='meal.item.category',
        help='The type of item. e.g. entree, appetizer',
        ondelete='restrict',
    )


class MealItemCategory(models.Model):
    """ A food category.

    Note: create multi
    """
    _name = 'meal.item.category'
    _description = 'Category of a food item'
    _inherit = ['descriptor.mixin']

    meal_item_ids = fields.One2many(
        comodel_name='meal.item',
        inverse_name='category_id',
    )

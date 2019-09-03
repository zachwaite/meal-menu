from odoo import models, fields, api, _ 


class Meal(models.Model):
    _inherit = 'meal.meal'

    entree_1 = fields.Many2one(comodel_name='meal.item')
    entree_2 = fields.Many2one(comodel_name='meal.item')
    appetizer_1 = fields.Many2one(comodel_name='meal.item')
    appetizer_2 = fields.Many2one(comodel_name='meal.item')
    dessert_1 = fields.Many2one(comodel_name='meal.item')

    entree_filter = fields.Many2one(
        comodel_name='meal.item.category',
        default=lambda self: self.env.ref('meal_menu_demo.category_entree').id,
    )

    appetizer_filter = fields.Many2one(
        comodel_name='meal.item.category',
        default=lambda self: self.env.ref('meal_menu_demo.category_appetizer').id,
    )

    dessert_filter = fields.Many2one(
        comodel_name='meal.item.category',
        default=lambda self: self.env.ref('meal_menu_demo.category_dessert').id,
    )


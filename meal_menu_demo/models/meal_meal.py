from odoo import models, fields, api, _ 


class Meal(models.Model):
    _inherit = 'meal.meal'

    entree_1 = fields.Many2one(comodel_name='meal.item')
    entree_2 = fields.Many2one(comodel_name='meal.item')
    appetizer_1 = fields.Many2one(comodel_name='meal.item')
    appetizer_2 = fields.Many2one(comodel_name='meal.item')
    dessert_1 = fields.Many2one(comodel_name='meal.item')


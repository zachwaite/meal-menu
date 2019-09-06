from odoo import models, fields, api, _ 
from odoo.exceptions import UserError


class MealDay(models.Model):
    _name = 'meal.day'
    _description = 'Collection of meals for a meal_date'
    _rec_name = 'meal_date'

    # to be overriden
    ITEM_FIELDS = []

    meal_date = fields.Date(
        required=True,
        readonly=True,
    )

    meal_ids = fields.One2many(
        comodel_name='meal.meal',
        inverse_name='meal_day_id',
    )

    meal_cycle_id = fields.Many2one(
        comodel_name='meal.cycle',
        compute='_compute_meal_cycle_id',
        store=True,
        help='The meal cycle owning the meals. Will always be a singleton as a date is never split cross cycle',
    )

    meal_item_ids = fields.Many2many(
        comodel_name='meal.item',
        compute='_compute_meal_item_ids',
    )

    @api.multi
    def _compute_meal_item_ids(self):
        for record in self:
            record.meal_item_ids = record.meal_ids.mapped('meal_item_ids')

    @api.multi
    @api.depends('meal_ids', 'meal_ids.meal_cycle_id')
    def _compute_meal_cycle_id(self):
        for record in self:
            cycle_rs = record.meal_ids.mapped('meal_cycle_id')
            if len(cycle_rs) > 1:
                raise UserError('Meal Day must only belong to one Meal Cycle')
            record.meal_cycle_id = cycle_rs.id

    def get_meal_item(self, key, slot):
        """Get the related meal item from meal_ids
        """
        self.ensure_one()
        meal = self.meal_ids.filtered(lambda m: m.meal_time_id.key == key)
        return meal[slot]

    def set_meal_item(self, key, slot, val):
        self.ensure_one()
        meal = self.meal_ids.filtered(lambda m: m.meal_time_id.key == key)
        meal[slot] = val



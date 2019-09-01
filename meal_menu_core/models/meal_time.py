from odoo import models, fields, api


class MealTime(models.Model):
    _name = 'meal.time'
    _description = 'The time details for the meal'
    _inherit = ['descriptor.mixin', 'image.mixin', 'timespan.mixin']

    @api.model
    def create(self, vals):
        self._prepare_image_vals(vals)
        return super(MealTime, self).create(vals)



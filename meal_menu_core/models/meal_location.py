from odoo import models, fields, api


class MealLocation(models.Model):
    _name = 'meal.location'
    _description = 'The location where a meal will be served'
    _inherit = ['descriptor.mixin', 'image.mixin']

    @api.model
    def create(self, vals):
        self._prepare_image_vals(vals)
        return super(MealLocation, self).create(vals)



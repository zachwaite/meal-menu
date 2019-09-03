from odoo import models, fields, api
from .mixins import OrmExtensions


class MealLocation(models.Model, OrmExtensions):
    _name = 'meal.location'
    _description = 'The location where a meal will be served'
    _inherit = ['descriptor.mixin', 'image.mixin']

    @api.model
    def create(self, vals):
        self._prepare_image_vals(vals)
        rs = super(MealLocation, self).create(vals)
        rs._postprocess_images()
        return rs

    @api.multi
    def write(self, vals):
        rs = super(MealLocation, self).write(vals)
        if self.IMAGE_FIELDS.intersection(set(vals.keys())):
            self._postprocess_images()
        return True



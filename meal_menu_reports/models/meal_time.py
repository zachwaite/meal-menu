from odoo import models, fields, api, _ 


class MealTime(models.Model):
    _inherit = 'meal.time'

    IMAGE_FIELDS = {'image', 'image_small', 'image_medium', 'meal_report_image'}

    meal_report_image = fields.Binary(
        attachment=True,
    )



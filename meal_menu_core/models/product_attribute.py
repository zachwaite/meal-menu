from odoo import models, fields, api, _ 


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    create_variant = fields.Selection(default='no_variant')

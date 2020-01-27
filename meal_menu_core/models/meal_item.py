from collections import defaultdict
from odoo import models, fields, api, _ 

from .mixins import OrmExtensions

class MealItem(models.Model, OrmExtensions):
    """ A single food offering

    Note: create multi
    """
    _name = 'meal.item'
    _description = 'A single food offering'
    _inherit = ['image.mixin']
    _inherits = {'product.template': 'product_tmpl_id'}

    @api.model_cr_context
    def _init_column(self, column_name):
        """Override this hook to set custom default values for product_tmpl_id
        See: odoo/odoo/models.py

        Overridden in the same manner as odoo/addons/hr_attendence/models/hr_employee.py

        Args:
            column_name (str): The string field name from the model definintion
        """
        if column_name == 'product_tmpl_id':
            print('initializing' + '=' * 20)
            sql = 'SELECT id FROM meal_item WHERE product_tmpl_id IS NULL'
            self.env.cr.execute(sql)
            record_ids = [tup[0] for tup in self.env.cr.fetchall()]
            records = self.env['meal.item'].browse(record_ids)
            for record in records:
                tmpl = self.env['product.template'].create({
                    'name': record.name or 'ZZZZ',
                    'image': record.image,
                    'description': record.description,
                    'sequence': record.sequence,
                })
                sql = 'UPDATE meal_item SET product_tmpl_id = %s WHERE id = %s' % (tmpl.id, record.id)
                self.env.cr.execute(sql)
        super(MealItem, self)._init_column(column_name)

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product Template',
        auto_join=True,
        index=True,
        ondelete='cascade',
        required=True,
    )

    category_id = fields.Many2one(
        comodel_name='meal.item.category',
        help='The type of item. e.g. entree, appetizer',
        ondelete='restrict',
    )

    # inherits overlaps:
    # name, key, description, sequence
    # image, image_small, image_medium
    #
    # broadcastng common values to it's product
    # image = fields.Binary(
    #     compute='_compute_image',
    #     inverse='_inverse_image',
    #     store=True,
    # )

    # @api.multi
    # @api.depends('product_tmpl_id.image')
    # def _compute_image(self):
    #     for record in self:
    #         record.image = record.product_tmpl_id.image

    # def _inverse_image(self):
    #     self.product_tmpl_id.image = self.image

    # name = fields.Char(
    #     compute='_compute_name',
    #     inverse='_inverse_name',
    #     store=True,
    #     required=True,
    # )

    # @api.multi
    # @api.depends('product_tmpl_id.name')
    # def _compute_name(self):
    #     for record in self:
    #         record.name = record.product_tmpl_id.name

    # def _inverse_name(self):
    #     self.product_tmpl_id.name = self.name

    # description = fields.Text(
    #     compute='_compute_description',
    #     inverse='_inverse_description',
    #     store=True,
    # )

    # @api.multi
    # @api.depends('product_tmpl_id.description')
    # def _compute_description(self):
    #     for record in self:
    #         record.description = record.product_tmpl_id.description

    # def _inverse_description(self):
    #     self.product_tmpl_id.description = self.description

    # sequence = fields.Integer(
    #     compute='_compute_sequence',
    #     inverse='_inverse_sequence',
    #     store=True,
    # )

    # @api.multi
    # @api.depends('product_tmpl_id.sequence')
    # def _compute_sequence(self):
    #     for record in self:
    #         record.sequence = record.product_tmpl_id.sequence

    # def _inverse_sequence(self):
    #     self.product_tmpl_id.sequence = self.sequence

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


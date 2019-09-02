import datetime
from odoo import models, fields, api, _ 

from .mixins import OrmExtensions

class MealCycle(models.Model, OrmExtensions):
    _name = 'meal.cycle'
    _description = 'Collection of meals'
    _inherit = ['daterange.mixin']

    name = fields.Char(
        default=lambda self: 'New',
        readonly=True,
        required=True,
        copy=False,
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
    ], default='draft',
        help='Published = visible to external clients',
    )

    active = fields.Boolean(
        default=True,
    )

    meal_ids = fields.One2many(
        comodel_name='meal.meal',
        inverse_name='meal_cycle_id',
    )

    meal_count = fields.Integer(
        help='The number of meals planned for this cycle',
        compute='_compute_meal_count',
    )

    meal_location_ids = fields.Many2many(
        comodel_name='meal.location',
    )

    meal_time_ids = fields.Many2many(
        comodel_name='meal.time',
    )

    # extending from daterange.mixin
    start_date = fields.Date(
        default=lambda self: self.get_default_cycle_start_date(),
        help='First day of the meal cycle',
    )

    end_date = fields.Date(
        help='Last day of the meal cycle',
    )

    duration = fields.Integer(
        help='The number of days in this cycle',
    )

    # ----------------- Private ------------------------------

    def get_default_meal_locations(self):
        """Use all available meal locations
        """
        MealLocation = self.env['meal.location']
        locations = MealLocation.get_all()
        return locations

    def get_default_meal_times(self):
        """Use all available meal times
        """
        MealTime = self.env['meal.time']
        times = MealTime.get_all()
        return times

    def get_meal_count(self):
        """The number of meals planned for this cycle
        """
        return len(self.meal_ids)

    def get_default_cycle_start_date(self):
        """Use the history to get the next upcoming cycle start
        """
        Meal = self.env['meal.meal']
        last_meal_date = Meal.get_last_scheduled_meal_date()
        if last_meal_date:
            return last_meal_date + datetime.timedelta(days=1)
        else:
            return datetime.date.today() + datetime.timedelta(days=1)

    # ----------------- Public Api ------------------------------

    @api.multi
    def _compute_meal_count(self):
        for record in self:
            record.meal_count = record.get_meal_count()

    @api.multi
    def generate_meals(self):
        """Generate a collection of meals based on the other attributes.

        This should be fired on button click, perhaps in wizard

        Ensure one to prevent confusion in finding default start date
        """
        self.ensure_one()
        Meal = self.env['meal.meal']
        vals_list = []
        date_series = self.get_date_series(self.start_date, self.end_date)
        # TODO: This will need additional params for meal_time_ids, meal_location_ids
        meal_data = Meal.generate_meal_data(self.id, self.meal_location_ids.ids, self.meal_time_ids.ids, date_series)
        meals = Meal.create(meal_data)
        return True

    @api.model
    def create(self, vals):
        """Use sequence
        """
        if vals.get('name', 'New') == 'New':
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('meal.cycle') or 'New'
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('meal.cycle') or 'New'
        rs = super(MealCycle, self).create(vals)
        return rs

    @api.multi
    def write(self, vals):
        """State changes to cycle cascade to meals
        """
        if 'state' in vals:
            self.meal_ids.write({'state': vals['state']})
        return super(MealCycle, self).write(vals)

    # for backend button click handlers
    @api.multi
    def action_publish_cycle(self):
        return self.write({'state': 'published'})

    @api.multi
    def action_generate_meals(self):
        return self.generate_meals()

    @api.multi
    def action_view_meals(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Meals for %s' % self.name,
            'res_model': 'meal.meal',
            'domain': [('id', 'in', self.meal_ids.ids)],
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
        }


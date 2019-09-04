from collections import defaultdict
import datetime
import json

from odoo import models, fields, api, _ 
from odoo.exceptions import UserError
from odoo.tools import json_default

from .mixins import OrmExtensions

def today():
    """Utility for mocking
    """
    return datetime.date.today()

class Meal(models.Model, OrmExtensions):
    """A meal

    Note: create multi
    """
    _name = 'meal.meal'
    _description = 'A single meal'
    _rec_name = 'meal_time_id'

    meal_date = fields.Date(
        help='The scheduled date of the meal',
    )

    meal_label = fields.Char(
        string='Meal Day Label',
        compute='_compute_meal_label',
    )

    active = fields.Boolean(
        default=True,
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
    ], default='draft',
        help='Published = visible to external clients',
    )

    meal_cycle_id = fields.Many2one(
        comodel_name='meal.cycle',
        ondelete='cascade',
    )

    meal_location_id = fields.Many2one(
        comodel_name='meal.location',
        ondelete='restrict',
    )

    meal_time_id = fields.Many2one(
        comodel_name='meal.time',
        ondelete='restrict',
    )

    meal_day_id = fields.Many2one(
        comodel_name='meal.day',
    )

    @api.multi
    @api.depends('meal_date')
    def _compute_meal_day_id(self):
        for record in self:
            record.meal_day_id = record.get_or_create_meal_day(self.meal_date)

    @api.multi
    def _compute_meal_label(self):
        # TODO: use special labels
        for record in self:
            record.meal_label = record.get_meal_label(record.meal_date, False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'meal_date' in vals:
                vals['meal_day_id'] = self.get_or_create_meal_day(vals['meal_date']).id
        return super(Meal, self).create(vals_list)

    @api.multi
    def write(self, vals):
        if 'meal_date' in vals:
            vals['meal_day_id'] = self.get_or_create_meal_day(vals['meal_date']).id
        rs = super(Meal, self).write(vals)
        if 'meal_cycle_id' in vals:
            self.mapped('meal_day_id').write({'meal_cycle_id': vals['meal_cycle_id']})
        return rs

    @api.multi
    def unlink(self):
        for record in self:
            if record.state == 'published':
                raise UserError('Deleting published Meal Cycles is not allowed')
        return super(Meal, self).unlink()

    def get_or_create_meal_day(self, meal_date):
        MealDay = self.env['meal.day']
        md = MealDay.search([('meal_date', '=', meal_date)])
        if md:
            return md
        else:
            vals = {
                'meal_date': meal_date,
            }
            return MealDay.create(vals)

    def generate_meal_data(self, meal_cycle_id, meal_location_ids, meal_time_ids, date_series):
        data = []
        for dat in date_series:
            vals = {
                'meal_cycle_id': meal_cycle_id,
                'meal_date': dat,
            }
            for loc in meal_location_ids:
                vals.update({'meal_location_id': loc})
                for t in meal_time_ids:
                    vals.update({'meal_time_id': t})
                    # have to create a new dict, else reference semantics apply
                    data.append(dict(vals))
        return data

    def get_last_scheduled_meal_date(self):
        """Search the meal history for the last meal
        """
        last_meal = self.search([], limit=1, order='meal_date desc')
        if last_meal:
            return last_meal.meal_date
        else:
            return False

    def get_meal_weekday(self, meal_date):
        return meal_date.strftime('%a')

    def get_meal_label(self, meal_date, special_label):
        """Designed to allow injecting a special label instead of normal weekday
        """
        if special_label:
            return special_label
        else:
            return self.get_meal_weekday(meal_date)

    @api.multi
    def group_by_week(self):
        """Sort the meals and return a dict, tagging the group by the first date.
        Loosely named group_by_week, but the starting weekday can be whatever.

        Returns:
            A dict of lists of meal ids
        """
        sorted_meals = self.sorted(key='meal_date')
        if not sorted_meals:
            return {}

        wk = sorted_meals[0].meal_date
        date0 = sorted_meals[0].meal_date
        delta0 = 0
        out = defaultdict(list)
        for meal in sorted_meals:
            delta = (meal.meal_date - date0).days
            if delta > 0 and delta % 7 == 0 and meal.meal_date not in out.keys():
                wk = meal.meal_date
            out[wk].append(meal.id)
        return out

    def _get_meal_data(self, delta, time_key, location_key, fields=[]):
        """ API workhorse. Use date delta and meal_time key to get the meal data
        Meant to be overridden in project.

        Args:
            delta (int): Number of days relative to today to query
            time_key (str): The key for the meal time to query
            location_key (str): The key for the meal location to query

        Returns:
            A list of dicts for json conversion
        """
        # convert delta to meal date
        meal_date = today() + datetime.timedelta(days=delta)
        domain = [
            ('state', '=', 'published'),
            ('meal_date', '=', meal_date),
            ('meal_location_id.key', '=', location_key),
            ('meal_time_id.key', '=', time_key),
        ]
        return self.env['meal.meal'].search_read(domain, fields)

    def get_meal_data(self, delta, time_key, location_key, fields=[]):
        data = self._get_meal_data(delta, time_key, location_key, fields)
        return json.dumps(data, default=json_default)


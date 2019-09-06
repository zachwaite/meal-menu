from odoo import models, fields, api, _ 


class MealCycle(models.Model):
    _inherit = 'meal.cycle'

    @api.multi
    def print_meal_cycle(self):
        return self.env.ref('meal_menu_reports.action_report_meal_cycle')\
                .with_context({'discard_logo_check': True}).report_action(self)


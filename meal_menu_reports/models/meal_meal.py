from odoo import models, fields, api, _ 


class Meal(models.Model):
    _inherit = 'meal.meal'

    report_image_url = fields.Char(
        compute='_compute_report_image_url',
    )

    @api.multi
    def _compute_report_image_url(self):
        for record in self:
            record.report_image_url = record.get_report_image_url()

    def get_report_image_url(self):
        """Get the report background image
        """
        Attachment = self.env['ir.attachment'].sudo()
        domain = [
            ('res_model', '=', 'meal.time'),
            ('res_field', '=', 'meal_report_image'),
            ('res_id', '=', self.meal_time_id.id),
        ]
        att = Attachment.search(domain)
        return '/web/image/{0}'.format(att.id)

    @api.multi
    def print_meal_menu(self):
        return self.env.ref('meal_menu_reports.action_report_meal_menu')\
                .with_context({'discard_logo_check': True}).report_action(self)


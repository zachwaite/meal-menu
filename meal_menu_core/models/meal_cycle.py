from odoo import models, fields, api, _ 


class MealCycle(models.Model):
    _name = 'meal.cycle'
    _description = 'Collection of meals'

    start_date = fields.Date(
       required=True,
       help='Start date for the cycle',
       default=lambda self: self.get_default_cycle_start_date(),
    )

    cycle_duration = fields.Integer(
        required=True,
        help='The number of days in this meal cycle',
        default=21,
    )

    end_date = fields.Date(
        required=True,
        help='End date for the cycle',
        compute='_compute_end_date',
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

    # meal_ids
    # meal_location_ids
    # meal_time_ids

    @api.multi
    def _compute_end_date(self):
        for record in self:
            record.end_date = record.get_end_date(record.start_date, record.cycle_duration)

    def get_end_date(self, start_date, cycle_duration):
        """Add start_date and cycle_duration to get the end_date

        Args:
            start_date (datetime.date)
            cycle_duration (int)

        Returns:
            A datetime.date
        """
        pass

    def get_default_cycle_start_date(self):
        """Use the history to get the next upcoming cycle start
        """
        pass

    @api.multi
    def generate_meals(self):
        """Generate a collection of meals based on the other attributes.

        This should be fired on button click, perhaps in wizard

        Ensure one to prevent confusion in finding default start date
        """
        self.ensure_one()
        pass

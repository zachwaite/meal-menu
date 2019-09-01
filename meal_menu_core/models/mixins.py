import datetime
import pytz
from odoo import models, fields, api, _ 
from odoo import tools



def unfloat_time(float_time):
    """Utility to convert float time to a triple of (h, m, s)

    Always using 0 for s
    """
    h, m = divmod(float(float_time) * 60, 60)
    return (h, m, 0)

def unfloat_time_formatted(float_time):
    """Utility to format float time as hh:mm:ss"""
    return '{0:02.0f}:{1:02.0f}:00'.format(*unfloat_time(float_time)[:1])


class TimespanMixin(models.AbstractModel):
    _name = 'timespan.mixin'
    _description = 'Mixin class to add start, end time and helpers'

    start_time = fields.Float(
        help='Time the meal starts (local timezone)',
    )

    end_time = fields.Float(
        help='Time the meal ends (local timezone)',
    )

    def get_datetime_from_float_time(self, date, float_time):
        """Use the supplied date and self.*_time to construct a datetime in local time

        Args:
            date (datetime.date or datetime.datetime): The date component
            float_time (a float time): The time component

        Returns:
            A datetime.datetime in utc representing the combined datetime
        """
        y = date.year
        m = date.month
        d = date.day
        h, m, s = unfloat_time(float_time)
        return datetime.datetime(y, m, d, h, m, s)

    def get_start_datetime(self, date):
        return self.get_datetime_from_float_time(date, self.start_time)

    def get_end_datetime(self, date):
        return self.get_datetime_from_float_time(date, self.start_time)

    @api.model
    def localize(self, naive):
        """Localize a naive datetime to users timezone"""
        tz_str = self.env.user.tz
        local_tz = pytz.timezone(tz_str)
        localized = local_tz.localize(naive)
        return localized

    @api.model
    def convert_utc(self, dt):
        """Convert a tz aware datetime to utc"""
        return dt.astimezone(pytz.UTC)

    @api.model
    def convert_local(self, dt):
        """Convert a datetime to local tz"""
        tz_str = self.env.user.tz
        local_tz = pytz.timezone(tz_str)
        return dt.astimezone(local_tz)


class DescriptorMixin(models.AbstractModel):
    _name = 'descriptor.mixin'
    _description = 'Mixin class to add name, key, description'

    name = fields.Char(
        required=True,
        help='Display name for record. e.g. Main Cafeteria',
    )

    key = fields.Char(
        size=10,
        help='Short code uniquely identifying this record. e.g. cafeteria_1',
        required=True,
    )

    description = fields.Text(
       help='Description of the dining space. e.g. Our newly renovated dining room, with comfortable seating and friendly staff',
    )



class ImageMixin(models.AbstractModel):
    _name = 'image.mixin'
    _description = 'Mixin class to add images'

    image = fields.Binary(
        attachment=True,
        help='The image used as the avatar, limted to 1024px x 1024px',
    )

    image_small = fields.Binary(
        attachment=True,
        help='The image, resized to 64px x 64',
    )

    image_medium = fields.Binary(
        attachment=True,
        help='The image, resized to 64px x 64',
    )

    def _prepare_image_vals(self, vals):
        tools.image_resize_images(vals, sizes={'image': (1024, None)})
        return vals


class DateRangeMixin(models.AbstractModel):
    _name = 'daterange.mixin'
    _description = 'Mixin class for models with start, end and duration'

    start_date = fields.Date(
       required=True,
       help='Start date for the cycle',
    )

    duration = fields.Integer(
        required=True,
        help='The number of days in this meal cycle',
        default=21,
    )

    end_date = fields.Date(
        required=True,
        help='End date for the cycle',
        compute='_compute_end_date',
    )

    @api.multi
    def _compute_end_date(self):
        for record in self:
            record.end_date = record.get_end_date(record.start_date, record.duration)

    def get_end_date(self, start_date, cycle_duration):
        """Add start_date and cycle_duration, minus to get the end_date
        (Include start, exclude end)

        Args:
            start_date (datetime.date)
            cycle_duration (int)

        Returns:
            A datetime.date
        """
        return start_date + datetime.timedelta(days=cycle_duration - 1)

    def get_date_series(self, start_date, end_date):
        """Produce a list of dates

        Args:
            start_date (datetime.Date)
            end_date (datetime.Date)

        Returns:
            A list of datetime.dates
        """
        if not start_date or not end_date:
            raise ValidationError('start and end required')

        if end_date < start_date:
            raise ValidationError('end date should be after start')

        rng = (end_date - start_date).days + 1
        return [start_date + datetime.timedelta(days=x) for x in range(rng)]


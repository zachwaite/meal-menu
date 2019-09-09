import datetime
import pytz
import mimetypes
import re
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
        help='Time the meal starts (local timezone). Uses 24hr clock.',
    )

    end_time = fields.Float(
        help='Time the meal ends (local timezone). Uses 24hr clock.',
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
        help='Short code uniquely identifying this record. e.g. cafeteria_1',
        compute='_compute_key',
        store=True,
    )

    description = fields.Text(
       help='Description of the dining space. e.g. Our newly renovated dining room, with comfortable seating and friendly staff',
    )

    sequence = fields.Integer(
        default=25
    )

    def snake_cased(self, s):
        """Return name as snake case

        Args:
            s (string)

        Returns:
            A string
        """
        _s = s.replace(' ', '_').lower()
        _s = re.sub('[^A-Za-z0-9_]', '', _s)
        _s = re.sub('[_]{1,}', '_', _s)
        return _s

    @api.multi
    @api.depends('name')
    def _compute_key(self):
        for record in self:
            record.key = record.snake_cased(record.name)


class ImageMixin(models.AbstractModel):
    _name = 'image.mixin'
    _description = 'Mixin class to add images'

    IMAGE_FIELDS = {'image', 'image_small', 'image_medium'}

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
        help='The image, resized to 128px x 128px',
    )

    def _prepare_image_vals(self, vals):
        tools.image_resize_images(vals, sizes={'image': (1024, None)})
        return vals

    @api.multi
    def _postprocess_images(self):
        """Add a dummy datas_fname to the attachment record to be used in url
        """
        for record in self:
            known_extensions = {
                'image/jpg': '.jpg',
                'image/jpeg': '.jpg',
                'image/png': '.png',
            }
            image_fields = record.IMAGE_FIELDS
            for fld in image_fields:
                if record[fld]:
                    # uses sudo()
                    att = record.get_image_attachment(fld)

                    # create a bogus filename from mimetype and fieldname
                    ext = known_extensions.get(att.mimetype) or mimetypes.guess_extension(att.mimetype)
                    att.write({'datas_fname': fld + ext})
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.update(self._prepare_image_vals(vals))
        rs = super(ImageMixin, self).create(vals_list)
        rs._postprocess_images()
        return rs

    @api.multi
    def write(self, vals):
        if self.IMAGE_FIELDS.intersection(set(vals.keys())):
            self._prepare_image_vals(vals)
            rs = super(ImageMixin, self).write(vals)
            self._postprocess_images()
        else:
            rs = super(ImageMixin, self).write(vals)
        return True

    def get_image_attachment(self, field_name='image'):
        """Query the attachments table for the record, thus to construct a url

        Args:
            field_name (str): A string of an image field name

        Returns:
            A recordset of type ir.attachment()
        """
        allowed_field_names=self.IMAGE_FIELDS
        if not field_name in allowed_field_names:
            raise ValidationError('field_name must be in %s' % allowed_field_names)
        Attachment = self.env['ir.attachment'].sudo()
        domain = [
            ('res_model', '=', self._name),
            ('res_field', '=', field_name),
            ('res_id', '=', self.id)
        ]
        return Attachment.search(domain)

    def get_image_attachment_url(self, field_name='image', resize=()):
        """Get a web url, optionally resizing

        Args:
            field_name (string):
            resize (tuple): A tuple of (x, y) pixels to resize to, limited to 500x500

        Returns:
            A url
        """
        att = self.get_image_attachment(field_name)
        if resize:
            return '/web/image/{id}/{x}x{y}/{name}'.format(**{
                'id': str(att.id),
                'x': resize[0],
                'y': resize[1],
                'name': att.datas_fname,
            })
        else:
            return '/web/image/{id}/{name}'.format(**{
                'id': str(att.id),
                'name': att.datas_fname,
            })


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
    @api.depends('start_date', 'duration')
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


class OrmExtensions():
    """Mixin to patch all applied models
    """

    @api.model
    def get_all(self, active_test=None):
        """Get all records in model

        Args:
            active_test (bool): The domain value for active. If `None`, omit active clause, else use the bool

        Returns:
            A recordset of all records in model
        """
        domain = []
        if active_test is not None:
            if active_test:
                domain.append(('active', '=', True))
            else:
                domain.append(('active', 'in', [True, False]))
        return self.search(domain)


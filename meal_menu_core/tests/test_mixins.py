import datetime
import pytz
from .common import TestMealMenuBase
from odoo.addons.meal_menu_core.models.mixins import unfloat_time


class TestImageMixin(TestMealMenuBase):
    """Test methods on mixins
    """

    def test_test(self):
        assert True

    def test_prepare_image_vals(self):
        img = self.env.ref('base.res_partner_address_1').image
        vals = {'image': img}

        ImageMixin = self.env['image.mixin']
        ImageMixin._prepare_image_vals(vals)

        self.assertTrue(vals.get('image', False))
        self.assertTrue(vals.get('image_small', False))
        self.assertTrue(vals.get('image_medium', False))


class TestTimspanMixin(TestMealMenuBase):
    """
    """
    def test_unfloat_time(self):
        data = [
            (0.25, (0, 15, 0)),
            (1, (1, 0, 0)),
            (12.25, (12, 15, 0)),
            (13.5, (13, 30, 0)),
            (23.75, (23, 45, 0)),
        ]
        for t in data:
            out = unfloat_time(t[0])
            self.assertEqual(out, t[1])

    def test_localize_preserve(self):
        """Ensure the date and times aren't altered during localization.
        """
        Timespan = self.env['timespan.mixin']
        data = [
            datetime.datetime(2019, 2, 2, 0, 1, 2, 3),
            datetime.datetime(2020, 2, 5, 23, 1, 2, 3),
            datetime.datetime(2006, 2, 5, 23, 1, 2, 3),
        ]
        user_tz = pytz.timezone(self.env.user.tz)
        for dt in data:
            out = Timespan.localize(dt)
            self.assertEqual(dt.year, out.year)
            self.assertEqual(dt.month, out.month)
            self.assertEqual(dt.day, out.day)
            self.assertEqual(dt.hour, out.hour)
            self.assertEqual(dt.minute, out.minute)
            self.assertEqual(dt.second, out.second)

            # tzinfo differs based on date due to daylight savings, so relocalize the date here to test
            self.assertEqual(out.tzinfo, user_tz.localize(dt).tzinfo)

    def test_convert_utc(self):
        Timespan = self.env['timespan.mixin']
        # user tz is brussels (UTC +2h on August 30)
        data = [
            (datetime.datetime(2019, 8, 30, 7, 0, 7, 52), datetime.datetime(2019, 8, 30, 9, 0, 7, 52))
        ]
        for dt in data:
            dt_utc = pytz.UTC.localize(dt[0])
            dt_local = Timespan.localize(dt[1])
            self.assertEqual(dt_utc, Timespan.convert_utc(dt_local))

    def test_convert_local(self):
        Timespan = self.env['timespan.mixin']
        # user tz is brussels (UTC +2h on August 30)
        data = [
            (datetime.datetime(2019, 8, 30, 7, 0, 7, 52), datetime.datetime(2019, 8, 30, 9, 0, 7, 52))
        ]
        for dt in data:
            dt_utc = pytz.UTC.localize(dt[0])
            dt_local = Timespan.localize(dt[1])
            self.assertEqual(dt_local, Timespan.convert_local(dt_utc))

class TestDateRangeMixin(TestMealMenuBase):
    def setUp(self):
        super(TestDateRangeMixin, self).setUp()

        # data
        self.mocked_date = datetime.date(2019, 11, 1)


    def test_get_end_date(self):
        """
        """
        data = [
            (21, datetime.date(2019, 11, 21)),
            (10, datetime.date(2019, 11, 10)),
        ]

        DateRangeMixin = self.env['daterange.mixin']
        for dur in data:
            end_date = DateRangeMixin.get_end_date(self.mocked_date, dur[0])
            self.assertEqual(end_date, dur[1])

    def test_get_date_series(self):
        data = [
            {
                'start_date': datetime.date(2019, 11, 1),
                'end_date': datetime.date(2019, 11, 10),
                'expect': [
                    datetime.date(2019, 11, 1),
                    datetime.date(2019, 11, 2),
                    datetime.date(2019, 11, 3),
                    datetime.date(2019, 11, 4),
                    datetime.date(2019, 11, 5),
                    datetime.date(2019, 11, 6),
                    datetime.date(2019, 11, 7),
                    datetime.date(2019, 11, 8),
                    datetime.date(2019, 11, 9),
                    datetime.date(2019, 11, 10),
                ]
            },
            {
                'start_date': datetime.date(2019, 11, 30),
                'end_date': datetime.date(2019, 12, 5),
                'expect': [
                    datetime.date(2019, 11, 30),
                    datetime.date(2019, 12, 1),
                    datetime.date(2019, 12, 2),
                    datetime.date(2019, 12, 3),
                    datetime.date(2019, 12, 4),
                    datetime.date(2019, 12, 5),
                ]
            }
        ]
        DateRangeMixin = self.env['daterange.mixin']
        for case in data:
            rs = DateRangeMixin.get_date_series(case['start_date'], case['end_date'])
            self.assertListEqual(rs, case['expect'])

class TestModelExtended(TestMealMenuBase):
    def test_get_all(self):
        MealCycle = self.env['meal.cycle']
        cycle = self.make_cycle()

        # test 1: None
        expected = MealCycle.search([])
        rs = MealCycle.get_all()
        self.assertEqual(rs, expected)
        self.assertIn(cycle.id, rs.mapped('id'))

        # deactivate cycle
        cycle.write({'active': False})

        # test 2: active True
        expected = MealCycle.search([])
        rs = MealCycle.get_all(active_test=True)
        self.assertEqual(rs, expected)
        self.assertNotIn(cycle.id, rs.mapped('id'))

        # test 3: active False
        expected = MealCycle.search([('active', 'in', [True, False])])
        rs = MealCycle.get_all(active_test=False)
        self.assertEqual(rs, expected)
        self.assertNotIn(cycle.id, rs.mapped('id'))



from .common import TestMealMenuBase


class TestMealLocation(TestMealMenuBase):
    """ Location related tests
    """

    def test_required_fields(self):
        """Check if the required flag is set. No need to test if it works,
        odoo does that.
        """
        REQUIRED = ['name',]

        Fields = self.env['ir.model.fields']
        MODEL = 'meal.location'

        for fld in REQUIRED:
            frecord = Fields.search([('model', '=', MODEL), ('name', '=', fld)])
            self.assertTrue(frecord.required)

    # tests for image.mixin
    def test_has_images(self):
        vals = self.location_1_vals
        self.location_1 = self.env['meal.location'].create(vals)

        self.assertTrue(self.location_1.image)
        self.assertTrue(self.location_1.image_small)
        self.assertTrue(self.location_1.image_medium)

    def test_get_image_attachment(self):
        location = self.env['meal.location'].create(self.location_1_vals)
        for fld in ['image', 'image_small', 'image_medium']:
            att = location.get_image_attachment(fld)
            self.assertTrue(len(att) > 0)

    def test_postprocess_images(self):
        # image is a jpg
        location = self.env['meal.location'].create(self.location_1_vals)
        location._postprocess_images()
        for fld in ['image', 'image_small', 'image_medium']:
            att = location.get_image_attachment(fld)
            self.assertEqual(att.datas_fname, fld + '.jpg')

    def test_create_postprocesses(self):
        location = self.env['meal.location'].create(self.location_1_vals)
        for fld in ['image', 'image_small', 'image_medium']:
            att = location.get_image_attachment(fld)
            self.assertEqual(att.datas_fname, fld + '.jpg')

    def test_write_postprocesses(self):
        location = self.env['meal.location'].create(self.location_1_vals)
        location.write(self.location_2_vals)
        for fld in location.IMAGE_FIELDS:
            att = location.get_image_attachment(fld)
            self.assertEqual(att.datas_fname, fld + '.jpg')

    def test_get_image_attachment_url(self):
        location = self.env['meal.location'].create(self.location_1_vals)

        # test 1
        att = location.get_image_attachment('image')
        url = location.get_image_attachment_url('image')
        self.assertEqual(url, '/web/image/%s/%s' % (att.id, att.datas_fname))

        # test 2
        att = location.get_image_attachment('image_small')
        url = location.get_image_attachment_url('image_small', resize=(200, 200))
        self.assertEqual(url, '/web/image/%s/200x200/%s' % (att.id, att.datas_fname))

    # tests for descriptor.mixin
    def test_key(self):
        # test with default key
        location = self.env['meal.location'].create({
            'name': 'Breakfast',
        })
        self.assertEqual(location.key, 'breakfast')

        # test with long default key
        location = self.env['meal.location'].create({
            'name': 'Early Morning #$ Breakfast',
        })
        self.assertEqual(location.key, 'early_morning_breakfast')



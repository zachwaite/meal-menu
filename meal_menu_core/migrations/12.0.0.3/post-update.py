def migrate(cr, version):
    cr.execute('ALTER TABLE meal_item DROP COLUMN name;')
    cr.execute('ALTER TABLE meal_item DROP COLUMN key;')
    cr.execute('ALTER TABLE meal_item DROP COLUMN description;')
    cr.execute('ALTER TABLE meal_item DROP COLUMN sequence;')

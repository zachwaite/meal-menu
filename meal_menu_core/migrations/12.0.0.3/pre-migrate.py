def migrate(cr, version):
    print('premigratiing ================================')
    sql = "SELECT name FROM meal_item;";
    cr.execute(sql)
    for name in cr.fetchall():
        print(name)

{
    'name': 'Meal Menu Backend Views',
    'summary': """ """,
    'category': 'Uncategorized',
    'version': '11.0.0.1',

    'author': 'Waite Perspectives, LLC - Zach Waite',

    'depends': [
            'meal_menu_core',
    ],

    'data': [
        'views/meal_location.xml',
        'views/meal_time.xml',
        'views/meal_item.xml',
        'views/meal_item_category.xml',
        'views/meal_meal.xml',
        'views/meal_cycle.xml',
        'views/menu_items.xml',
    ],

    'demo': [],

    'qweb': [],

    'images': [],
    'post_load': None,
    'pre_init_hook': None,
    'post_init_hook': None,
    'uninstall_hook': None,

    'application': False,
    'auto_install': False,
    'installable': True,
    # 'external_dependencies': {'python': [], 'bin': []},
    # 'support': 'zach@waiteperspectives.com',
    # 'website': 'www.waiteperspectives.com',

    # 'license': 'LGPL-3',
    # 'price': 999.00,
    # 'currency': 'USD',
}

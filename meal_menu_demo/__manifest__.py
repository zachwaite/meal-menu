{
    'name': 'Meal Management Demo',
    'summary': """ """,
    'category': 'Uncategorized',
    'version': '12.0.0.1',

    'author': 'Waite Perspectives, LLC - Zach Waite',

    'depends': [
            'meal_menu_core',
            'meal_menu_views',
    ],

    'data': [
        'data/categories.xml',
        'data/items.xml',
        'data/locations.xml',
        'data/times.xml',
        'views/meal_meal.xml',
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

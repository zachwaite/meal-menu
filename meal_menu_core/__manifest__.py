{
    'name': 'Meal Menu Core',
    'summary': """Models, methods and utils for meal plan management""",
    'category': 'Uncategorized',
    'version': '12.0.0.2',

    'author': 'Waite Perspectives, LLC - Zach Waite',

    'depends': [
        'base',
        'product',
    ],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/sequences.xml',
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

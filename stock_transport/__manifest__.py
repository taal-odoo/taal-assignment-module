{
    'name': "Dispatch Management System",
    'version': '1.0',
    'depends': ['base', 'stock_picking_batch', 'fleet'],
    'author': "Alex Tamboli",
    'description': """
        Transport Management System
    """,
    'data': [
        'security/ir.model.access.csv',

        # 'views/fleet_vehicle_model_views.xml',
        'views/fleet_vehicle_category_views.xml',
        'views/stock_picking_batch_views.xml',
    ],
    "demo": [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    "license": "LGPL-3",
}

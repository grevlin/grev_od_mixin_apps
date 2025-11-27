# -*- coding: utf-8 -*-

{
    'name': 'JSON Widget',
    'version': '19.0.1.0.1',
    'summary': """Interactive JSON Field Editor Widget for Odoo""",
    'description': """
        This module provides a user-friendly widget for editing JSON data fields in Odoo, 
        allowing easy management of key-value pairs through an intuitive interface without.""",
    'author': "Grevlin Global Corp, Tharcisse Mukundayi",
    'maintainer': 'mukundayi@gmail.com',
    'website': "https://github.com/grevlin/grev_od_mixin_apps",
    'depends': ['web'],
    'category':"hidden",
    'assets': {
        'web.assets_backend': [
            "grev_od_json_widget/static/src/**/*"
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': "LGPL-3",
    'installable': True,
    'auto_install': False,
}

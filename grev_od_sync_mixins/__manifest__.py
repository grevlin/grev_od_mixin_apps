{
    'name': 'Sync Mixins',
    'version': '19.0.1.1.1',
    'description':  """
Sync Mixins
============

A collection of reusable synchronization mixins for Odoo connector modules.

This module provides:
- Synchronization state tracking
- External ID mapping helpers
- Pull/Push synchronization logic helpers
- Generic synchronization error recovery logic
- Helper service and methods for remote API integrations

It is designed to be used as a foundation for Odoo ↔ External System connectors.
    """,
    'summary': 'Reusable synchronization mixins for Odoo connectors and third-party integrations.',
    'author': 'Grevlin Global Corp,Tharcisse Mukundayi',
    'website': 'https://grevlin.com',
    'maintainer': 'mukundayi@gmail.com',
    'license': 'LGPL-3',
    'category': 'Tools/hidden',
    'depends': [
        'base'
    ],
    'auto_install': False,
    'application': False,
}
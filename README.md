# Sync Mixins

Reusable synchronization mixins for Odoo connectors and external API integrations.

This module provides a clean and extensible foundation for building Odoo ↔ External System connectors.  
It contains shared mixins that offer consistent synchronization logic across multiple integration modules.

---

## 🚀 Features

- Synchronization state tracking
- External ID mapping helpers
- Push/Pull synchronization utilities
- Retry and error recovery helpers
- Timestamp and status fields included out-of-the-box
- Can be inherited by any Odoo model
- Lightweight and connector-agnostic

---

## 📦 Typical Use Cases

- Building custom Odoo connectors  
- Integrating Odoo with REST/SOAP/GraphQL APIs  
- Synchronizing products, partners, orders, inventory, etc.  
- Multi-connector setups sharing common sync logic  

---

## 🧱 Technical Mixins Included

- `ExternalIDMixin` – map Odoo records to remote IDs
- `SyncStateMixin` – track sync timestamps, state, and logs
- `PullMixin` – logic for receiving data from external systems
- `PushMixin` – logic for exporting Odoo data remotely
- `SyncErrorMixin` – retry, failure isolation, and recovery helpers

Each mixin can be inherited individually or combined to form a complete connector architecture.

---

## 🔧 Installation

1. Copy the module into your Odoo `addons` folder.
2. Update the apps list.
3. Install the module.
4. Extend the mixins in your custom models.

```python
from odoo import models
from odoo.addons.grev_od_sync_mixins.mixins import ExternalIDMixin, PushMixin

class ProductTemplate(models.Model):
    _inherit = ["product.template", "api.sync.mixin", "push.mixin"]

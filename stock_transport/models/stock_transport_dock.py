from odoo import api, fields, models

class StockTransportDock(models.Model):
    _name = "stock.transport.dock"

    name = fields.Char(string="Dock")

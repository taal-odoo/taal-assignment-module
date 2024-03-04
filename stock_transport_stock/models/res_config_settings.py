from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_stock_transport = fields.Boolean("Dispatch Management System", implied_group='stock.group_stock_sign_delivery')

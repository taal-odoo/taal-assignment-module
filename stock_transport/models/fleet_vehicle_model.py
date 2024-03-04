from odoo import api, fields, models

class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle.model"

    category = fields.Many2one("fleet.vehicle.model.category",string="Category")

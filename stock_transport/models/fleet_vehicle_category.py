from odoo import api, fields, models

class FleetVehicleCategory(models.Model):
    _inherit = "fleet.vehicle.model.category"

    max_weight = fields.Integer(string="Max Weight")
    max_volume = fields.Integer(string="Max Volume")

    @api.depends('max_weight', 'max_volume')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.name} ({record.max_weight} kg, {record.max_volume} m3)"

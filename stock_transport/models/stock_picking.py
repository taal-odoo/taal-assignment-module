from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    weight = fields.Float(compute="_compute_weight", store=True)
    volume = fields.Float(compute="_compute_volume", store=True)

    @api.depends('move_ids.quantity', 'move_ids.product_id.weight')
    def _compute_weight(self):
        for picking in self:
            temp = 0
            for move in self.move_ids:
                temp += move.product_id.weight * move.quantity
            picking.weight = temp
    
    @api.depends('move_ids.quantity', 'move_ids.product_id.volume')
    def _compute_volume(self):
        for picking in self:
            temp = 0
            for move in self.move_ids:
                temp += move.product_id.volume * move.quantity
            picking.volume = temp

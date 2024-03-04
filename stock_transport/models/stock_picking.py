from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    test = fields.Char(string="Test field")
    weight = fields.Float(compute="_compute_weight")
    volume = fields.Float(compute="_compute_volume")

    def _compute_weight(self):
        for picking in self:
            move_ids = self.move_ids
            temp = 0
            for move in self.move_ids:
                temp += move.product_id.weight * move.quantity
            picking.weight = temp
    
    def _compute_volume(self):
        for picking in self:
            move_ids = self.move_ids
            temp = 0
            for move in self.move_ids:
                temp += move.product_id.volume * move.quantity
            picking.volume = temp

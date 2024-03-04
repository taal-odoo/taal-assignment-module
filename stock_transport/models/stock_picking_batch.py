from odoo import api, fields, models

class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    dock_id = fields.Many2one("stock.transport.dock", string="Dock")
    vehicle_id = fields.Many2one("fleet.vehicle.model", string="Vehicle")
    vehicle_category_id = fields.Many2one("fleet.vehicle.model.category", string="Vehicle Category")
    weight = fields.Float(compute = "_compute_weight", store=True)
    volume = fields.Float(compute = "_compute_volume", store=True)
    weight_ratio = fields.Float(compute="_compute_weight_ratio")
    volume_ratio = fields.Float(compute="_compute_volume_ratio")
    move_ids_count = fields.Integer(compute="_compute_move_ids_count", string="Line Count", store=True)
    picking_ids_count = fields.Integer(compute="_compute_picking_ids_count", string="Transfer Count", store=True)

    @api.depends('move_ids')
    def _compute_move_ids_count(self):
        for record in self:
            record.move_ids_count = len(record.move_ids)

    @api.depends('picking_ids')
    def _compute_picking_ids_count(self):
        for record in self:
            record.picking_ids_count = len(record.picking_ids)

    @api.depends('vehicle_category_id')
    def _compute_weight(self):
        for record in self:
            total_weight = 0
            for picking in record.picking_ids:
                total_weight += picking.weight
            record.weight = total_weight

    @api.depends('vehicle_category_id')
    def _compute_volume(self):
        for record in self:
            total_volume = 0
            for picking in record.picking_ids:
                total_volume += picking.volume
            record.volume = total_volume

    @api.depends('vehicle_category_id')
    def _compute_weight_ratio(self):
        for record in self:
            if not record.vehicle_category_id or record.vehicle_category_id.max_weight == 0:
                record.weight_ratio = 0
                return True
            max_weight = record.vehicle_category_id.max_weight
            total_weight = 0
            for picking in record.picking_ids:
                total_weight += picking.weight 
            record.weight_ratio = ( total_weight / max_weight ) * 100
        
    
    @api.depends('vehicle_category_id')
    def _compute_volume_ratio(self):
        for record in self:
            if not record.vehicle_category_id or record.vehicle_category_id.max_volume == 0:
                record.volume_ratio = 0
                return True
            max_volume = record.vehicle_category_id.max_volume
            total_volume = 0
            for picking in record.picking_ids:
                total_volume += picking.volume
            record.volume_ratio = ( total_volume / max_volume ) * 100

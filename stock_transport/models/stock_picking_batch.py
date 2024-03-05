from odoo import api, fields, models
from odoo.exceptions import UserError

from dateutil.relativedelta import relativedelta


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    dock_id = fields.Many2one("stock.transport.dock", string="Dock")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle")
    vehicle_category_id = fields.Many2one("fleet.vehicle.model.category", string="Vehicle Category")
    weight = fields.Float(compute = "_compute_weight", digits=(16, 2), store=True)
    volume = fields.Float(compute = "_compute_volume", digits=(16, 2), store=True)
    weight_ratio = fields.Float(compute="_compute_weight_ratio")
    volume_ratio = fields.Float(compute="_compute_volume_ratio")
    move_ids_count = fields.Integer(compute="_compute_move_ids_count", string="Line Count", store=True)
    picking_ids_count = fields.Integer(compute="_compute_picking_ids_count", string="Transfer Count", store=True)
    driver_id = fields.Many2one("res.partner", compute="_compute_driver_id", string="Driver", store=True)

    @api.depends('weight', 'volume')
    def _compute_display_name(self):
        for record in self:
            if record.weight and record.volume:
                record.display_name = f"{record.name}: {record.weight}Kg, {record.volume}m\u00b3 Driver: {record.driver_id.name}"
            else:
                record.display_name = record.name

    @api.depends('vehicle_id')
    def _compute_driver_id(self):
        for record in self:
            if record.vehicle_id and record.vehicle_id.driver_id:
                record.driver_id = record.vehicle_id.driver_id.id
            else:
                record.driver_id = False

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
            ratio = ( total_weight / max_weight ) * 100
            if ratio > 100:
                raise UserError("Weight exceeds max weight of vehicle. Kindly change the vehicle or reduce quantity in batch.")
            record.weight_ratio = ratio
    
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
            ratio = ( total_volume / max_volume ) * 100
            if ratio > 100:
                raise UserError("Volume exceeds max volume of vehicle. Kindly change the vehicle or reduce quantity in batch.")
            record.volume_ratio = ratio

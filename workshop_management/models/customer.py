from odoo import api, fields, models

class Customer(models.Model):
    _name = "workshop.customer"
    _inherits = {'res.partner': 'partner_id'}
    _description = "Workshop Customer"

    partner_id = fields.Many2one('res.partner',string="Related Partner", required=True, ondelete="cascade")
    device_ids = fields.One2many("workshop.device","customer_id",string="Device")
    ticket_ids = fields.One2many("workshop.ticket","customer_id",string="Tickets")

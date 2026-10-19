from odoo import fields, models

class Device(models.Model):
    _name = 'workshop.device'
    _description = 'Workshop Device'

    name = fields.Char(string="Device Name", required=True)
    description = fields.Char(string="Device Description")
    serial_number = fields.Char(string="Serial Number")
    customer_id = fields.Many2one(
        'workshop.customer',
        string='Owner',
        ondelete='cascade',
        required=True,
    )
    ticket_ids = fields.One2many('workshop.ticket', 'device_id', string="Tickets")
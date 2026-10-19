from odoo import api, fields, models
from odoo.exceptions import UserError

class Ticket(models.Model):
    _name = 'workshop.ticket'
    _description = 'Workshop Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # عشان الـ chatter
    _order = 'id desc'

    name = fields.Char(string="Reference", default="New", copy=False, readonly=True)
    description = fields.Text(string="Description")

    customer_id = fields.Many2one('workshop.customer', string='Customer', required=True)

    device_id = fields.Many2one('workshop.device', string='Device', required=True)

    technician_id = fields.Many2one('res.users', string='Technician')

    state = fields.Selection([
        ('new', 'New'),
        ('inspection', 'In Inspection'),
        ('waiting_part', 'Waiting for Part'),
        ('repaired', 'Repaired'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='new', tracking=True, required=True)

    line_ids = fields.One2many('workshop.ticket.line', 'ticket_id', string='Lines')

    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('workshop.ticket') or 'New'
        return super().create(vals_list)

    def action_start_inspection(self):
        for rec in self:
            rec.state = 'inspection'

    def action_waiting_part(self):
        for rec in self:
            rec.state = 'waiting_part'

    def action_repaired(self):
        for rec in self:
            rec.state = 'repaired'

    def action_delivered(self):
        for rec in self:
            if rec.state != 'repaired':
                raise UserError("Can only deliver a repaired ticket.")
            rec.state = 'delivered'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

class TicketLine(models.Model):
    _name = 'workshop.ticket.line'
    _description = 'Workshop Ticket Line'

    ticket_id = fields.Many2one('workshop.ticket', string='Ticket', ondelete='cascade')

    product_id = fields.Many2one('product.product', string='Product', required=True)

    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
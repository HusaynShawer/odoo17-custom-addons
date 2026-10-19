from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    is_technician = fields.Boolean(string='Is Workshop Technician', default=False)
    ticket_ids = fields.One2many('workshop.ticket', 'technician_id', string='Assigned Tickets')
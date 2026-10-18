from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    price = fields.Float(string="Price")
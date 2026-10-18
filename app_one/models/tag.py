from odoo import fields, models

class Tag(models.Model):
    _name = 'tag'
    name = fields.Char(required=True)
    # property_ids = fields.Many2many()
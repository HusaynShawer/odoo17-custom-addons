from odoo import fields,models

class Owner(models.Model):
    _name = 'owner'
    name = fields.Char(required=True)
    email = fields.Char()
    phone = fields.Char(required=True)
    adress = fields.Char()
    property_ids = fields.One2many(comodel_name='property',inverse_name='owner_id')
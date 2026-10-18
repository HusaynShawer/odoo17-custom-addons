from docutils.core import default_usage
from geoip2 import records
from maxminddb import file

from odoo import models,fields, api
from odoo.exceptions import ValidationError
from datetime import  datetime
class Property(models.Model):
    _name = 'property'
    _description = 'Appartment Property'
    _inherit = ['mail.thread','mail.activity.mixin']
    name = fields.Char(required=True,default='husayn')
    description = fields.Text(required=False,tracking=True)
    postcode = fields.Char(required=False)
    data_availability = fields.Date(default = datetime.utcnow(),tracking=True)
    expected_price = fields.Float(required=True)
    sell_price = fields.Float(required=True,default = 5.00)
    diff = fields.Float(compute = "_compute_diff")
    bedrooms = fields.Integer(default=3)
    expected_selling_date = fields.Date(tracking=True)
    is_late = fields.Boolean()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ],default='north')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('sold', 'Sold'),
        ('closed','Closed'),
    ],default='draft')

    owner_id = fields.Many2one('owner')
    owner_adress = fields.Char(related='owner_id.adress', readonly=True, store=False)
    owner_phone = fields.Char(related='owner_id.phone', readonly=True, store=False)

    tag_ids = fields.Many2many('tag')
    line_ids = fields.One2many('property.line', 'property_id')

    _sql_constraints = [
        ('unique_name','unique(name)','Unique name is required')
    ]
    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for record in self:
            print("self bedrooms",self.bedrooms)
            if self.bedrooms <= 0:
                raise  ValidationError('Bedrooms must be greater than 0')
    def action_draft(self):
        for record in self:
            record.state = 'draft'

    def action_confirmed(self):
        for record in self:
            record.state = 'confirmed'

    def action_sold(self):
        for record in self:
            record.state = 'sold'

    def close_action(self):
        for record in self:
            record.state = 'closed'
    @api.depends('expected_price','sell_price')
    def _compute_diff(self):
        for rec in self:
            print("inside _compute_diff")
            rec.diff = rec.expected_price - rec.sell_price

    def check_expected_selling_date(self):
        records = self.search([])
        for record in records:
            if record.expected_selling_date and record.expected_selling_date < fields.date.today():
                record.is_late = True
                print(record.expected_selling_date,fields.date.today())



class PropertyLine(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area = fields.Integer()
    description = fields.Text(required=False)

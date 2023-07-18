from odoo import fields, models, api


class TestBook(models.Model):
    _name = 'test_02.book'
    _description = 'Description'

    name = fields.Char()
    condition = fields.Selection(string='Condition', required=True, default='new',
                                 selection=[('new', 'New'),
                                            ('used', 'Used')])
    description = fields.Text(string="Description")
    price = fields.Float(string='Price')
    quantity = fields.Integer(string='Quantity')
    category = fields.Char(string='Category')
    author = fields.Char(string='Author')
    quote = fields.Text(string='Quote')
    language = fields.Char(string='Language')
    collection = fields.Boolean(string='Collection')

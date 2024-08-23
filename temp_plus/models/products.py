from odoo import fields, models


class CommprogProduct(models.Model):
    _inherit = 'commprog.product'

    quantity = fields.Float(string='Quantity', required=True, readonly=True)
    description = fields.Text(string='Description')

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class CommprogProduct(models.Model):
    _name = 'commprog.product'
    _rec_name = 'product'

    product = fields.Char(string='Product', required=True)
    quantity = fields.Integer(string='Quantity', required=True, readonly=True)
    barcode = fields.Char(string='Barcode', required=True)
    in_price = fields.Float(string='In Price', required=True)
    out_price = fields.Float(string='Out Price', required=True)

    # _sql_constraints = [
    #     ('quantity', 'CHECK(quantity>=0)', 'Quantity must be positive'),
    # ]

    @api.constrains('quantity')
    def _check_quantity(self):
        for product in self:
            if product.quantity < 0:
                raise ValidationError('Quantity must be positive')

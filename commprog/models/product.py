from odoo import fields, models


class CommprogProduct(models.Model):
    _name = 'commprog.product'
    _description = 'Produktet'

    name = fields.Char(string="Product name")
    quantity = fields.Float(string='Quantity', required=True, default=0)
    purchase_price = fields.Float(string='Purchase Price', required=True, default=0)
    sale_price = fields.Float(string='Sale Price', required=True, default=0)


class CommprogCategory(models.Model):
    _name = 'commprog.category'
    _description = 'Commprog Category'

    name = fields.Char(string="Category name")

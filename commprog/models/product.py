from odoo import fields, models


class CommprogProduct(models.Model):
    _name = 'commprog.product'
    _description = 'Produktet'

    name = fields.Char(string="Product name")
    quantity = fields.Float(string='Quantity', required=True, default=0)
    purchase_price = fields.Float(string='Purchase Price', required=True, default=0)
    sale_price = fields.Float(string='Sale Price', required=True, default=0)
    category_ids = fields.Many2many(comodel_name='commprog.category', string='Categories')
    cost = fields.Float(string="Cost")

    def calc_cost(self):
        invoice_line_ids = self.env['commprog.invoice.line'].search([('product_id', '=', self.id)], order='date')
        sum = 0
        quantity = 0
        cost = 0
        for invoice_line in invoice_line_ids:
            if invoice_line.invoice_id.invoice_type == 'in':
                sum += invoice_line.total
                quantity += invoice_line.quantity
                cost = sum / quantity
            else:
                sum -= cost * invoice_line.quantity
                quantity -= invoice_line.quantity
        self.cost = cost


class CommprogCategory(models.Model):
    _name = 'commprog.category'
    _description = 'Commprog Category'

    name = fields.Char(string="Category name")

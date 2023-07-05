from odoo import fields, models


class CommprogInvoice(models.Model):
    _name = 'commprog.invoice'
    _description = 'Description'

    invoice_number = fields.Char()
    date = fields.Datetime(string='Date', required=True, default=lambda self: fields.Datetime.now())
    invoice_type = fields.Selection(string='Type', required=True,
                                    selection=[('in', 'Purchase'), ('out', 'Sale')])


class CommprogInvoiceLine(models.Model):
    _name = 'commprog.invoice.line'
    _description = 'CommprogInvoiceLine'

    quantity = fields.Float(string="Quantity", default=0, required=True)
    price = fields.Float(string="Price", default=0, required=True)

from odoo import fields, models


class CommprogInvoice(models.Model):
    _name = 'commprog.invoice'
    _description = 'Description'
    _rec_name = 'invoice_number'

    invoice_number = fields.Char()
    date = fields.Datetime(string='Date', required=True, default=lambda self: fields.Datetime.now())
    invoice_type = fields.Selection(string='Type', required=True,
                                    selection=[('in', 'Purchase'), ('out', 'Sale')])
    client_id = fields.Many2one(comodel_name='commprog.client', string='Client')
    employee_id = fields.Many2one(comodel_name='commprog.employee', string='Employee', required=True)
    state = fields.Selection(string='State', required=True, default='draft',
                             selection=[('draft', 'Draft'), ('done', 'Done'), ('paid', 'Paid')])
    invoice_line_ids = fields.One2many(comodel_name='commprog.invoice.line', inverse_name='invoice_id',
                                       string='Invoice line')

    def confirm(self):
        self.state = 'done'

    def pay(self):
        self.state = 'paid'

    def sent_to_draft(self):
        self.state = 'draft'


class CommprogInvoiceLine(models.Model):
    _name = 'commprog.invoice.line'
    _description = 'CommprogInvoiceLine'

    quantity = fields.Float(string="Quantity", default=0, required=True)
    price = fields.Float(string="Price", default=0, required=True)
    invoice_id = fields.Many2one(comodel_name='commprog.invoice', string='Invoice', required=True)
    product_id = fields.Many2one(comodel_name='commprog.product', string='Product', required=True)

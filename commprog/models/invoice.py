from odoo import fields, models, api
from odoo.exceptions import UserError


class CommprogInvoice(models.Model):
    _name = 'commprog.invoice'
    _description = 'Description'
    _rec_name = 'invoice_number'

    invoice_number = fields.Char()
    date = fields.Datetime(string='Date', required=True, default=lambda self: fields.Datetime.now())
    invoice_type = fields.Selection(string='Type', required=True,
                                    selection=[('in', 'Purchase'), ('out', 'Sale')])
    client_id = fields.Many2one(comodel_name='commprog.client', string='Client')  # FK
    employee_id = fields.Many2one(comodel_name='commprog.employee', string='Employee', required=True)
    state = fields.Selection(string='State', required=True, default='draft',
                             selection=[('draft', 'Draft'), ('done', 'Done'), ('paid', 'Paid')])
    invoice_line_ids = fields.One2many(comodel_name='commprog.invoice.line', inverse_name='invoice_id',
                                       string='Invoice line')
    # invoice_line_ids2 = fields.One2many(comodel_name='commprog.invoice.line', inverse_name='invoice_id',
    #                                    string='Invoice line 2', domain=[('quantity', '>=', 10), ('price', '>', 500)])
    total = fields.Float(string='Total', store=True, compute="_calc_total_invoice")

    @api.depends('invoice_line_ids')
    def _calc_total_invoice(self):
        for invoice in self:
            # s = 0
            # for invoice_line in invoice.invoice_line_ids:
            #     s += invoice_line.total
            # invoice.total = s
            invoice.total = sum(invoice.invoice_line_ids.mapped('total'))

    def confirm(self):
        self.state = 'done'
        if self.invoice_type == 'in':
            for invoice_line in self.invoice_line_ids:
                invoice_line.product_id.quantity += invoice_line.quantity
        else:
            for invoice_line in self.invoice_line_ids:
                if invoice_line.product_id.quantity < invoice_line.quantity:
                    raise UserError("Quantity to low!")
                invoice_line.product_id.quantity -= invoice_line.quantity
            self.client_id.points += self.total * 0.01

    def pay(self):
        self.state = 'paid'

    def sent_to_draft(self):
        self.state = 'draft'

    def unlink(self):
        for rec in self:
            if rec.state != "draft":
                raise UserError("Invoice can't be deleted!")
        return super(CommprogInvoice, self).unlink()


class CommprogInvoiceLine(models.Model):
    _name = 'commprog.invoice.line'
    _description = 'CommprogInvoiceLine'

    quantity = fields.Float(string="Quantity", default=0, required=True)
    price = fields.Float(string="Price", default=0, required=True)
    invoice_id = fields.Many2one(comodel_name='commprog.invoice', string='Invoice', required=True, ondelete="cascade")
    product_id = fields.Many2one(comodel_name='commprog.product', string='Product', required=True)
    total = fields.Float(string='Total', compute="_calc_total")
    date = fields.Datetime(related='invoice_id.date', string="date")

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.invoice_id.invoice_type == 'in':
            self.price = self.product_id.purchase_price
        else:
            self.price = self.product_id.sale_price

    @api.depends('quantity', 'price')
    def _calc_total(self):
        for invoice_line in self:
            invoice_line.total = invoice_line.quantity * invoice_line.price

    @api.model
    def create(self, values):
        res = super(CommprogInvoiceLine, self).create(values)
        if res.quantity < 0:
            raise UserError("Quantity < 0!")
        return res

    def write(self, values):

        if values['quantity'] < 0:
            raise UserError("Quantity < 0!")
        return super(CommprogInvoiceLine, self).write(values)

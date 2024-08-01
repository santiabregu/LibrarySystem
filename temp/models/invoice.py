from odoo import fields, models, api
from odoo.exceptions import UserError


class CommprogInvoice(models.Model):
    _name = 'commprog.invoice'
    _description = 'Description'
    _rec_name = 'code'

    code = fields.Char(string='Code', required=True, default='New')
    total = fields.Float(string='Total', compute='_calc_total', store=True)
    date = fields.Date(string='Date', required=True)
    in_out = fields.Boolean(string='In/Out', required=True)
    client_id = fields.Many2one(comodel_name='commprog.client', string='Client', required=True)
    points = fields.Float(string='Points', related='client_id.points', readonly=True)
    employee_id = fields.Many2one(comodel_name='commprog.employee', string='Employee', required=True)
    state = fields.Selection(string='State', selection=[('draft', 'Draft'), ('done', 'Done'), ('paid', 'Paid')],
                             default='draft')
    pay_method = fields.Selection(string='Pay Method',
                                  selection=[('cash', 'Cash'), ('card', 'Card'), ('point', 'Point')], default='cash')
    invoice_line_ids = fields.One2many(comodel_name='commprog.invoice.line', inverse_name='invoice_id',
                                       string='Invoice Line')

    def action_done(self):
        koef = 1 if self.in_out else -1
        for invoice_line in self.invoice_line_ids:
            invoice_line.product_id.quantity += koef * invoice_line.qty
        self.state = 'done'

    def action_paid(self):
        if self.pay_method != 'point':
            self.client_id.points += self.total / 100
        else:
            self.client_id.points -= self.total
        self.state = 'paid'

    @api.depends('invoice_line_ids')
    def _calc_total(self):
        for invoice in self:
            s = 0
            for invoice_line in invoice.invoice_line_ids:
                s += invoice_line.price * invoice_line.qty
            invoice.total = s
            # invoice.total = sum(invoice.invoice_line_ids.mapped('total'))

    @api.onchange('in_out')
    def onchange_invoice_type(self):
        for invoice_line in self.invoice_line_ids:
            invoice_line._onchange_product()

    @api.model
    def create(self, values):
        if values['in_out']:
            code = self.env['ir.sequence'].next_by_code('in.invoice.cp')
        else:
            code = self.env['ir.sequence'].next_by_code('out.invoice.cp')
        values['code'] = code
        res = super(CommprogInvoice, self).create(values)
        return res

    def write(self, values):
        res = super(CommprogInvoice, self).write(values)
        return res

    def unlink(self):
        for invoice in self:
            if invoice.state != 'draft':
                raise UserError('Invoice can not be deleted')
        res = super(CommprogInvoice, self).unlink()
        return res


class CommprogInvoiceLine(models.Model):
    _name = 'commprog.invoice.line'

    invoice_id = fields.Many2one(comodel_name='commprog.invoice', string='Invoice', required=True, ondelete='cascade')
    product_id = fields.Many2one(comodel_name='commprog.product', string='Product', required=True)
    qty = fields.Float(string='Qty', required=True, default=1)
    price = fields.Float(string='Price', required=True)
    total = fields.Float(string='Total', compute='_calc_total')
    date = fields.Date(string='Date', related='invoice_id.date')

    @api.onchange('product_id')
    def _onchange_product(self):
        if self.invoice_id.in_out:
            self.price = self.product_id.in_price
        else:
            self.price = self.product_id.out_price

    @api.depends('qty', 'price')
    def _calc_total(self):
        for invoice_line in self:
            invoice_line.total = invoice_line.price * invoice_line.qty

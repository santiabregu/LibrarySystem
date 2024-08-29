from odoo import fields, models, api


class CommprogEmployee(models.Model):
    _inherit = 'commprog.employee'

    invoice_ids = fields.One2many(comodel_name='commprog.invoice', inverse_name='employee_id', string='Invoices')
    total = fields.Float(string='Total', compute='_calc_total', store=True)

    @api.depends('invoice_ids')
    def _calc_total(self):
        for employee in self:
            employee.total = sum(employee.invoice_ids.mapped('total'))

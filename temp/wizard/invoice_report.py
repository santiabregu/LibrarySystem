from odoo import fields, models


class InvoiceReport(models.TransientModel):
    _name = 'invoice.report'
    _description = 'Invoice report'

    product_ids = fields.Many2many(comodel_name='commprog.product', string='Products')
    start_date = fields.Date(default=fields.Datetime.now, string='Start date', required=True)
    end_date = fields.Date(default=fields.Datetime.now, string='End date', required=True)

    def print_report(self):
        self.ensure_one()
        data = {
            "product_ids": self.product_ids.ids,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
        return self.env.ref('temp.action_report_invoice').report_action(None, data=data)

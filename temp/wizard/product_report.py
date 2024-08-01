from odoo import fields, models


class InvoiceReport(models.TransientModel):
    _name = 'product.report'
    _description = 'Invoice report'

    product_ids = fields.Many2many(comodel_name='commprog.product', string='Products')
    start_date = fields.Date(default=fields.Datetime.now, string='Start date', required=True)
    end_date = fields.Date(default=fields.Datetime.now, string='End date', required=True)
    in_out = fields.Selection([('in', 'In'), ('out', 'Out'), ('all', 'All')], string='In/Out', required=True)

    def print_report(self):
        self.ensure_one()
        data = {
            "product_ids": self.product_ids.ids,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "in_out": self.in_out,
        }
        return self.env.ref('temp.action_report_product').report_action(None, data=data)

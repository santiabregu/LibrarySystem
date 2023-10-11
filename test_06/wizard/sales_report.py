from odoo import fields, models, api


class SalesReportWizard(models.TransientModel):
    _name = 'sales.report.wizard'
    _description = 'Description'

    product_ids = fields.Many2many(comodel_name='commprog.product', string='Product_ids')
    year = fields.Integer(string='Year')

    def print_report(self):
        self.ensure_one()
        data = {
            "product_ids": self.product_ids.ids,
            "start_date": self.year,
        }
        return self.env.ref('test_06.action_sales_report').report_action(None, data=data)

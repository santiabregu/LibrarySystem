from odoo import models, api


class CommprogReportInvoice(models.AbstractModel):
    _name = 'report.temp.report_product'
    _description = 'Invoice report'

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = [('date', '>=', data['start_date']), ('date', '<', data['end_date'])]

        if data['product_ids']:
            domain.append(('product_id', 'in', data['product_ids']))

        rreshta_fature_obj = self.env['commprog.invoice.line'].search(domain)

        res = {}

        for line in rreshta_fature_obj:
            product_id = line.product_id.id
            if not res.get(product_id):
                res[product_id] = {
                    'name': line.product_id.product,
                    'qty_in': 0,
                    'value_in': 0,
                    'qty_out': 0,
                    'value_out': 0,
                    'profit': 0,
                }
            if line.invoice_id.in_out:
                res[product_id]['qty_in'] += line.qty
                res[product_id]['value_in'] += line.qty * line.price
                res[product_id]['profit'] -= line.qty * line.price
            else:
                res[product_id]['qty_out'] += line.qty
                res[product_id]['value_out'] += line.qty * line.price
                res[product_id]['profit'] += line.qty * line.price

        return {
            'docs': res.values(),
        }

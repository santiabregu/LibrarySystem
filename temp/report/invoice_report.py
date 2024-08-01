from odoo import models, api


class CommprogReportInvoice(models.AbstractModel):
    _name = 'report.temp.report_invoice'
    _description = 'Invoice report'

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = [('date', '>=', data['start_date']), ('date', '<', data['end_date'])]

        if not data['product_ids']:
            name = 'Te gjitha produktet'
        else:
            domain.append(('product_id', 'in', data['product_ids']))
            produktet = self.env['commprog.product'].browse(data['product_ids']).mapped("product")
            name = f'Produktet: {", ".join(produktet)}'

        rreshta_fature_obj = self.env['commprog.invoice.line'].search(domain)
        res = []
        for product_line in rreshta_fature_obj:
            product = {
                'product': product_line.product_id.product,
                'qty': product_line.qty,
                'price': product_line.price,
                'total': product_line.total,
            }
            res.append(product)
        return {
            'docs': res,
            'r_name': name,
        }

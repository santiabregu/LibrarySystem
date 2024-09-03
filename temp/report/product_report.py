from odoo import models, api


class CommprogReportInvoice(models.AbstractModel):
    _name = 'report.temp.report_product'
    _description = 'Invoice report'

    # M1
    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     domain = [('date', '>=', data['start_date']), ('date', '<', data['end_date'])]
    #
    #     if data['product_ids']:
    #         domain.append(('product_id', 'in', data['product_ids']))
    #
    #     rreshta_fature_obj = self.env['commprog.invoice.line'].search(domain)
    #
    #     res = {}
    #
    #     for line in rreshta_fature_obj:
    #         product_id = line.product_id.id
    #         if not res.get(product_id):
    #             res[product_id] = {
    #                 'name': line.product_id.product,
    #                 'qty_in': 0,
    #                 'value_in': 0,
    #                 'qty_out': 0,
    #                 'value_out': 0,
    #                 'profit': 0,
    #             }
    #         if line.invoice_id.in_out:
    #             res[product_id]['qty_in'] += line.qty
    #             res[product_id]['value_in'] += line.qty * line.price
    #             res[product_id]['profit'] -= line.qty * line.price
    #         else:
    #             res[product_id]['qty_out'] += line.qty
    #             res[product_id]['value_out'] += line.qty * line.price
    #             res[product_id]['profit'] += line.qty * line.price
    #
    #     return {
    #         'docs': res.values(),
    #     }

    # M2
    @api.model
    def _get_report_values(self, docids, data=None):
        domain = [('date', '>=', data['start_date']), ('date', '<', data['end_date'])]
        product_domain = []
        if data['product_ids']:
            domain.append(('product_id', 'in', data['product_ids']))
            product_domain = [('id', 'in', data['product_ids'])]

        invoice_line_obj = self.env['commprog.invoice.line'].search(domain)

        res = []
        products = self.env['commprog.product'].search(product_domain)
        for product in products:
            product_lines_in = invoice_line_obj.filtered(
                lambda line: line.product_id.id == product.id and line.invoice_id.in_out)
            product_lines_out = invoice_line_obj.filtered(
                lambda line: line.product_id.id == product.id and not line.invoice_id.in_out)
            res.append({
                'name': product.product,
                'qty_in': sum(product_lines_in.mapped('qty')),
                'value_in': sum(product_lines_in.mapped('total')),
                'qty_out': sum(product_lines_out.mapped('qty')),
                'value_out': sum(product_lines_out.mapped('total')),
                'profit': sum(product_lines_out.mapped('total')) - sum(product_lines_in.mapped('total')),
            })

        return {
            'docs': res,
        }

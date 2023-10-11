from odoo import models, api, fields


class CommprogReportSales(models.AbstractModel):
    _name = 'report.test_06.report_sales'
    _description = 'Invoice report'

    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     domain = [('date', '>=', data['start_date']), ('date', '<', data['end_date'])]
    #
    #     if not data['product_ids']:
    #         name = 'Te gjitha produktet'
    #     else:
    #         domain.append(('product_id', 'in', data['product_ids']))
    #         produktet = self.env['commprog.product'].browse(data['product_ids']).mapped("name")
    #         name = f'Produktet {", ".join(produktet)}'
    #
    #     rreshta_fature_obj = self.env['commprog.invoice.line'].search(domain)
    #     rreshta_fature = []
    #
    #     for rec in rreshta_fature_obj:
    #         rreshta_fature.append({
    #             'produkt': rec.product_id.name,
    #             'sasi': rec.quantity,
    #             'cmimi': rec.price,
    #             'total': rec.total,
    #         })
    #     return {
    #         'docs': rreshta_fature,
    #         'r_name': name,
    #     }

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = [('date', '>=', '{}-01-01'.format(data['year'])), ('date', '<', '{}-01-01'.format(data['year'] + 1)), ('invoice_id.invoice_type', '=', 'out')]

        if not data['product_ids']:
            name = 'Te gjitha produktet'
        else:
            domain.append(('product_id', 'in', data['product_ids']))
            produktet = self.env['commprog.product'].browse(data['product_ids']).mapped("name")
            name = f'Produktet {", ".join(produktet)}'

        rreshta_fature_obj = self.env['commprog.invoice.line'].search(domain)
        months = []
        for i in range(12):
            months.append({'total': 0, 'quantity': 0})
        res_total = {}
        for rec in rreshta_fature_obj:
            month = fields.Date.to_date(rec.data).month
            if rec.product_id.id in res_total:
                res_total[(rec.product_id.id, rec.product_id.name)] = months.copy()
            res_total[rec.product_id.id, rec.product_id.name][month - 1]['total'] += rec.total
            res_total[rec.product_id.id, rec.product_id.name][month - 1]['quantity'] += rec.quantity

        return {
            'docs': res_total,
            'r_name': name,
        }

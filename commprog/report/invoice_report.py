from odoo import models, api


class CommprogReportInvoice(models.AbstractModel):
    _name = 'report.commprog.report_invoice'
    _description = 'Invoice report'

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = [('date', '>=', data['start_date']), ('date', '<', data['end_date'])]

        if not data['product_ids']:
            name = 'Te gjitha produktet'
        else:
            domain.append(('product_id', 'in', data['product_ids']))
            produktet = self.env['commprog.product'].browse(data['product_ids']).mapped("name")
            name = f'Produktet {", ".join(produktet)}'

        rreshta_fature_obj = self.env['commprog.invoice.line'].search(domain)
        rreshta_fature = []

        for rec in rreshta_fature_obj:
            rreshta_fature.append({
                'produkt': rec.product_id.name,
                'sasi': rec.quantity,
                'cmimi': rec.price,
                'total': rec.total,
            })
        return {
            'docs': rreshta_fature,
            'r_name': name,
        }

from odoo import models, api

class ReportBorrow(models.AbstractModel):
    _name = 'report.library.report_borrow'
    _description = 'Borrow Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        domain = [('borrowed_at', '>=', start_date), ('borrowed_at', '<=', end_date)]

        if not data.get('borrow_ids'):
            name = 'All Borrowed Books'
        else:
            domain.append(('id', 'in', data['borrow_ids']))
            borrows = self.env['library.borrow'].browse(data['borrow_ids']).mapped("book_id.name")
            name = f'Books: {", ".join(borrows)}'

        borrowed_books = self.env['library.borrow'].search(domain)
        res = []
        for borrow in borrowed_books:
            one_book = {
                'name': borrow.book_id.name,
                'genre': borrow.book_id.genre_ids.mapped('name')
            }
            res.append(one_book)
        return {
            'docs': res,
            'r_name': name,
        }
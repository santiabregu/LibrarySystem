from datetime import timedelta

from odoo import fields, models, api


class BorrowWizard(models.TransientModel):
    _name = 'library.borrow.wizard'
    _description = 'Borrow Wizard'

    member_id = fields.Many2one('library.member', string='Member', required=True)
    book_id = fields.Many2one('library.book', string='Book', required=True)
    borrow_employee_id = fields.Many2one('library.employee', string='Employee', required=True)
    borrowed_at = fields.Date(string='Borrowed At', required=True, default=fields.Date.today)
    return_due_date = fields.Date(string='Return Due Date', compute='_compute_return_due_date', store=True)

    @api.depends('borrowed_at')
    def _compute_return_due_date(self):
        for record in self:
            if record.borrowed_at:
                record.return_due_date = record.borrowed_at + timedelta(weeks=4)

    def action_create_borrow(self):
        self.env['library.borrow'].create({
            'member_id': self.member_id.id,
            'book_id': self.book_id.id,
            'borrow_employee_id': self.borrow_employee_id.id,
            'borrowed_at': self.borrowed_at,
            'return_due_date': self.return_due_date,
        })
        return {'type': 'ir.actions.act_window_close'}

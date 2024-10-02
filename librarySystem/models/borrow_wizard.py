from odoo import fields, models, api
from datetime import timedelta

class BorrowWizard(models.TransientModel):
    _name = 'library.borrow.wizard'
    _description = 'Borrow Wizard'

    member_id = fields.Many2one('library.member', string='Member', required=True)
    borrow_ids = fields.One2many('library.borrow.wizard.line', 'wizard_id', string='Borrows')

    def action_create_borrow(self):
        borrows_data = []
        for line in self.borrow_ids:
            borrows_data.append({
                'member_id': self.member_id.id,
                'book_id': line.book_id.id,
                'borrow_employee_id': line.borrow_employee_id.id,
                'borrowed_at': line.borrowed_at,
                'return_due_date': line.return_due_date,
            })
        borrows = self.env['library.borrow'].create(borrows_data)
        self.env['library.ticket'].create_ticket_from_borrows(borrows)
        return {'type': 'ir.actions.act_window_close'}

class BorrowWizardLine(models.TransientModel):
    _name = 'library.borrow.wizard.line'
    _description = 'Borrow Wizard Line'

    wizard_id = fields.Many2one('library.borrow.wizard', string='Wizard', required=True, ondelete='cascade')
    book_id = fields.Many2one('library.book', string='Book', required=True)
    borrow_employee_id = fields.Many2one('library.employee', string='Employee', required=True)
    borrowed_at = fields.Date(string='Borrowed At', required=True, default=fields.Date.today)
    return_due_date = fields.Date(string='Return Due Date', compute='_compute_return_due_date', store=True)

    @api.depends('borrowed_at')
    def _compute_return_due_date(self):
        for record in self:
            if record.borrowed_at:
                record.return_due_date = record.borrowed_at + timedelta(weeks=4)
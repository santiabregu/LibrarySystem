from odoo import fields, models, api
from odoo.exceptions import UserError

class CommprogTicket(models.Model):
    _name = 'library.ticket'
    _description = 'Description'
    _rec_name = 'code'

    code = fields.Char(string='Code', required=True, default='New')
    date = fields.Date(string='Date', required=True)
    member_id = fields.Many2one(comodel_name='library.member', string='Member', required=True)
    employee_id = fields.Many2one(comodel_name='library.employee', string='Employee', required=True)
    state = fields.Selection(string='State', selection=[('draft', 'Draft'), ('done', 'Done'), ('paid', 'Paid')],
                             default='draft')
    ticket_line_ids = fields.One2many(comodel_name='library.ticket.line', inverse_name='ticket_id', string='Ticket Line')

    @api.model
    def create_ticket_from_borrows(self, borrows):
        if not borrows:
            raise UserError('No borrows provided to create a ticket.')

        member = borrows[0].member_id
        employee = borrows[0].employee_id
        date = borrows[0].borrowed_at

        ticket_lines = []
        for borrow in borrows:
            ticket_lines.append((0, 0, {
                'book_id': borrow.book_id.id,
                'qty': 1,
                'date': borrow.borrowed_at,
                'return_due_date': borrow.return_due_date,
            }))

        ticket_vals = {
            'date': date,
            'member_id': member.id,
            'employee_id': employee.id,
            'ticket_line_ids': ticket_lines,
        }
        self.create(ticket_vals)

    def action_done(self):
        for ticket_line in self.ticket_line_ids:
            book = ticket_line.book_id
            if book.copies_available > 0:
                book.write({'copies_available': book.copies_available - 1})
            else:
                raise UserError('No copies available for the book: %s' % book.name)
        self.state = 'done'


class CommprogTicketLine(models.Model):
    _name = 'library.ticket.line'

    ticket_id = fields.Many2one(comodel_name='library.ticket', string='Ticket', required=True, ondelete='cascade')
    book_id = fields.Many2one(comodel_name='library.book', string='Product', required=True)
    qty = fields.Float(string='Qty', required=True, default=1)
    date = fields.Date(string='Date', related='ticket_id.date')
    return_due_date = fields.Date(string='Return Due Date', required=True)
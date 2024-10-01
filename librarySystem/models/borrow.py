from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Borrow(models.Model):
    _name = 'library.borrow'

    member_id = fields.Many2one(comodel_name='library.member', string='Member', required=True)
    book_id = fields.Many2one(comodel_name='library.book', string='Book', required=True)
    borrow_employee_id = fields.Many2one(comodel_name='library.employee', string='Employee', required=True)
    borrowed_at = fields.Date(string='Borrowed At', required=True, default=fields.Date.today())
    return_due_date = fields.Date(string='Return Due Date', required=True)
    returned = fields.Boolean(string='Returned', default=False)
    returned_at = fields.Date(string='Returned At')
    return_employee_id = fields.Many2one(comodel_name='library.employee', string='Return Employee')
    return_condition = fields.Selection(string='Condition', selection=[('good', 'Good'), ('damaged', 'Damaged')], default='good')
    borrow_finalized = fields.Boolean(string='Borrow Finalized', default=False)

    @api.model
    def create_multiple_borrows(self, borrows_data):
        borrows = self.create(borrows_data)
        self.env['library.ticket'].create_ticket_from_borrows(borrows)
        return borrows
    @api.constrains('returned', 'returned_at', 'return_employee_id', 'return_condition')
    def _check_return_fields(self):
        for record in self:
            if record.returned:
                if not record.returned_at or not record.return_employee_id or not record.return_condition:
                    raise ValidationError("When 'Returned' is set to True, 'Returned At', 'Return Employee', and 'Return Condition' must be filled.")

    @api.model
    def create(self, vals):
        borrow = super(Borrow, self).create(vals)
        borrow._reduce_book_copies()
        return borrow

    def write(self, vals):
        for record in self:
            if record.borrow_finalized:
                raise ValidationError("You cannot edit a borrow that has been finalized.")
            if 'returned' in vals and vals['returned'] and not record.returned:
                record._increase_book_copies()
                vals['borrow_finalized'] = True
        return super(Borrow, self).write(vals)

    def _reduce_book_copies(self):
        for record in self:
            if record.book_id.copies_available > 0:
                record.book_id.copies_available -= 1
            else:
                raise ValidationError("No copies available for the book: %s" % record.book_id.name)



    def _increase_book_copies(self):
        for record in self:
            record.book_id.copies_available += 1
    # add function that calculates return_due_date based on borrowed_at , adding 3 weeks to the borrowed_at date
    # check if there are copies available for a book before a borrow
    # after a borrow, reduce the number of copies_available for a book
    # should make possible to create a number of borrows in one go (list of borrows),
    # it can be implemented as a button add borrowed book

    # if memberSubscription of a member has expired , member cant do a borrow
    # add field in view that shows if membership is active
    # add field in view that shows if book is available
    # when a member borrows a series of books, a borrow list should be created

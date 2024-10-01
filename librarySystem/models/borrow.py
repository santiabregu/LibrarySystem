from odoo import fields, models, api

class Borrow(models.Model):
    _name = 'library.borrow'

    # every borrow has one member, one book , one employee
    member_id = fields.Many2one(comodel_name='library.member', string='Member', required=True)
    book_id = fields.Many2one(comodel_name='library.book', string='Book', required=True)
    borrow_employee_id = fields.Many2one(comodel_name='library.employee', string='Employee', required=True)
    borrowed_at = fields.Date(string='Borrowed At', required=True, default=fields.Date.today())
    return_due_date = fields.Date(string='Return Due Date', required=True)
    returned = fields.Boolean(string='Returned', default=False)
    returned_at = fields.Date(string='Returned At')
    return_employee_id = fields.Many2one(comodel_name='library.employee', string='Return Employee')
    return_condition = fields.Selection(string='Condition', selection=[('good', 'Good'), ('damaged', 'Damaged')],
                                        default='good')

    @api.model
    def create_multiple_borrows(self, borrows_data):
        borrows = self.create(borrows_data)
        self.env['library.ticket'].create_ticket_from_borrows(borrows)
        return borrows


    # add function that calculates return_due_date based on borrowed_at , adding 3 weeks to the borrowed_at date
    # check if there are copies available for a book before a borrow
    # after a borrow, reduce the number of copies_available for a book
    # should make possible to create a number of borrows in one go (list of borrows),
    # it can be implemented as a button add borrowed book

    # if memberSubscription of a member has expired , member cant do a borrow
    # add field in view that shows if membership is active
    # add field in view that shows if book is available
    # when a member borrows a series of books, a borrow list should be created

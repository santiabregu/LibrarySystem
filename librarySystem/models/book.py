from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Book(models.Model):
    _name = 'library.book'
    _description = 'book'

    title = fields.Char(string='Title', required=True)
    author_id = fields.Many2one(comodel_name='library.author', string='Author', required=True)
    published_at = fields.Date(string='Published At', required=True)
    genre_ids = fields.One2many(comodel_name='library.genre', inverse_name='book_id', string='Genres')
    copies_available = fields.Integer(string='Copies Available', default=1)
    copies_total = fields.Integer(string='Total Copies', required=True)
    borrow_ids = fields.One2many(comodel_name='library.borrow', inverse_name='book_id', string='Borrows')
    image = fields.Binary(string="Image")

    @api.onchange('copies_total')
    def _onchange_copies_total(self):
        if not self.id:
            self.copies_available = self.copies_total
    @api.constrains('copies_available')
    def _check_quantity(self):
        for book in self:
            if book.copies_available < 0:
                raise ValidationError('Quantity must be positive')
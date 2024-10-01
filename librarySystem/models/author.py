from odoo import fields, models

class Author(models.Model):
    _name = 'library.author'
    _description = 'Author'

    name = fields.Char(string='Name', required=True)
    surname = fields.Char(string='Surname', required=True)
    book_ids = fields.One2many(comodel_name='library.book', inverse_name='author_id', string='Books')
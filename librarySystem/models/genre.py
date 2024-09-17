from odoo import fields, models

class CommprogGenre(models.Model):
    _name = 'library.genre'
    _description = 'Genre'

    name = fields.Char(string='Genre', required=True)
    book_id = fields.Many2one(comodel_name='library.book', string='Book', required=True)
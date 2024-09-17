from odoo import fields, models

class CommprogPublisher(models.Model):
    _name = 'library.publisher'
    _description = 'Description'

    name = fields.Char('Name', required=True)
    address = fields.Char(string='Address')
    phoneNumber = fields.Char(string='Phone Number')

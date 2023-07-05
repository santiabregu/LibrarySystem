from odoo import fields, models


class CommprogClient(models.Model):
    _name = 'commprog.client'

    name = fields.Char(string="Name", required=True)
    surname = fields.Char(string='Surname', required=True)
    phone = fields.Char(string='Phone')
    points = fields.Integer(string="Points")

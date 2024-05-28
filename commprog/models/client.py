from odoo import fields, models


class CommprogClient(models.Model):
    _name = 'commprog.client'

    name = fields.Char(string="Name", required=True)
    surname = fields.Char(string='Surname', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Char(string='Address')
    nid = fields.Char(string='NID')
    points = fields.Integer(string='Points', default=0)
    type = fields.Selection(string='Type', selection=[('client', 'Client'), ('partner', 'Partner')], default='client')

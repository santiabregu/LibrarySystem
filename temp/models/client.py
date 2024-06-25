from odoo import fields, models


class CommprogClient(models.Model):
    _name = 'commprog.client'
    _description = 'Description'

    name = fields.Char(string='Name', required=True)
    surname = fields.Char(string='Surname', required=True)
    tel = fields.Char(string='Tel', required=True)
    email = fields.Char(string='Email')
    address = fields.Char(string='Address')
    nid = fields.Char(string='NID')
    points = fields.Float(string='Points', default=0, readonly=True)
    type = fields.Selection(string='Type', selection=[('client', 'Client'), ('partner', 'Partner')], default='client')

from odoo import fields, models, api


class CommprogCategory(models.Model):
    _name = 'commprog.category'
    _description = 'Description'

    name = fields.Char(string='Category', required=True)

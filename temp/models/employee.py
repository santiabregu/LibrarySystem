from odoo import fields, models


class CommprogEmployee(models.Model):
    _name = 'commprog.employee'
    _description = 'Description'

    name = fields.Char('Name', required=True)
    bank = fields.Char(string='IBAN Bank', required=True)
    role = fields.Selection(string='Role', selection=[('manager', 'Manager'), ('seller', 'Seller'), ], required=True)
    salary = fields.Float(string='Salary', required=True)
    bonus = fields.Float(string='Bonus')
    user_id = fields.Many2one(comodel_name='res.users')

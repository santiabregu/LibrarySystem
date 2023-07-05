from odoo import fields, models


class CommprogEmployee(models.Model):
    _name = 'commprog.employee'
    _description = 'Description'

    name = fields.Char(string="Name", required=True)
    surname = fields.Char(string='Surname', required=True)
    position = fields.Selection(string='Position', required=True,
                                selection=[
                                    ('sales', 'Sales'),
                                    ('manager', 'Manager')])
    salary = fields.Float(string='Salary', required=True)

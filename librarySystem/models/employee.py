from odoo import fields, models


class CommprogEmployee(models.Model):
    _name = 'library.employee'
    _description = 'Description'

    employeeId = fields.Integer(string='Employee ID', required=True, index=True)
    name = fields.Char('Name', required=True)
    bank = fields.Char(string='IBAN Bank', required=True)
    salary = fields.Float(string='Salary', required=True)
    phone_number = fields.Char(string='Phone Number', required=True)


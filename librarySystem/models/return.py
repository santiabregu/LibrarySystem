from odoo import fields, models, api

class Return(models.Model):
    _name = 'library.return'
    _rec_name = 'return'

    borrow_id = fields.Integer(string='Product ID', required=True)
    employeeId = fields.Integer(string='Employee ID', required=True)
    returnedAt = fields.Date(string='Returned At', required=True)
    condition  = fields.Char(string='Condition', selection=[('good', 'Good'), ('damaged', 'Damaged')], default='good')
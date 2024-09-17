from odoo import fields, models, api


class Subscription(models.Model):
    _name = 'library.subscription'
    _description = 'Subscription Details'

    subscription_name = fields.Char(string='Name', required=True)
    price = fields.Float(string='Price', required=True)
    duration_in_weeks = fields.Integer(string='Duration', required=True)


from odoo import fields, models, api


class Subscription(models.Model):
    _name = 'library.subscription'
    _description = 'Subscription Details'

    subscription_name = fields.Char(string='Name', required=True)
    price = fields.Float(string='Price', required=True)
    duration_in_weeks = fields.Integer(string='Duration in weeks', required=True)

    def name_get(self):
        result = []
        for record in self:
            name = record.subscription_name
            result.append((record.id, name))
        return result
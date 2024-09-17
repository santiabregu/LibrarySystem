from datetime import timedelta
from odoo import fields, models, api

class CommprogMemberSubscription(models.Model):
    _name = 'library.member_subscription'

    code = fields.Char(string='Code', required=True, default='New')
    subscription_type = fields.Selection(string='Subscription Type', selection='_get_subscription_types', required=True)
    member_id = fields.Many2one('library.member', string='Member', required=True)
    employee_id = fields.Many2one('library.employee', string='Employee', required=True)
    pay_method = fields.Selection(string='Pay Method', selection=[('cash', 'Cash'), ('card', 'Card')], default='cash')
    sub_start_date = fields.Date(string='Subscription Start Date', required=True, default=fields.Date.today())
    sub_end_date = fields.Date(string='Subscription End Date', required=True)

    @api.depends('subscription_type', 'sub_start_date')
    def _compute_sub_end_date(self):
        for record in self:
            if record.subscription_type:
                subscription = self.env['library.subscription'].browse(record.subscription_type)
                record.sub_end_date = record.sub_start_date + timedelta(weeks=subscription.duration_in_weeks)

    @api.model
    def _get_subscription_types(self):
        subscriptions = self.env['library.subscription'].search([])
        return [(sub.id, sub.subscription_name) for sub in subscriptions]

    @api.model
    def create(self, vals):
        record = super(CommprogMemberSubscription, self).create(vals)
        self.env['library.member'].update_last_subscription(record.member_id.id, record.id)
        return record
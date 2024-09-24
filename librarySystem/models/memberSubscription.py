from datetime import timedelta, date
from odoo import fields, models, api

class CommprogMemberSubscription(models.Model):
    _name = 'library.member_subscription'

    code = fields.Char(string='Code', required=True, default='New')
    subscription_type = fields.Char(string='Subscription Type', required=True)
    member_id = fields.Many2one('library.member', string='Member', required=True)
    employee_id = fields.Many2one('library.employee', string='Employee')
    pay_method = fields.Selection(string='Pay Method', selection=[('cash', 'Cash'), ('card', 'Card')], default='cash')
    sub_start_date = fields.Date(string='Subscription Start Date', required=True, default=fields.Date.today())
    sub_end_date = fields.Date(string='Subscription End Date', required=True)
    is_active = fields.Boolean(string='Is Active', compute='_compute_is_active', store=True)

    @api.depends('sub_end_date')
    def _compute_is_active(self):
        for record in self:
            record.is_active = record.sub_end_date and record.sub_end_date > date.today()

    @api.depends('subscription_type', 'sub_start_date')
    def _compute_sub_end_date(self):
        for record in self:
            if record.subscription_type:
                subscription = self.env['library.subscription'].search([('subscription_name', '=', record.subscription_type)], limit=1)
                record.sub_end_date = record.sub_start_date + timedelta(weeks=subscription.duration_in_weeks)

    @api.model
    def create(self, vals):
        record = super(CommprogMemberSubscription, self).create(vals)
        record.member_id.update_last_member_subscription(record.member_id.id, record.id)
        return record
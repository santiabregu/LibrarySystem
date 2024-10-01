from datetime import timedelta, date
from odoo import fields, models, api
import random
import string

class CommprogMemberSubscription(models.Model):
    _name = 'library.member_subscription'

    code = fields.Char(string='Code', required=True, default='New')
    subscription_type = fields.Many2one('library.subscription', string='Subscription Type', required=True)
    member_id = fields.Many2one('library.member', string='Member', required=True)
    employee_id = fields.Many2one('library.employee', string='Employee')
    pay_method = fields.Selection(string='Pay Method', selection=[('cash', 'Cash'), ('card', 'Card')], default='cash')
    sub_start_date = fields.Date(string='Subscription Start Date', required=True, default=fields.Date.today())
    sub_end_date = fields.Date(string='Subscription End Date', compute='_compute_sub_end_date', store=True)
    is_active = fields.Boolean(string='Is Active', compute='_compute_is_active', store=True)

    @api.depends('sub_end_date')
    def _compute_is_active(self):
        for record in self:
            record.is_active = record.sub_end_date and record.sub_end_date > date.today()

    @api.depends('subscription_type', 'sub_start_date')
    def _compute_sub_end_date(self):
        for record in self:
            if record.subscription_type and record.sub_start_date:
                record.sub_end_date = record.sub_start_date + timedelta(weeks=record.subscription_type.duration_in_weeks)

    @api.onchange('subscription_type', 'sub_start_date')
    def _onchange_subscription_details(self):
        if self.subscription_type and self.sub_start_date:
            self.sub_end_date = self.sub_start_date + timedelta(weeks=self.subscription_type.duration_in_weeks)
        if self.subscription_type or self.sub_start_date:
            self.code = self._generate_random_code()

    def _generate_random_code(self):
        prefix = 'INV'
        date_part = date.today().strftime('%Y%m%d')
        random_part = ''.join(random.choices(string.digits, k=5))
        return f'{prefix}{date_part}{random_part}'
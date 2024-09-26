from datetime import timedelta

from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class Member(models.Model):
    _name = 'library.member'
    _description = 'Member Details'

    borrow_ids = fields.One2many(comodel_name='library.borrow', inverse_name='member_id', string='Borrows')
    name = fields.Char(string='Name', required=True)
    surname = fields.Char(string='Surname', required=True)
    membership_date = fields.Date(string='Membership Date', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone', required=True)
    address = fields.Char(string='Address', required=True)
    last_member_subscription_id = fields.Many2one('library.member_subscription', string='Last Subscription', compute='_compute_last_member_subscription', store=True)
    subscription_type = fields.Many2one('library.subscription', string='Subscription Type', required=True)
    is_last_subscription_active = fields.Boolean(string='Is Last Subscription Active', compute='_compute_is_last_subscription_active')

    @api.depends('last_member_subscription_id')
    def _compute_is_last_subscription_active(self):
        for member in self:
            member.is_last_subscription_active = member.last_member_subscription_id.is_active if member.last_member_subscription_id else False

    @api.depends('last_member_subscription_id')
    def _compute_last_member_subscription(self):
        for member in self:
            subscriptions = self.env['library.member_subscription'].search([('member_id', '=', member.id)], order='sub_start_date desc')
            member.last_member_subscription_id = subscriptions[0] if subscriptions else False

    @api.model
    def create(self, vals):
        member = super(Member, self).create(vals)
        subscription = self.env['library.subscription'].browse(vals['subscription_type'])
        sub_start_date = fields.Date.today()
        sub_end_date = sub_start_date + timedelta(weeks=subscription.duration_in_weeks)
        self.env['library.member_subscription'].create({
            'subscription_type': subscription.id,  # Use the ID of the subscription
            'member_id': member.id,
            'employee_id': self.env.user.employee_id.id,
            'sub_start_date': sub_start_date,
            'sub_end_date': sub_end_date,
        })
        return member

    def action_open_borrow_wizard(self):
        _logger.info('Opening borrow wizard for member ID: %s', self.id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Borrow',
            'res_model': 'library.borrow.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_member_id': self.id,
            },
        }

    def unlink(self):
        for member in self:
            # Delete related borrows
            member.borrow_ids.unlink()
            # Delete related subscriptions
            self.env['library.member_subscription'].search([('member_id', '=', member.id)]).unlink()
            # Delete related tickets
            self.env['library.ticket'].search([('member_id', '=', member.id)]).unlink()
        return super(Member, self).unlink()
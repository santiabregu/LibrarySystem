from datetime import timedelta
from odoo import fields, models, api
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class Member(models.Model):
    _name = 'library.member'
    _description = 'Member Details'

    borrow_ids = fields.One2many(comodel_name='library.borrow', inverse_name='member_id', string='Borrows')
    name = fields.Char(string='Name', required=True)
    surname = fields.Char(string='Surname', required=True)
    membership_date = fields.Date(string='Membership Date')
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone', required=True)
    address = fields.Char(string='Address', required=True)
    last_member_subscription_id = fields.Many2one('library.member_subscription', string='Last Subscription', compute='_compute_last_member_subscription', store=True)
    is_last_subscription_active = fields.Boolean(string='Is Last Subscription Active', compute='_compute_is_last_subscription_active')
    is_subscription_saved = fields.Boolean(string='Is Subscription Saved', default=False)
    subscription_ids = fields.One2many('library.member_subscription', 'member_id', string='Subscriptions')
    borrow_info_html = fields.Html(string='Books borrowed', compute='_compute_borrow_info_html')  # Add this line

    @api.depends('borrow_ids')
    def _compute_borrow_info_html(self):
        for member in self:
            borrow_info_html = []
            for borrow in member.borrow_ids:
                borrow_info_html.append(f'<a href="/web#id={borrow.id}&model=library.borrow&view_type=form" target="_blank">Borrow ID: {borrow.id}, Book Title: {borrow.book_id.title}</a>')
            member.borrow_info_html = '<br/>'.join(borrow_info_html)

    @api.depends('last_member_subscription_id')
    def _compute_is_last_subscription_active(self):
        for member in self:
            member.is_last_subscription_active = member.last_member_subscription_id.is_active if member.last_member_subscription_id else False

    @api.depends('last_member_subscription_id')
    def _compute_last_member_subscription(self):
        for member in self:
            subscriptions = self.env['library.member_subscription'].search([('member_id', '=', member.id)], order='sub_start_date desc')
            member.last_member_subscription_id = subscriptions[0] if subscriptions else False

    def _update_membership_date(self):
        for member in self:
            subscriptions = self.env['library.member_subscription'].search([('member_id', '=', member.id)], order='sub_start_date asc')
            if subscriptions:
                member.membership_date = subscriptions[0].sub_start_date

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

    @api.model
    def create(self, vals):
        if not vals.get('subscription_ids'):
            raise ValidationError("You cannot create a member without a subscription.")
        if len(vals.get('subscription_ids')) > 1:
            raise ValidationError("You can only add one subscription when creating a new member.")

        member = super(Member, self).create(vals)

        # Force computation of last_member_subscription_id
        member._compute_last_member_subscription()
        member._compute_is_last_subscription_active()

        # Update membership date
        member._update_membership_date()

        return member
    def unlink(self):
        for member in self:
            # Delete related borrows
            member.borrow_ids.unlink()
            # Delete related subscriptions
            self.env['library.member_subscription'].search([('member_id', '=', member.id)]).unlink()
            # Delete related tickets
            self.env['library.ticket'].search([('member_id', '=', member.id)]).unlink()
        return super(Member, self).unlink()
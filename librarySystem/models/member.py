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
    last_subscription_id = fields.Many2one('library.member_subscription', string='Last Subscription')

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
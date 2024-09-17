from odoo import fields, models, api


class Member(models.Model):
    _name = 'library.member'
    _description = 'Member Details'

    # a member has various borrowed books
    borrow_ids = fields.One2many(comodel_name='library.borrow', inverse_name='member_id', string='Borrows')
    name = fields.Char(string='Name', required=True)
    surname = fields.Char(string='Surname', required=True)
    membership_date = fields.Date(string='Membership Date', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone', required=True)
    address = fields.Char(string='Address', required=True)
    last_subscription_id = fields.Many2one('library.member_subscription', string='Last Subscription')

    @api.model
    def update_last_subscription(self, member_id):
        member = self.search([('id', '=', member_id)], limit=1)
        if member:
            last_subscription = self.env['library.member_subscription'].search(
                [('member_id', '=', member_id)], order='sub_start_date desc', limit=1
            )
            if last_subscription:
                member.last_subscription_id = last_subscription.id
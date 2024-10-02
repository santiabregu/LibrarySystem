from odoo import fields, models

class BorrowReport(models.TransientModel):
    _name = 'borrow.report'
    _description = 'Borrow Report'

    borrow_ids = fields.Many2many(comodel_name='library.borrow', string='Borrowed Books')
    start_date = fields.Date(default=fields.Date.context_today, string='Start Date', required=True)
    end_date = fields.Date(default=fields.Date.context_today, string='End Date', required=True)

    def print_report(self):
        self.ensure_one()
        data = {
            "borrow_ids": self.borrow_ids.ids,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
        return self.env.ref('library.action_report_borrow').report_action(self, data=data)
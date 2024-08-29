from odoo import models


class CommprogInvoice(models.Model):
    _inherit = 'commprog.invoice'

    def action_done(self):
        super(CommprogInvoice, self).action_done()
        if not self.in_out:
            self.action_paid()

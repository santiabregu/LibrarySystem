from odoo import fields, models


class CommprogProduct(models.Model):
    _inherit = 'commprog.product'

    name = fields.Char(string="Emri i Produkti", required=True)
    unit = fields.Selection(string='Unit', required=False,
                            selection=[('kg', 'Kilogram'), ('l', 'Liter'), ])

    def set_kg(self):
        self.unit = 'kg'

    def set_l(self):
        self.unit = 'l'

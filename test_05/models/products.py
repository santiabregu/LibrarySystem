from odoo import fields, models, api


class Test05Products(models.Model):
    _name = 'test_05.products'
    _description = 'Description'

    name = fields.Char()
    weight = fields.Float(string='Weight')
    weight_deviation = fields.Float(string='Weight deviation')
    quality_ids = fields.One2many(comodel_name='test_05.products.quality', inverse_name='name', string='Quality')

    def check_quality(self):
        """ Kap te gjitha item te produktit qe nuk jane
            kontrolluar (controlled) dhe modifikon fushen (refuse)
        """
        # not_controlled = self.env['test_05.product.item'].search([('name', '=', self.id), ('controlled', '=', False)])
        min_weight = self.weight - self.weight_deviation
        max_weight = self.weight + self.weight_deviation
        # for item in not_controlled:
        #     item.controlled = True
        #     if not (min_weight < item.weight < max_weight):
        #         item.refuse = True
        not_refused_items = self.env['test_05.product.item'].search([('name', '=', self.id), ('controlled', '=', False), ('weight', '>', min_weight), ('weight', '<', max_weight)])
        not_refused_items.write({'controlled': True})
        refused_items = self.env['test_05.product.item'].search(
            [('name', '=', self.id), ('controlled', '=', False), '|', ('weight', '<', min_weight),
             ('weight', '>', max_weight)])
        refused_items.write({'controlled': True, 'refused': True})

    def create_quality_lines(self):
        """ Per cdo lot_id, factory_id per kete
        produkt krijohet nje rresht quality i
        cili ruan ratio, factory_id, produc_id, lot_id"""
        pass


class Test05Factory(models.Model):
    _name = 'test_05.factory'
    _description = 'Test05Factory'

    name = fields.Char()
    capacity = fields.Integer(string='Capacity')


class Test05ProductionLot(models.Model):
    _name = 'test_05.production.lot'
    _description = 'ProductionLot'

    name = fields.Char()
    start_date = fields.Date(string='Start date', required=True)
    end_date = fields.Date(string='End date', required=True)


class Test05ProductItem(models.Model):
    _name = 'test_05.product.item'
    _description = 'Test05Production'

    name = fields.Many2one(comodel_name='test_05.products', string='Produkt', required=True)
    code = fields.Char(string='Code', required=True)
    factory_id = fields.Many2one(comodel_name='test_05.factory', string='Factory', required=True)
    lot_id = fields.Many2one(comodel_name='test_05.production.lot', string='Lot', required=True)
    weight = fields.Float(string='Weight')
    refuse = fields.Boolean(string='Refuse', required=True, default=False)
    controlled = fields.Boolean(string='Controlled', required=True, default=False)


class Test05ProductQuality(models.Model):
    _name = 'test_05.products.quality'
    _description = 'Test05ProductQuality'

    name = fields.Many2one(comodel_name='test_05.products', string='Produkt', required=True)
    ratio = fields.Float(string='Ratio')
    factory_id = fields.Many2one(comodel_name='test_05.factory', string='Factory', required=True)
    lot_id = fields.Many2one(comodel_name='test_05.production.lot', string='Lot', required=True)

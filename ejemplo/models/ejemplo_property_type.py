from odoo import fields, models, api

class PropertyType(models.Model):
    _name='ejemplo.property.type'

    name=fields.Char(required=True)
    _order='name'
    property_ids = fields.One2many(comodel_name="ejemplo.real.estate.model", inverse_name="property_type_id")
    sequence=fields.Integer('Sequence')
    offers_ids=fields.One2many('ejemplo.property.offer', 'property_type_id')
    offer_count=fields.Integer(compute='_compute_property_type_count')

    _sql_constraints = [
         ('unique_value_type', 'UNIQUE(name)', 'Los tipos deben ser unicas')
    ]

    
    @api.depends('offers_ids')
    def _compute_property_type_count(self):
        for record in self:
            record.offer_count = len(record.offers_ids.filtered(lambda o: o.property_type_id.id == record.id))
  
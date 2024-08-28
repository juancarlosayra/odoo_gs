from odoo import fields, models

class PropertyOffer(models.Model):
    _name='ejemplo.property.offer'

    price=fields.Float(required=True)
    status=fields.Selection(string='status', selection=[('accepted', 'Accepted'),
    ('refused','Refused')], copy=False)
    partner_id=fields.Many2one('res.partner', required=True)
    property_id=fields.Many2one('ejemplo.real.estate.model', required=True, ondelete='cascade')
    property_type_id=fields.Many2one(related='property_id.property_type_id')
    
    _order='price desc'
    
    _sql_constraints = [
      ('check_price_positive', 'CHECK(price > 0)', 'El precio de una oferta debe ser estrictamente positivo')
    ]

    
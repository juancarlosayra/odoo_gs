from odoo import fields, models

class PropertyTag(models.Model):
    _name='ejemplo.property.tag'

    name= fields.Char(required=True)
    color=fields.Integer(string='Color', widget="color_picker")
    _order='name'

    _sql_constraints = [
         ('unique_value', 'UNIQUE(name)', 'Las tags deben ser unicas')
    ]
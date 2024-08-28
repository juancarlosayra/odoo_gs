from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError

class RealEstate(models.Model):
    _name = 'ejemplo.real.estate.model'
    _description = 'Second model example'

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Datetime.today()+timedelta(365/4))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False, compute='_compute_acc_selling_price')
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active=fields.Boolean(string='Available')
    state=fields.Selection(string='Estado', 
      selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'),
      ('sold', 'Sold'), ('canceled', 'Canceled')], default='new')
    garden_orientation = fields.Selection(string = 'garden_orientation',
      selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    
    property_type_id=fields.Many2one('ejemplo.property.type', string='Property Type',
    options={'no_quick_create': True})

    salesperson=fields.Many2one('res.users',  default=lambda self: self.env.user)
    buyer=fields.Many2one('res.partner', copy=False, compute='_compute_acc_buyer')
    tags_ids=fields.Many2many('ejemplo.property.tag')
    offer_ids=fields.One2many('ejemplo.property.offer', 'property_id', string='Offer',
    ondelete='cascade')

    _order='id desc'
    
    total_area=fields.Float(compute='_compute_total')
    best_offer=fields.Integer(compute='_compute_highest_offer')
    offer_status=fields.Char(compute='_compute_offer_status')



    _sql_constraints = [
      ('valid_price', 'CHECK(expected_price >= 0)', 'El precio de una vivienda debe ser estrictamente positivo'),
      ('valid_selling_price', 'CHECK(selling_price >= 0)', 'El precio esperado de una vivienda debe ser estrictamente positivo'),
      
    ]

    @api.depends('garden_area','living_area')
    def _compute_total(self):
      for area in self:
        area.total_area = area.garden_area + area.living_area

    @api.depends('offer_ids')
    def _compute_highest_offer(self):
      for record in self:
        if record.offer_ids:
          record.best_offer=max(record.offer_ids.mapped('price'))
        else:
          record.best_offer = 0

    @api.onchange('garden')
    def _compute_onchange_garden(self):
      if self.garden:
        self.garden_area = 10
        self.garden_orientation = 'north'
      else:
        self.garden_area = 0
        self.garden_orientation = None

    def sold(self):
      for record in self:
        if record.state == 'canceled':
          raise UserError('Una propiedad que ha sido cancelada no puede ser vendida')
        record.state = 'sold'
      return True

    def canceld(self):
      for record in self:
        if record.state == 'sold':
          raise UserError('Una propiedad que ha sido vendida no puede ser cancelada')
        record.state = 'canceled'
     
    def _compute_offer_status(self):
      for record in self:
        record.offer_status = None if not record.offer_ids else "accepted" if record.offer_ids.filtered(lambda o: o.status == "accepted") else "refused"
    
    @api.depends('offer_ids')
    def _compute_acc_selling_price(self):
      for record in self:
        accepted_offer = record.offer_ids.filtered(lambda o: o.status == 'accepted')
        if accepted_offer:
            record.selling_price = accepted_offer[0].price
        else:
            record.selling_price = 0

    @api.depends('offer_ids')
    def _compute_acc_buyer(self):
      for record in self:
        accepted_offer = record.offer_ids.filtered(lambda o: o.status == 'accepted')
        if accepted_offer:
            record.buyer = accepted_offer[0].partner_id
        else:
            record.buyer = None
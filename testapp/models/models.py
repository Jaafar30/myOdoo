# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TestApp(models.Model):
    _name = 'my.app'
    _description = 'Hello World'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float()
    description = fields.Text()
    trueFalse = fields.Boolean()
    html = fields.Html()
    date = fields.Date()
    date_time = fields.Datetime()
    binary = fields.Binary() #for images
    selection = fields.Selection([('1','val1'),('2','val2'),('3','val3'),]) #(value,label)

class MyOrders(models.Model):
    _name = 'my.order'

    name = fields.Char()
    date_time = fields.Datetime()
    items_ids = fields.One2many('my.orders.items','order_id')

class MyOrdersItems(models.Model):
    _name = 'my.orders.items'

    name = fields.Char()
    itemPrice = fields.Float()
    qty = fields.Integer()
    order_id = fields.Many2one('my.order')









    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100

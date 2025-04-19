from odoo import models,fields,api,_


class JaffarRoom(models.Model):
    _name = 'jaffar_module.room'
    _description = 'Room'

    name = fields.Char(string='Room Name',required=True)
    code = fields.Char(string="Room Code",required=True)
    
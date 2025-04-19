from odoo import models,fields,api,_


class JaffarLocation(models.Model):
    _name = 'jaffar_module.location'
    _description = 'Location'

    name = fields.Char(string='Location Name',required=True)
    code = fields.Char(string="Location Code",required=True)
    
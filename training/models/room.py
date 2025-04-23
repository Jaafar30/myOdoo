from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class TrainingRoom(models.Model):
    _name = 'training.room'
    _description = 'Room model'

    name = fields.Char(string='Room Name', required=True)
    code = fields.Char(string="Room Code", required=True)
    location_id = fields.Many2one('training.location', string='location',required=True)

    @api.constrains('name', 'code')
    def _check_unique_name_code(self):
        for record in self:
            # check name uniquene
            existing_name = self.search([
                ('name', '=', record.name),
                ('id', '!=', record.id)
            ], limit=1)
            if existing_name:
                raise ValidationError(_("The room name '%s' must be unique.") % record.name)

            # check code uniquene
            existing_code = self.search([
                ('code', '=', record.code),
                ('id', '!=', record.id)
            ], limit=1)
            if existing_code:
                raise ValidationError(_("The room code '%s' must be unique.") % record.code)

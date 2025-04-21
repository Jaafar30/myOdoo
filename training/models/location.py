from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class TrainingLocation(models.Model):
    _name = 'training.location'
    _description = 'Location model'

    name = fields.Char(string='Room Name', required=True)
    code = fields.Char(string="Room Code", required=True)

    @api.constrains('name', 'code')
    def _check_unique_name_code(self):
        for record in self:
            # check name uniquene
            existing_name = self.search([
                ('name', '=', record.name),
                ('id', '!=', record.id)
            ], limit=1)
            if existing_name:
                raise ValidationError(_("The location name '%s' must be unique.") % record.name)

            # check code uniquene
            existing_code = self.search([
                ('code', '=', record.code),
                ('id', '!=', record.id)
            ], limit=1)
            if existing_code:
                raise ValidationError(_("The location code '%s' must be unique.") % record.code)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class TrainingRegistration(models.Model):
    _name = 'training.registration'
    _description = 'Registration model'

    name = fields.Char(
        string='Serial Number',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('New')
    )
    #trainee name(list of employees)
    course_id = fields.Many2one(
        'training.course',
        string='Courses',
    )
    #course description
    course_description = fields.Text(
        string='Course Description',
        compute='_get_course_data'
    )
    #teacher name
    #start date
    #end date
    #number of days
    #start time
    #end time
    #room names
    #room location
    
    # Sequence generation
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('training.registration.sequence') or _('New')
        return super(TrainingRegistration, self).create(vals)
    
    #compute from course
    @api.depends('course_id')
    def _get_course_data(self):
        for record in self:
            if record.course_id:
                self.course_description = self.course_id.description
            else:
                self.course_description = ''



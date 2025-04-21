from odoo import models, fields, api, _

class TrainingRegistration(models.Model):
    _name = 'training.registration'
    _description = 'Registration model'

    serial_number = fields.Char( 
        string='Serial Number',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('New')
    )
    course_id = fields.Many2one('training.course',string="Course",required=True,ondelete='cascade')
    trainee_id = fields.Many2one('hr.employee',string="Trainee",required=True,ondelete='cascade')
    # compute fields
    course_description = fields.Text(string="Course Description",related='course_id.description')
    teacher_id = fields.Many2one(
        'hr.employee',
        string='Teacher Name',
        related='course_id.teacher_id',
        store=True,
        readonly=True
    )
    start_date = fields.Date(string='Start Date',related='course_id.start_date')
    end_date = fields.Date(string='End Date',related='course_id.end_date')
    start_time = fields.Selection(string='Start Time',related="course_id.start_time")
    end_time = fields.Selection(string='End Time',related='course_id.end_time')
    room_ids = fields.Many2many('training.room', string='Rooms',related='course_id.room_ids')
    location_ids = fields.Many2many(
        'training.location',
        string='Locations',
        compute='_compute_locations',
        store=False
    )

    #sequence function
    @api.model
    def create(self,vals):
        if vals.get('serial_number',_('New')) == _('New'):
            vals['serial_number'] = self.env['ir.sequence'].next_by_code('training.registration.sequence') or _('New')
        result = super(TrainingRegistration,self).create(vals)
        return result

    @api.depends('room_ids')
    def _compute_locations(self):
        for rec in self:
            locations = rec.room_ids.mapped('location_id')
            rec.location_ids = locations
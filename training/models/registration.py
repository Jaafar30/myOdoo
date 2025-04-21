from odoo import models, fields, api, _

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
    course_id = fields.Many2one(
        'training.course',
        string='Courses',
    )
    
    trainee_ids = fields.Many2many(
        'hr.employee',  # Model you're relating to
        string='Trainees',  # Label for the field
        relation='course_trainees',  # Custom table name
        
    )
    course_description = fields.Text(
        string='Course Description',
        related='course_id.description'
    )
    teacher_id = fields.Many2one(
        'hr.employee',
        string='Teacher Name',
        related='course_id.teacher_id',
        store=True,
        readonly=True
    )
    start_date = fields.Date(
        string='Start Date',
        related='course_id.start_date'
    )
    end_date = fields.Date(
        string='End Date',
        related='course_id.end_date'
    )
    number_of_days = fields.Integer(
        string='Number Of Days',
        related='course_id.number_of_days'
    )
    start_time = fields.Selection(
        string='Start Time',
        related='course_id.start_time'    
    )
    end_time = fields.Selection(
        string='End Time',
        related='course_id.end_time'
    )
    room_ids = fields.Many2many(
        'training.room',
        string='Rooms',
        related='course_id.room_ids',
        readonly=True
    )
    location_ids = fields.Many2many(
        'training.location',
        string='Locations',
        compute='_compute_locations',
        store=False
    )

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('training.registration.sequence') or _('New')
        return super(TrainingRegistration, self).create(vals)

    @api.depends('room_ids')
    def _compute_locations(self):
        for rec in self:
            locations = rec.room_ids.mapped('location_id')
            rec.location_ids = locations

    @api.depends('course_id')
    def _compute_trainee_ids(self):
        for rec in self:
            teacher = rec.course_id.teacher_id
            domain = [('id', '!=', teacher.id)] if teacher else []
            rec.trainee_ids = self.env['hr.employee'].search(domain)



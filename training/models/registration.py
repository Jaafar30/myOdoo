from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class TrainingRegistration(models.Model):
    _name = 'training.registration'
    _description = 'Registration model'

    name = fields.Char(
        compute='_compute_name',
        store=True,
        string="Registration Name"
    )
    serial_number = fields.Char( 
        string='Serial Number',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('New')
    )
    course_id = fields.Many2one(
        'training.course',
        string="Course",
        required=True,
        ondelete='cascade',
        domain=lambda self: self._get_course_domain()
    )
    trainee_id = fields.Many2one(
        'hr.employee',
        string="Trainee",
        required=True,
        ondelete='cascade',
        domain="[('id', '!=', teacher_id)]",
        default=lambda self: self._get_default_trainee()
    )
    # Related & computed fields
    course_description = fields.Text(string="Course Description", related='course_id.description')
    teacher_id = fields.Many2one(
        'hr.employee',
        string='Teacher Name',
        related='course_id.teacher_id',
        store=True,
        readonly=True,
    )
    number_of_days = fields.Integer(string='Number Of Days', related='course_id.number_of_days')
    start_date = fields.Date(string='Start Date', related='course_id.start_date')
    end_date = fields.Date(string='End Date', related='course_id.end_date')
    start_time = fields.Selection(string='Start Time', related="course_id.start_time")
    end_time = fields.Selection(string='End Time', related='course_id.end_time')
    room_ids = fields.Many2many('training.room', string='Rooms', related='course_id.room_ids')
    location_ids = fields.Many2many(
        'training.location',
        string='Locations',
        compute='_compute_locations',
        store=False
    )
    status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', required=True,readonly=True)

    # sequence generation
    @api.model
    def create(self, vals):
        if vals.get('serial_number', _('New')) == _('New'):
            vals['serial_number'] = self.env['ir.sequence'].next_by_code('training.registration.sequence') or _('New')
        return super(TrainingRegistration, self).create(vals)

    # locations based on rooms
    @api.depends('room_ids')
    def _compute_locations(self):
        for rec in self:
            rec.location_ids = rec.room_ids.mapped('location_id')

    @api.model
    def _get_default_trainee(self):
        """Set default trainee based on user group."""
        user = self.env.user
        if user.has_group('training.group_training_hr'):
            return False  # HR group remains unaffected
        else:
            # For Requester or other groups, set the user's employee ID as default
            employee = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
            return employee.id if employee else False

    @api.model
    def _get_course_domain(self):
        """Filter courses to exclude those where the user is the teacher."""
        user = self.env.user
        employee = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        if employee:
            return [('teacher_id', '!=', employee.id)]
        return []

    @api.depends('course_id', 'trainee_id')
    def _compute_name(self):
        """Compute the name field as 'Course Name - Trainee Name'."""
        for rec in self:
            course_name = rec.course_id.name if rec.course_id else ''
            trainee_name = rec.trainee_id.name if rec.trainee_id else ''
            rec.name = f"{course_name} - {trainee_name}" if course_name and trainee_name else ''

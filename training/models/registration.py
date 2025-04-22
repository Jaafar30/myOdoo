from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

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

    today_date = fields.Date(string="Today's Date", default=lambda self: fields.Date.today())


    # sequence generation
    @api.model
    def create(self, vals):
        """Override create to enforce conditions for registration."""
        # Check if the user has been employed for at least 6 months
        user = self.env.user
        employee = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        if employee and employee.create_date:
            hire_date = fields.Datetime.from_string(employee.create_date).date()
            six_months_ago = datetime.today().date() - timedelta(days=6 * 30)  # Approximate 6 months
            if hire_date > six_months_ago:
                raise ValidationError(_("You must complete at least 6 months in the company to register for a course."))

        # Check if the user already has a request in the same year with status 'approved' or 'draft'
        if employee:
            current_year = datetime.today().year
            existing_request = self.env['training.registration'].search([
                ('trainee_id', '=', employee.id),
                ('status', 'in', ['draft', 'approved']),
                ('create_date', '>=', f'{current_year}-01-01'),
                ('create_date', '<=', f'{current_year}-12-31')
            ], limit=1)
            if existing_request:
                raise ValidationError(_("You already have a registration request with status 'draft' or 'approved' in the same year."))

        # Check the maximum number of requests condition
        course_id = vals.get('course_id')
        if course_id:
            # Count the number of draft and approved registrations for the course
            registration_count = self.env['training.registration'].search_count([
                ('course_id', '=', course_id),
                ('status', 'in', ['draft', 'approved'])
            ])
            # Get the maximum number of requests allowed for the course
            course = self.env['training.course'].browse(course_id)
            if registration_count >= course.available_seats:
                raise ValidationError(_("The maximum number of requests for the course '%s' has been reached.") % course.name)

        # Generate serial number if not provided
        if vals.get('serial_number', _('New')) == _('New'):
            vals['serial_number'] = self.env['ir.sequence'].next_by_code('training.registration.sequence') or _('New')

        return super(TrainingRegistration, self).create(vals)
    
    gender = fields.Char(sudo=True, string="Gender", compute='get_gender', store=True)

    @api.depends('trainee_id')  # Only include this if trainee_id should actually affect gender
    def get_gender(self):
        for record in self:
            # Get the logged-in user with sudo if needed
            user = self.env.user
            # If user is linked to an employee, get gender
            gender = user.employee_ids.gender if user.employee_ids else False
            record.gender = gender

    # locations based on rooms
    @api.depends('room_ids')
    def _compute_locations(self):
        for rec in self:
            rec.location_ids = rec.room_ids.mapped('location_id')

    @api.model
    def _get_default_trainee(self):
        """Set default trainee."""
        user = self.env.user
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

    def confirm_registration(self):
        """Confirm the registration."""
        for rec in self:
            if rec.status == 'draft':
                rec.status = 'approved'
            else:
                raise ValidationError(_("You cannot confirm a registration that is not in draft status."))

    def reject_registration(self):
        """Reject the registration."""
        for rec in self:
            if rec.status == 'draft':
                rec.status = 'rejected'
            else:
                raise ValidationError(_("You cannot reject a registration that is not in draft status."))
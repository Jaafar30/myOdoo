from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

class TrainingCourse(models.Model):
    _name = 'training.course'
    _description = 'Course model'

    serial_number = fields.Char( 
        string='Serial Number',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('New')
    )
    name = fields.Char(string='Course Name',required=True)
    description = fields.Text(string='Course Description')
    teacher_id = fields.Many2one(
        'hr.employee',
        string='Course Teacher',
        required=True,
        domain=lambda self: self._get_teacher_domain()
    )
    start_date = fields.Date(string='Start Date',default=fields.Date.today,required=True)
    end_date = fields.Date(string='End Date',defaul=fields.Date.today,required=True)
    number_of_days = fields.Integer(compute='_compute_number_of_days',string='Number Of Days',store=True)
    start_time = fields.Selection(
        [
            ('1', "1 AM"), ('2', "2 AM"), ('3', "3 AM"), ('4', "4 AM"),
            ('5', "5 AM"), ('6', "6 AM"), ('7', "7 AM"), ('8', "8 AM"),
            ('9', "9 AM"), ('10', "10 AM"), ('11', "11 AM"), ('12', "12 PM"),
            ('13', "1 PM"), ('14', "2 PM"), ('15', "3 PM"), ('16', "4 PM"),
            ('17', "5 PM"), ('18', "6 PM"), ('19', "7 PM"), ('20', "8 PM"),
            ('21', "9 PM"), ('22', "10 PM"), ('23', "11 PM"), ('0', "12 AM")
        ], 
        string='Start Time',
        required=True
    )
    end_time = fields.Selection(
        [
            ('1', "1 AM"), ('2', "2 AM"), ('3', "3 AM"), ('4', "4 AM"),
            ('5', "5 AM"), ('6', "6 AM"), ('7', "7 AM"), ('8', "8 AM"),
            ('9', "9 AM"), ('10', "10 AM"), ('11', "11 AM"), ('12', "12 PM"),
            ('13', "1 PM"), ('14', "2 PM"), ('15', "3 PM"), ('16', "4 PM"),
            ('17', "5 PM"), ('18', "6 PM"), ('19', "7 PM"), ('20', "8 PM"),
            ('21', "9 PM"), ('22', "10 PM"), ('23', "11 PM"), ('0', "12 AM")
        ],
        string='End Time',
        required=True
    )
    room_ids = fields.Many2many('training.room', string='Rooms',required=True)
    available_seats = fields.Integer(string='Available Seats',required=True,default=30)
    target_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('both', 'Both'),
    ], string='Target gender',required=True,default='both')
    deadline = fields.Date('Deadline',required=True)
    registration_ids = fields.One2many(
        'training.registration',  # Related model
        'course_id',              # Field in the registration model that links to this course
        string='Registrations'
    )
    
    
    #sequence function
    @api.model
    def create(self,vals):
        if vals.get('serial_number',_('New')) == _('New'):
            vals['serial_number'] = self.env['ir.sequence'].next_by_code('training.course.sequence') or _('New')
        result = super(TrainingCourse,self).create(vals)
        return result

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            existing_name = self.search([('name','=',record.name),('id','!=',record.id)],limit=1)
            if existing_name :
                raise ValidationError(_("The Course name '%s' must be unique.") % record.name)

    @api.constrains('start_date','end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date > record.end_date:
                raise ValidationError(_('The Starting Date Cannot Be After The End Date'))

    

    # compute number of days required
    @api.depends('start_date', 'end_date')
    def _compute_number_of_days(self):
        for record in self:
            if record.start_date and record.end_date:
                duration = (record.end_date - record.start_date).days + 1
                record.number_of_days = duration if duration > 0 else 0
            else:
                record.number_of_days = 0


    @api.constrains('start_time', 'end_time')
    def _check_time_order(self):
        for record in self:
            if record.start_time and record.end_time:
                start = int(record.start_time)
                end = int(record.end_time)
                if start >= end:
                    raise ValidationError(_("Start Time must be before End Time."))

    
    @api.constrains('deadline')
    def _check_deadline(self):
        for record in self:
            if record.deadline is not None:
                if record.start_date <= record.deadline:
                    raise ValidationError(_("The deadline must be before the Start Date"))

    @api.constrains('room_ids')
    def _check_rooms_required(self):
        for record in self:
            if not record.room_ids:
                raise ValidationError(_("At least one Room must be selected for the course."))

    @api.constrains('available_seats')
    def _check_available_seats(self):
        for record in self:
            if record.available_seats <= 0:
                raise ValidationError(_("The number of available seats must be greater than 0."))

    def _get_teacher_domain(self):
        teacher_group = self.env.ref('training.group_training_teacher')
        users_in_group = self.env['res.users'].search([
            ('groups_id', 'in', teacher_group.id)
        ])
        return [('user_id', 'in', users_in_group.ids)]



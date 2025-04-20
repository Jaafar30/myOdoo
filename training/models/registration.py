from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

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

    trainee_id = fields.Many2one(
        'hr.employee',
        string='Trainee',
        required=True
    )

    course_id = fields.Many2one(
        'training.course',
        string='Course',
        required=True,
        domain=[('deadline', '>=', fields.Date.today())]
    )

    course_name = fields.Char(
        string='Course Name',
        readonly=True
    )

    course_description = fields.Text(
        string='Course Description',
        readonly=True
    )

    teacher_name = fields.Char(
        string='Teacher Name',
        readonly=True
    )

    start_date = fields.Date(
        string='Start Date',
        readonly=True
    )

    end_date = fields.Date(
        string='End Date',
        readonly=True
    )

    number_of_days = fields.Integer(
        string='Number Of Days',
        readonly=True
    )

    start_time = fields.Char(
        string='Start Time',
        readonly=True
    )

    end_time = fields.Char(
        string='End Time',
        readonly=True
    )

    room_name = fields.Char(
        string='Room Name',
        readonly=True
    )

    course_location = fields.Char(
        string='Course Location',
        readonly=True
    )

    # Sequence generation
    @api.model
    def create(self, vals):
        if vals.get('serial_number', _('New')) == _('New'):
            vals['serial_number'] = self.env['ir.sequence'].next_by_code('training.registration.sequence') or _('New')
        return super(TrainingRegistration, self).create(vals)

    # Onchange method to auto-fill course-related fields and filter trainees by gender
    @api.onchange('course_id')
    def _onchange_course_id(self):
        for rec in self:
            course = rec.course_id
            if course:
                # Populate course-related fields
                rec.course_name = course.name
                rec.course_description = course.description
                rec.teacher_name = course.teacher_id.name
                rec.start_date = course.start_date
                rec.end_date = course.end_date
                rec.number_of_days = course.number_of_days
                rec.start_time = dict(course._fields['start_time'].selection).get(course.start_time)
                rec.end_time = dict(course._fields['end_time'].selection).get(course.end_time)
                rec.room_name = ', '.join(course.room_ids.mapped('name'))
                rec.course_location = ', '.join(course.room_ids.mapped('location_id.name'))

                # Filter trainees by course target gender
                domain = [('is_teacher', '=', False)]
                if course.target_gender != 'both':
                    domain.append(('gender', '=', course.target_gender))

                return {
                    'domain': {
                        'trainee_id': domain
                    }
                }

        # Fallback
        return {
            'domain': {
                'trainee_id': [('is_teacher', '=', False)]
            }
        }


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date

class TrainingTeacher(models.Model):
    _name = 'training.teacher'
    _description = 'Teacher Model'

    name = fields.Char(string='Name', compute='_make_name', store=True)

    teacher_id = fields.Many2one(
        'hr.employee',
        string='Teacher',
        domain=[('is_teacher', '=', True)],
        required=True
    )

    course_id = fields.Many2one(
        'training.course',
        string='Course',
        domain=lambda self: [('id', 'not in', self.env['training.teacher'].search([]).mapped('course_id.id'))],
        required=True
    )

    @api.depends('teacher_id', 'course_id')
    def _make_name(self):
        for record in self:
            if record.teacher_id and record.course_id:
                record.name = f"{record.course_id.name} - {record.teacher_id.display_name}"
            else:
                record.name = False
    




# domain=lambda self: [('id', 'not in', self.env['training.teacher'].search([]).mapped('course_id.id'))],
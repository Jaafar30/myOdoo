from odoo import models,fields,api,_


class JaffarCourse(models.Model):
    _name = 'jaffar_module.course'
    _description = 'Course'

    serial_number = fields.Char(
        string='Serial Number',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('New')
    )
    name = fields.Char(string='Course Name')
    # description = fields.Text()
    # teacher_id = fields.Many2one()
    # start_date = fields.Date()
    # end_date = fields.Date()
    # number_of_days = fields.Integer()
    # time = fields.Datetime()
    # room_id = fields.Many2one()
    # seats = fields.Integer('seats')
    # target = fields.Selection([
    #     ('male', 'Male'),
    #     ('female', 'Female'),
    #     ('both', 'Both'),
    # ], string='target')
    # deadline = fields.Date()

    @api.model
    def create(self,vals):
        if vals.get('serial_number',_('New')) == _('New'):
            vals['serial_number'] = self.env['ir.sequence'].next_by_code('jaffar.module.course.sequence') or _('New')
        result = super(JaffarCourse,self).create(vals)
        return result
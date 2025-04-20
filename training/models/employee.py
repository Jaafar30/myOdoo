from odoo import models, fields

class TrainingEmployee(models.Model):
    _inherit = 'hr.employee'

    is_teacher = fields.Boolean(string='Is Teacher',default=False)

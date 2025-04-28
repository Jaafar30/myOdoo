from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PresalesMatrix(models.Model):
    _name = 'presales.matrix'
    _description = 'CRM Presales Matrix'
    
    # 1
    fit_to_is_business = fields.Selection([
        ('fit', 'Fit'),
        ('not_fit', 'Not Fit'),
    ], string='Fit to IS Business')

    # 2
    region_id = fields.Many2one('account.region', string='Region')
    town_name = fields.Char()

    # 3
    early_engagement = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Early Engagement')

    # 4
    estimated_budget = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Do we have an estimated budget')
    esstimated_budget_specify = fields.Text()

    # 5
    invitation = fields.Selection([
        ('direct_invitation', 'Direct Invitation'),
        ('public', 'Public'),
    ], string='Direct / Public Invitation')

    # 6
    protected_vendor = fields.Selection([
        ('protected', 'Protected'),
        ('fair_price_to_all', 'Fair Price to All'),
    ], string='Are we Protected by vendor')
    protected_technology = fields.Text()

    # 7
    is_relation_with_vendor = fields.Selection([
        ('strategic', 'Strategic'),
        ('adequate', 'Adequate'),
        ('firsttime', 'FirstTime'),
        ('poor', 'Poor'),
    ], string='Is relation with vendor/s')
    vendor_name = fields.Char()

    # 8
    high_competition = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='High Competition')
    high_competition_specify = fields.Text()

    # 9
    is_relation_with_customer = fields.Selection([
        ('good', 'Good'),
        ('average', 'Average'),
        ('firsttime', 'FirstTime'),
        ('poor', 'Poor'),
    ], string='IS relation with the customer')
    customer_partner = fields.Char()

    # 10
    visibility = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Do we have good visibility / Insight')

    # 11
    clear_customer_needs = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ])

    # 12
    overall_risk = fields.Selection([
        ('highrisk', 'HighRisk'),
        ('midrisk', 'MidRisk'),
        ('lowrisk', 'LowRisk'),
        ('norisk', 'NoRisk'),
    ])

    # 13
    professional_service = fields.Selection([
        ('vendor', 'Vendor'),
        ('is', 'IS'),
        ('3rd_party', '3rd Party'),
    ], string='Professional Service')
    majority_or_minority_service = fields.Text()

    # 14
    is_service = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='IS Service (MSS/Advisory)')

    # 15
    opportunity_exist = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Opportunity Exist on CRM')
    presales_request_no = fields.Many2one('crm.lead')

    def _check_and_nullify_fields(self, vals):
        """
        This function set dependent fields to None if their corresponding conditions are not met.
        """
        # dependent fields and their conditions
        # main_field - dependent_field - condition_value
        field_conditions = [
            ('estimated_budget', 'esstimated_budget_specify', 'yes'),
            ('high_competition', 'high_competition_specify', 'yes'),
            ('opportunity_exist', 'presales_request_no', 'yes'),
        ]

        for condition_field, target_field, condition_value in field_conditions:
            if vals.get(condition_field) != condition_value:
                vals[target_field] = None

        return vals

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals = self._check_and_nullify_fields(vals)
        return super().create(vals_list)

    def write(self, vals):
        vals = self._check_and_nullify_fields(vals)
        return super().write(vals)
        
        

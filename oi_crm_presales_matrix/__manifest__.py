# -*- coding: utf-8 -*-
{
    'name': "CRM Presales Matrix",

    'summary': "",

    'web_icon':'training/static/description/icon.png',

    'description': """
        
    """,

    'author': "Jaffar",
    
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'base',
        'crm',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/presales.xml',
        'views/crm_lead.xml',
        'views/menu.xml'
    ],
}


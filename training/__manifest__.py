# -*- coding: utf-8 -*-
{
    'name': "Training",

    'summary': "Training for employees",

    'web_icon':'training/static/description/icon.png',

    'description': """
        Training for employees ...
    """,

    'author': "Jaffar",
    
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'base',
        'hr',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/course_seq.xml',
        'views/my_courses_view.xml',
        'views/registration_seq.xml',
        'views/room_view.xml',
        'views/location_view.xml',
        'views/course_view.xml',
        'views/registration_view.xml',
        'views/teacher_view.xml',
        'views/menu.xml'
    ],
}


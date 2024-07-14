{
    'name': 'Student Management',
    'version': '1.0',
    'summary': 'Module to manage student records',
    'description': 'Module to manage student records with unique sequence numbers, automatic age calculation, logging, and access rights.',
    'author': 'Jivika Khadka',
    'category': 'Education',
    'data': [
        'security/student_security.xml',
        'security/ir.model.access.csv',
        'views/student_views.xml',
        'views/student_id_card_template.xml',
        'data/student_sequence.xml',
    ],
    'installable': True,
    'application': True,
    'auto_installable':False,
}

# -*- coding: utf-8 -*-
{
    'name': 'Todo List',
    'version': '1.0',
    'summary': 'Todo List System',
    'sequence': 10,
    'description': """
Todo List System
====================
This Todo List system allows users to create, edit, and manage tasks effectively. 
Users can assign statuses such as 'To Do', 'In Progress', and 'Done', set deadlines, and track task completion. 
The system ensures users provide complete information and follow logical workflows. 
It's designed to help improve productivity and task organization in daily routines.
""",
    'category': 'TodoList/TodoList',
    'website': 'https://todo_list.com',
    'author': 'Phonlakit',
    'depends': [],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/root_view.xml',
        'views/todo_view.xml',
        'views/menu_view.xml',
        'data/tag_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'assets': {},
    'license': 'LGPL-3',
}

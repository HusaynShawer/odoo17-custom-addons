{
    'name': 'To Do App',
    'version': '17.0.0.1.0',
    'author': 'husayn_shawer',
    'category': 'Uncategorized',
    'summary': 'To Do App',
    'depends':['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        "views/base_menu.xml",
        "views/todo_task_view.xml",
    ],
    'application': True,
}
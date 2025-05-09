from odoo import models, fields

class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Todo Task'

    # region : Main fields
    name = fields.Char(required=True, string="Task Name")
    description = fields.Text()
    is_done = fields.Boolean(string="Complete")
    todo_id = fields.Many2one('todo.list', string="Todo List", ondelete='cascade')
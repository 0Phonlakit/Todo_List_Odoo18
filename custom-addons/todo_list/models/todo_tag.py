from odoo import models, fields

class TodoTag(models.Model):
    _name = 'todo.tag'
    _description = 'Todo Tag'

    # region : Main fields
    name = fields.Char(required=True, string="Tag Name")
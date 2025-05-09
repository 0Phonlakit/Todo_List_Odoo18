from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class TodoList(models.Model):
    _name = "todo.list"
    _description = "Todo List"

    # region : Main fields.
    name = fields.Char(required=True, string="Title")
    tag_ids = fields.Many2many('todo.tag', string="Tags")
    start_date = fields.Datetime(required=True, string="Start Date")
    end_date = fields.Datetime(required=True, string="End Date")
    state = fields.Selection([ ('draft', 'Draft'),
                               ('in_progress', 'In Progress'),
                               ('complete', 'Complete')],
                               default='draft', string="Status", tracking=True)
    participants_ids = fields.Many2many( 'res.users',
                                         'todo_user_rel',
                                         'todo_id',
                                         'user_id',
                                         string="Participants")
    task_ids = fields.One2many('todo.task', 'todo_id', string="Todo Tasks")

    # region : Computed helper fields.
    button_section = fields.Selection( selection=[('tasks', 'Tasks'),
                                                  ('attendees', 'Attendees')],
                                                  default='tasks', string="Show Section")
    start_draft = fields.Boolean(compute='start_drafts')
    mark_complete = fields.Boolean(compute='mark_completes')

    # Change status from 'draft' to 'in_progress' if all required fields are filled and valid
    def start_progress(self):
        for rec in self:
            if rec.state != 'draft':
                continue
            if not rec.name or not rec.start_date or not rec.end_date:
                raise UserError("Please fill in all required fields before proceeding.")
            if rec.end_date < rec.start_date:
                raise UserError("The end date must be later than the start date.")
            rec.state = 'in_progress'
    
    # Change status from 'in_progress' to 'complete' if at least one task is present
    def end_progress(self):
        for rec in self:
            if rec.state != 'in_progress':
                raise UserError("You can only mark a task as 'Done' when its status is 'In Progress'.")
            if not rec.task_ids:
                raise UserError("Please add at least one Todo task before clicking Done.")
            rec.state = 'complete'

    # Compute boolean to control visibility of the Start button
    @api.depends('state', 'name', 'start_date', 'end_date')
    def start_drafts(self):
        for rec in self:
            rec.start_draft = ( rec.state == 'draft' 
                             and rec.name
                             and rec.start_date
                             and rec.end_date
                             and rec.end_date >= rec.start_date)

    # Compute boolean to control visibility of the Done button
    @api.depends('state', 'task_ids.is_done')
    def mark_completes(self):
        for rec in self:
            rec.mark_complete = rec.state == 'in_progress' and len(rec.task_ids) > 0

    # Raise error if end_date is earlier than start_date
    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError("The end date must be later than the start date.")

    # Set UI to show the Tasks section     
    def show_tasks(self):
        for rec in self:
            rec.button_section = 'tasks'
    
    # Set UI to show the Attendees section
    def show_attendees(self):
        for rec in self:
            rec.button_section = 'attendees'
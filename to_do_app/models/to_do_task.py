from jinja2 import defaults

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ToDoTask(models.Model):
    _name = "todo.task"
    _description = "To Do App"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char('Task Name',required=True)
    due_date = fields.Datetime('Due Date',required=True)
    description = fields.Text('Description',required=True)
    assign_to_id = fields.Many2one('res.partner',string='Assigned To',required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('complete', 'Complete'),
    ], string='Status', default='new', required=True)

    estimated_time = fields.Float('Estimated Time',required=True)
    lines_ids = fields.One2many('timesheat.task','todo_tasks_id')
    active = fields.Boolean('Active', default=True)

    def action_new(self):
        for record in self:
            record.state = 'new'
    def action_in_progress(self):
        for record in self:
            record.state = 'in_progress'
    def action_complete(self):
        for record in self:
            record.state = 'complete'


class TimeSheat(models.Model):
    _name = "timesheat.task"
    _description = "Time Heat"
    _rec_name = "task1"

    todo_tasks_id = fields.Many2one('todo.task')
    task1 = fields.Char('Task 1')
    task1_time = fields.Float('Task 1 Time')
    all_time = fields.Float('All Time',compute='clack_all_time',store =True)

    @api.depends('task1_time','todo_tasks_id.lines_ids.task1_time')
    def clack_all_time(self):
        for record in self:
            lines = record.todo_tasks_id.lines_ids
            record.all_time = sum(lines.mapped('task1_time'))
        print ("the all task time",record.all_time)

    @api.constrains('task1_time','todo_tasks_id')
    @api.constrains('task1_time', 'todo_tasks_id')
    def _cheat_all_time(self):
        for record in self:
            task = record.todo_tasks_id
            if not task:
                continue
            total_time = sum(task.lines_ids.mapped('task1_time'))
            if total_time > task.estimated_time:
                raise ValidationError(f'Task time is {total_time} must be less than estimated time{task.estimated_time}')

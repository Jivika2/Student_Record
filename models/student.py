from odoo import models, fields, api
from datetime import date

class Student(models.Model):
    _name = 'student.management'
    _inherit = ['mail.thread', 'mail.activity.mixin','website.published.mixin']
    _description = 'Student Management'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Char(string='Student Number', required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')
    birthdate = fields.Date(string='Birth Date', required=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', required=True)
    address = fields.Text(string='Address')
    student_id_card = fields.Binary(string='Student ID Card', attachment=True)
    department_id = fields.Many2one('student.department', string='Department')
    description = fields.Text(string='Description')
    history_count = fields.Integer(string='History Count', compute='_compute_history_count')

   
    @api.model
    def create(self, vals):
        if 'student_id' in vals and 'field_name' in vals and 'new_value' in vals:
            student = self.env['student.management'].browse(vals['student_id'])
            field_name = vals['field_name']
            
            # Debugging output
            print(f"Student ID: {vals['student_id']}")
            print(f"Field Name: {field_name}")
            print(f"Fields on student.management: {student._fields.keys()}")

            if field_name in student._fields:
                old_value = student.mapped(field_name)[0]
                vals['old_value'] = old_value
            else:
                raise ValueError(f"Field '{field_name}' does not exist on student.management model")
        
        return super(StudentHistory, self).create(vals)

    @api.depends('birthdate')
    def _compute_age(self):
        for student in self:
            if student.birthdate:
                today = date.today()
                student.age = today.year - student.birthdate.year - ((today.month, today.day) < (student.birthdate.month, student.birthdate.day))

    def write(self, vals):
        return super(Student, self).write(vals)

    def unlink(self):
        return super(Student, self).unlink()
    
    def _compute_history_count(self):
        for student in self:
            student.history_count = self.env['student.record.history'].search_count([('student_id', '=', student.id)])

    
    
    def action_view_history(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f"{self.name} - History",
            'domain': [('student_id', '=', self.id)],
            'view_mode': 'tree',
            'res_model': 'student.record.history'
        }

    
    def print_student_id_card(self):
        return self.env.ref('student_record.student_id_card_report_action').report_action(self)


class StudentHistory(models.Model):
    _name = 'student.record.history'
    _description = 'Student Record History'
    
    student_id = fields.Many2one('student.management', string='Student', required=True)
    field_name = fields.Char(string='Field Name')
    old_value = fields.Char(string='Old Value')
    new_value = fields.Char(string='New Value')
    change_date = fields.Datetime(string='Change Date', default=fields.Datetime.now)
    
    @api.model
    def create(self, vals):
        if 'student_id' in vals and 'field_name' in vals and 'new_value' in vals:
            old_value = self.env['student.management'].browse(vals['student_id']).mapped(vals['field_name'])[0]
            vals['old_value'] = old_value
        return super(StudentHistory, self).create(vals)


class StudentDepartment(models.Model):
    _name = 'student.department'
    _description = 'Student Department'

    name = fields.Char(string='Department Name', required=True)
    code = fields.Char(string='Department Code', required=True)
    manager_id = fields.Many2one('res.users', string='Department Manager')
    student_ids = fields.One2many('student.management', 'department_id', string='Students')
    description = fields.Text(string='Description')

from odoo import models, fields, api
from datetime import date
import logging

_logger = logging.getLogger(__name__)

class Student(models.Model):
    _name = 'student.management'
    _description = 'Student Management'
    _rec_name = 'name'
    _order = 'sequence'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Char(string='Student Number', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    birthdate = fields.Date(string='Birth Date', required=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', required=True)
    address = fields.Text(string='Address')
    student_id_card = fields.Binary(string='Student ID Card')

    @api.model
    def create(self, vals):
        if vals.get('sequence', ('New')) == ('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('student.management') or ('New')
        record = super(Student, self).create(vals)
        _logger.info(f"Created student record: {record.name}")
        return record

    @api.depends('birthdate')
    def _compute_age(self):
        for student in self:
            if student.birthdate:
                today = date.today()
                student.age = today.year - student.birthdate.year - ((today.month, today.day) < (student.birthdate.month, student.birthdate.day))
                _logger.info(f"Calculated age for student {student.name}: {student.age}")

    def write(self, vals):
        for record in self:
            changes = []
            for field, value in vals.items():
                old_value = record[field]
                if old_value != value:
                    changes.append(f"{field}: {old_value} -> {value}")
            _logger.info(f"Updating student record {record.name}: {', '.join(changes)}")
        return super(Student, self).write(vals)

    def unlink(self):
        for record in self:
            _logger.info(f"Deleting student record: {record.name}")
        return super(Student, self).unlink()

    def print_student_id_card(self):
        return self.env.ref('student_management.student_id_card_report').report_action(self)

class StudentHistory(models.Model):
    _name = 'student.record.history'
    _description = 'Student Record History'
    
    student_id = fields.Many2one('student.management', string='Student', required=True)
    field_name = fields.Char(string='Field Name', required=True)
    old_value = fields.Char(string='Old Value')
    new_value = fields.Char(string='New Value')
    change_date = fields.Datetime(string='Change Date', default=fields.Datetime.now)
    
    @api.model
    def create(self, vals):
        if 'student_id' in vals and 'field_name' in vals and 'new_value' in vals:
            old_value = self.env['student.record'].browse(vals['student_id']).mapped(vals['field_name'])[0]
            vals['old_value'] = old_value
        return super(StudentHistory, self).create(vals)
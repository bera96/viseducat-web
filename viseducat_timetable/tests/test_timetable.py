
from logging import info
import time
from .test_timetable_common import TestTimetableCommon


class TestFacultySession(TestTimetableCommon):

    def setUp(self):
        super(TestFacultySession, self).setUp()

    def test_case_faculty(self):
        faculty = self.vm_faculty.search([])
        if not faculty:
            raise AssertionError(
                'Error in data, please check for faculty session details')
        info('  Details Of Faculty Sessions:.....')
        for record in faculty:
            info('      Sessions : %s' % record.session_ids.name)


class TestTimetable(TestTimetableCommon):

    def setUp(self):
        super(TestTimetable, self).setUp()

    def test_case_timetable(self):
        session = self.vm_session.create({
            'timing_id': self.env.ref('viseducat_timetable.vm_timing_1').id,
            'start_datetime': time.strftime('%Y-%m-10 11:00'),
            'end_datetime': time.strftime('%Y-%m-10 12:00'),
            'course_id': self.env.ref('viseducat_core.vm_course_2').id,
            'faculty_id': self.env.ref('viseducat_core.vm_faculty_1').id,
            'batch_id': self.env.ref('viseducat_core.vm_batch_1').id,
            'subject_id': self.env.ref('viseducat_core.vm_subject_1').id
        })
        info('  Details Of Timetable Sessions:.....')
        session._compute_day()
        session._compute_name()
        session._compute_batch_users()
        session._check_date_time()
        session.onchange_course()
        session.notify_user()
        session.get_subject()
        session.get_import_templates()
        session.lecture_draft()
        session.lecture_confirm()
        session.lecture_done()
        session.lecture_cancel()


class TestGenerateTimetable(TestTimetableCommon):

    def setUp(self):
        super(TestGenerateTimetable, self).setUp()

    def test_case_wizard_generate_timetable(self):
        wizard = self.generate_timetable.create({
            'course_id': self.env.ref('viseducat_core.vm_course_2').id,
            'batch_id': self.env.ref('viseducat_core.vm_batch_1').id,
            'start_date': time.strftime('%Y-%m-01'),
            'end_date':  time.strftime('%Y-%m-01')
        })
        info('  Details Of Sessions:.....')
        wizard.act_gen_time_table()
        wizard.check_dates()
        wizard.onchange_course()


class TestWizardSession(TestTimetableCommon):

    def setUp(self):
        super(TestWizardSession, self).setUp()

    def test_case_wizard_session(self):
        wizard = self.generate_timetable.create({
            'course_id': self.env.ref('viseducat_core.vm_course_2').id,
            'batch_id': self.env.ref('viseducat_core.vm_batch_1').id,
            'start_date': time.strftime('%Y-%m-01'),
            'end_date': time.strftime('%Y-%m-01')
        })
        session = self.wizard_session.create({
            'gen_time_table': wizard.id,
            'faculty_id': self.env.ref('viseducat_core.vm_faculty_1').id,
            'subject_id': self.env.ref('viseducat_core.vm_subject_1').id,
            'timing_id': self.env.ref('viseducat_timetable.vm_timing_1').id,
            'day': '2'
        })
        info('  Details Of Session lines:.....')
        return session


class TestTimetableReport(TestTimetableCommon):

    def setUp(self):
        super(TestTimetableReport, self).setUp()

    def test_case_wizard_timetable_report(self):
        report = self.timetable_report.create({
            'state': 'student',
            'course_id': self.env.ref('viseducat_core.vm_course_2').id,
            'batch_id': self.env.ref('viseducat_core.vm_batch_1').id,
            'start_date': time.strftime('%Y-%m-01'),
            'end_date':  time.strftime('%Y-%m-01')
        })
        info('  Details Of Timetable Report:.....')
        report._check_dates()
        report.onchange_course()
        report.gen_time_table_report()

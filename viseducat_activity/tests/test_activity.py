from logging import info

from .test_activity_common import TestActivityCommon


class TestActivity(TestActivityCommon):

    def setUp(self):
        super(TestActivity, self).setUp()

    def test_case_activity_1(self):
        activity = self.vm_activity.search([])
        if not activity:
            raise AssertionError(
                'Error in data, please check for reference ')
        info('Details of Activity')
        for record in activity:
            info('      Student : %s' % record.student_id.name)
            info('      Faculty : %s' % record.faculty_id.name)
            info('      Activity Type : %s' % record.type_id.name)
            info('      Description : %s' % record.description)
            info('      Date : %s' % record.date)


class TestActivityType(TestActivityCommon):

    def setUp(self):
        super(TestActivityType, self).setUp()

    def test_case_1_activity_type(self):
        activity_type = self.vm_activity_type.search([])
        if not activity_type:
            raise AssertionError(
                'Error in data, please check for Activity type')
        info('Details of achievement_type')
        for category in activity_type:
            info('      Activity : %s' % category.name)


class TestStudentMigrateWizard(TestActivityCommon):

    def setUp(self):
        super(TestStudentMigrateWizard, self).setUp()

    def test_case_1_student_migrate_wizard(self):
        student_migrate = self.vm_student_migrate_wizard.create({
            'course_from_id': self.env.ref('viseducat_core.vm_course_2').id,
            'course_to_id': self.env.ref('viseducat_core.vm_course_3').id,
            'batch_id': self.env.ref('viseducat_core.vm_batch_2').id,
            'student_ids': self.env.ref('viseducat_core.vm_student_7'),
        })
        student_migrate1 = self.vm_student_migrate_wizard.create({
            'course_from_id': self.env.ref('viseducat_core.vm_course_3').id,
            'course_to_id': self.env.ref('viseducat_core.vm_course_2').id,
            'batch_id': self.env.ref('viseducat_core.vm_batch_1').id,
            'student_ids': self.env.ref('viseducat_core.vm_student_8'),
        })

        student_migrate.student_migrate_forward()
        student_migrate1.onchange_course_id()

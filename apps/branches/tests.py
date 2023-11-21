"""
Module for testing branches app.
"""
from django.test import TestCase
from .models import Branch, Schedule, Workdays


class BranchTestCase(TestCase):
    """
    Class for testing branches app.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create test data.
        """
        cls.schedule = Schedule.objects.create(
            title="Test title", description="Test description"
        )
        cls.branch = Branch.objects.create(
            image="Test image",
            name_of_shop="Test name",
            schedule=cls.schedule,
            address="Test address",
            phone_number="Test phone",
            link_to_map="Test link",
        )
        cls.workdays = Workdays.objects.create(
            schedule=cls.schedule, workday=1, start_time="10:00", end_time="20:00"
        )

    def test_branch(self):
        """
        Test branch model.
        """
        self.assertEqual(self.branch.image, "Test image")
        self.assertEqual(self.branch.name_of_shop, "Test name")
        self.assertEqual(self.branch.schedule.title, "Test title")
        self.assertEqual(self.branch.schedule.description, "Test description")
        self.assertEqual(self.branch.address, "Test address")
        self.assertEqual(self.branch.phone_number, "Test phone")
        self.assertEqual(self.branch.link_to_map, "Test link")

    def test_schedule(self):
        """
        Test schedule model.
        """
        self.assertEqual(self.schedule.title, "Test title")
        self.assertEqual(self.schedule.description, "Test description")

    def test_workdays(self):
        """
        Test workdays model.
        """
        self.assertEqual(self.workdays.schedule, self.schedule)
        self.assertEqual(self.workdays.workday, 1)
        self.assertEqual(self.workdays.start_time, "10:00")
        self.assertEqual(self.workdays.end_time, "20:00")

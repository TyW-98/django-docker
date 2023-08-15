"""
Test wait_for_db command
"""
from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from psycopg2 import OperationalError as Psycopg2Error


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):

    def test_wait_for_db_readiness(self, patched_check):
        """Test to check if database is ready"""
        # Return true value when command check is called
        patched_check.return_value = True

        # Simulate calling the command "wait_for_db"
        # located in the commands folder in command line
        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=['default'])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Check if database is ready if not delay and try again"""

        # Raise expectional error in the order they are called in when starting postgresql # noqa: E501
        # First two times (2) it will raise the Psycopg2Error
        # Next three times (3) it will raise the OperationalError
        # Before lastly returning True.
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command("wait_for_db")

        # Check the number of calls
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])

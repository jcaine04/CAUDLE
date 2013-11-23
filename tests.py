from app import app
from app.main import Team, Conference
import unittest


class TestTeam(unittest.TestCase):

    def test_get_roster_urls(self):
        team = Team()
        team_urls = team.extract_roster_urls()
        self.assertEqual(list, type(team_urls))

if __name__ == '__main__':
    unittest.main()
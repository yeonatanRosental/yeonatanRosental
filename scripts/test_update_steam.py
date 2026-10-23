import unittest
import xml.etree.ElementTree as ET

from update_steam import STEAM_ID, activity, render


def profile(body):
    return f'<profile><steamID64>{STEAM_ID}</steamID64><privacyState>public</privacyState>{body}</profile>'


class SteamCardTests(unittest.TestCase):
    def test_current_game_from_status_message(self):
        document = profile('<onlineState>in-game</onlineState><stateMessage><![CDATA[In-Game<br/>Balatro]]></stateMessage>')
        self.assertEqual(activity(document)[:2], ('NOW PLAYING', 'Balatro'))

    def test_current_game_and_xml_escaping(self):
        document = profile('<onlineState>in-game</onlineState><inGameInfo><gameName>A &amp; B &lt;C&gt;</gameName></inGameInfo>')
        self.assertEqual(activity(document)[:2], ('NOW PLAYING', 'A & B <C>'))
        svg = render(document, '2026-10-23 18:00')
        ET.fromstring(svg)
        self.assertIn('A &amp; B &lt;C&gt;', svg)

    def test_recent_games_when_offline(self):
        document = profile('<onlineState>offline</onlineState><mostPlayedGames><mostPlayedGame><gameName>Portal</gameName><hoursPlayed>2.5</hoursPlayed></mostPlayedGame></mostPlayedGames>')
        self.assertEqual(activity(document), ('RECENT ACTIVITY', 'Currently offline', [('Portal', '2.5')]))
        self.assertIn('2.5 h', render(document, '2026-10-23 18:00'))

    def test_no_activity_does_not_claim_to_be_playing(self):
        self.assertEqual(activity(profile('<onlineState>online</onlineState>')), ('ONLINE', 'No public game activity available', []))

    def test_private_profile(self):
        document = profile('').replace('>public<', '>private<')
        self.assertEqual(activity(document)[0], 'PROFILE PRIVATE')

    def test_invalid_response_is_rejected(self):
        for document in ['<html/>', '<response><error>Unavailable</error></response>', profile('').replace(STEAM_ID, '123'), 'not xml']:
            with self.subTest(document=document), self.assertRaises((ValueError, ET.ParseError)):
                activity(document)


if __name__ == '__main__':
    unittest.main()

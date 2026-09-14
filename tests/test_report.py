from pathlib import Path
import tempfile
import unittest
from app import template,validate,render

class ReportTests(unittest.TestCase):
    def test_required(self):
        with self.assertRaises(ValueError):validate(template())
    def test_html_escape(self):
        data=template()
        for key in ('numer_zlecenia','klient','urzadzenie','zgloszony_problem','diagnoza','wykonane_czynnosci','test_koncowy'):data[key]='<script>test</script>'
        with tempfile.TemporaryDirectory() as d:
            output=render(data,d);text=Path(output['files'][0]).read_text(encoding='utf-8');self.assertNotIn('<script>',text);self.assertIn('Dominik Wasilak',text)
    def test_bad_duration(self):
        data=template();data['czas_pracy_min']=-1
        with self.assertRaises(ValueError):validate(data)

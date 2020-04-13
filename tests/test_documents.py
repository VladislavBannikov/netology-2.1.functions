import main_app as app
import json
import unittest
from io import StringIO
from unittest.mock import patch


class TestDocuments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("../fixtures/documents.json", encoding="utf-8") as f:
            cls.documents = json.load(f)

        with open("../fixtures/directories.json", encoding="utf-8") as f:
            cls.directories = json.load(f)

    def setUp(self):
        with open("../fixtures/documents.json", encoding="utf-8") as f:
            app.documents = json.load(f)

        with open("../fixtures/directories.json", encoding="utf-8") as f:
            app.directories = json.load(f)

    def test_query_by_number_all_document_return(self):
        for doc in self.documents:
            result = app.query_by_number(doc['number'])
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0], doc)

    def test_list_all(self):
        newline = '\n'
        expected_result = ''
        for doc in self.documents:
            expected_result += f'{doc["type"]} "{doc["number"]}" "{doc["name"]}";' + newline

        with patch('sys.stdout',new=StringIO()) as fake_out:
            app.list_all()
            self. assertEqual(expected_result,fake_out.getvalue())

    def test_add_doc(self):
        test_shelf = "1"
        test_data = {"type": "passport", "number": "10008", "name": "Артур Пирожков"}

        with patch("main_app.input") as in_mock:
            in_mock.side_effect = list(test_data.values())+[test_shelf]
            result = app.add_doc()
        self.assertEqual(result, 0)
        self.assertIn(test_data, app.documents)
        self.assertIn(test_data["number"], app.directories[test_shelf])

        shelves = list(app.directories.keys())
        shelves.remove(test_shelf)
        for sh in shelves:
            self.assertNotIn(test_data["number"], app.directories[sh])

    def test_del_docs(self):
        numb_to_remove = "2207 876234"
        shelf = None
        for sh_number, docs in self.directories.items():
            if numb_to_remove in docs:
                shelf = sh_number
        print(shelf)
        self.assertIsNotNone(shelf)

        result = app.del_doc(numb_to_remove)
        self.assertEqual(result, 0)


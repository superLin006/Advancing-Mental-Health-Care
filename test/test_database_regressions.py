"""Isolate database routines from local model loading and external services."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]

class DatabaseRegressions(unittest.TestCase):
    def query(self, model, connector):
        path = ROOT / 'model' / f'query_{model}.py'
        tree = ast.parse(path.read_text(encoding='utf-8-sig'))
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'get_pairs_from_db')
        scope = {'mysql': SimpleNamespace(connector=connector), 'Error': ConnectionError}
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), 'exec'), scope)
        return scope['get_pairs_from_db']

    def test_failed_connect_preserves_original_error_in_all_query_models(self):
        original = ConnectionError('database unavailable')
        def fail(**kwargs): raise original
        for model in ('BERT', 'ALBERT', 'RoBERTa', 'XLNet'):
            with self.subTest(model=model), self.assertRaises(ConnectionError) as error:
                self.query(model, SimpleNamespace(connect=fail))({}, 0, 1)
            self.assertIs(error.exception, original)

    def test_cursor_creation_failure_closes_connection(self):
        closed = []
        def fail(): raise ConnectionError('cursor unavailable')
        conn = SimpleNamespace(is_connected=lambda: True, cursor=fail, close=lambda: closed.append(True))
        for model in ('BERT', 'ALBERT', 'RoBERTa', 'XLNet'):
            with self.assertRaises(ConnectionError):
                self.query(model, SimpleNamespace(connect=lambda **_: conn))({}, 0, 1)
        self.assertEqual(closed, [True] * 4)

    def test_create_precedes_alter_and_index_creation_is_repeatable(self):
        path = ROOT / 'Preprocessing' / 'data_import.py'
        tree = ast.parse(path.read_text(encoding='utf-8-sig'))
        nodes = []
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'file_path' for t in node.targets):
                break
            if not isinstance(node, (ast.Import, ast.ImportFrom)): nodes.append(node)
        for exists in (False, True):
            commands = []
            cursor = SimpleNamespace(execute=lambda sql, *params: commands.append(sql),
                                     fetchone=lambda: (1,) if exists else None)
            conn = SimpleNamespace(cursor=lambda: cursor)
            scope = {'mysql': SimpleNamespace(connector=SimpleNamespace(connect=lambda **_: conn))}
            exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), scope)
            create = next(i for i, sql in enumerate(commands) if 'CREATE TABLE' in sql)
            alter = next(i for i, sql in enumerate(commands) if 'CONVERT TO' in sql)
            self.assertLess(create, alter)
            self.assertEqual(sum('ADD FULLTEXT' in sql for sql in commands), int(not exists))
            self.assertIn('`medical_qa`', commands[0])

if __name__ == '__main__':
    unittest.main()

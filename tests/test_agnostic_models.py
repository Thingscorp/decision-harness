"""LLM-agnostic regression tests. No network, no key, no charges.

The hardcoded ALLOWED_MODELS allowlist was removed so any model string
is accepted on a SystemOne route. The endpoint, not this CLI, decides
which models it serves.
Run: python3 -m unittest tests.test_agnostic_models
"""
import json
import os
import sys
import unittest
from unittest.mock import patch

import importlib.util
import importlib.machinery
spec = importlib.util.spec_from_file_location(
    "clef_decide_agnostic",
    os.path.join(os.path.dirname(__file__), "..", "bin", "clef-decide"),
    loader=importlib.machinery.SourceFileLoader(
        "clef_decide_agnostic",
        os.path.join(os.path.dirname(__file__), "..", "bin", "clef-decide")))
clef = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clef)

QUESTIONS = {"q": {"type": "noul", "instructions": "Is this fine?"}}


class FakeResp:
    def __init__(self, payload):
        self._payload = payload

    def read(self):
        return json.dumps(self._payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class TestAgnosticModels(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ,
                              {"EXPERIENTIAL_API_KEY": "test-key-dummy"})
        self.env.start()

    def tearDown(self):
        self.env.stop()

    def test_resolve_judge_arbitrary_model_systemone(self):
        self.assertEqual(
            clef.resolve_judge("clef", model_flag="vendor-custom-v1"),
            ("systemone", "vendor-custom-v1"))

    def test_call_clef_arbitrary_model_sent_exactly(self):
        cap = {}

        def opener(req, timeout=None):
            cap["url"] = req.full_url
            cap["body"] = json.loads(req.data.decode())
            return FakeResp({"answers": {}, "usage": {}})

        clef.call_clef("vendor-custom-v1", "s", QUESTIONS, _opener=opener)
        self.assertEqual(cap["body"]["model"], "vendor-custom-v1")
        self.assertEqual(
            cap["url"], "https://api.experientiallabs.ai/v1/systemone")

    def test_no_allowlist_constant_remains(self):
        self.assertFalse(hasattr(clef, "ALLOWED_MODELS"))


if __name__ == "__main__":
    unittest.main()

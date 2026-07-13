import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "prepare_substrate.py"
SPEC = importlib.util.spec_from_file_location("prepare_substrate", MODULE_PATH)
prepare_substrate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = prepare_substrate
SPEC.loader.exec_module(prepare_substrate)


class ExecutionModeEstimateTest(unittest.TestCase):
    def test_threshold_itself_uses_one_reader(self) -> None:
        estimate = prepare_substrate.estimate_execution_mode(221_739)

        self.assertEqual(estimate["execution_mode"], "single_reader")
        self.assertEqual(estimate["projected_working_tokens"], 100_000)

    def test_above_threshold_uses_fanout(self) -> None:
        estimate = prepare_substrate.estimate_execution_mode(221_742)

        self.assertEqual(estimate["execution_mode"], "fanout")
        self.assertGreater(estimate["projected_working_tokens"], 100_000)


if __name__ == "__main__":
    unittest.main()

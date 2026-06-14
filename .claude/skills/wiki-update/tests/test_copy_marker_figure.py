#!/usr/bin/env python3
"""Regression tests for marker figure caption matching."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "copy_marker_figure.py"


def load_module():
    spec = importlib.util.spec_from_file_location("copy_marker_figure", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CopyMarkerFigureTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()

    def test_finds_colon_caption(self) -> None:
        markdown = "\n".join(
            [
                "![estimate plot](figures/figure-1.png)",
                "Figure 1: Main estimate.",
            ]
        )

        self.assertEqual(
            self.module.find_source_ref(markdown, "1", 2, 2),
            "figures/figure-1.png",
        )

    def test_finds_period_caption(self) -> None:
        markdown = "\n".join(
            [
                "![estimate plot](figures/figure-1.png)",
                "Figure 1. Main estimate.",
            ]
        )

        self.assertEqual(
            self.module.find_source_ref(markdown, "1", 2, 2),
            "figures/figure-1.png",
        )

    def test_period_caption_does_not_match_decimal_subfigure(self) -> None:
        markdown = "\n".join(
            [
                "![appendix plot](figures/figure-1-2.png)",
                "Figure 1.2 Appendix estimate.",
            ]
        )

        with self.assertRaisesRegex(SystemExit, "figure 1 image reference not found"):
            self.module.find_source_ref(markdown, "1", 2, 2)

    def test_bold_period_caption(self) -> None:
        # NEJM/JAMA style: label and trailing period live inside bold markup.
        markdown = "\n".join(
            [
                "**Figure 1.** Enrollment and randomization.",
                "![flow diagram](figures/figure-1.png)",
            ]
        )

        self.assertEqual(
            self.module.find_source_ref(markdown, "1", 2, 2),
            "figures/figure-1.png",
        )

    def test_caption_outranks_inline_mention(self) -> None:
        # An inline mention precedes the real caption and sits one line from the
        # previous figure's image; the caption must still win.
        markdown = "\n".join(
            [
                "results appear in **FIGURE 2** and Table 1.",  # 0 inline mention
                "![fig1](figures/figure-1.png)",               # 1 prev figure image
                "filler",                                       # 2
                "**Figure 2.** Main estimate.",                # 3 real caption
                "![fig2](figures/figure-2.png)",               # 4 this figure image
            ]
        )

        self.assertEqual(
            self.module.find_source_ref(markdown, "2", 2, 2),
            "figures/figure-2.png",
        )

    def test_mention_only_prefers_forward_image_on_tie(self) -> None:
        # JAMA Fig 3 shape: no caption line exists, only an inline mention that
        # is equidistant from the previous figure's image (above) and this
        # figure's image (below). Forward image must win.
        markdown = "\n".join(
            [
                "![fig2](figures/figure-2.png)",                  # 0 prev image
                "filler",                                         # 1
                "estimates appear in **FIGURE 3** and Table 1.",  # 2 inline mention
                "filler",                                         # 3
                "![fig3](figures/figure-3.png)",                  # 4 this image
            ]
        )

        self.assertEqual(
            self.module.find_source_ref(markdown, "3", 2, 2),
            "figures/figure-3.png",
        )


if __name__ == "__main__":
    unittest.main()

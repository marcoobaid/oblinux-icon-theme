#!/usr/bin/env python3
"""Regression tests for the OBLinux Horizon icon generator."""

from pathlib import Path
import tempfile
import unittest

from build_papirus_derivative import transform_theme


SVG = '<svg width="16" height="16"><path fill="#000000" d="M1 1h14v14H1z"/></svg>\n'
APP_FRAME = 'scale(0.76)'


class TransformThemeTests(unittest.TestCase):
    def test_symbolic_app_icons_are_not_wrapped_in_application_frame(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "Papirus"
            destination = root / "OBLinux-Horizon"
            symbolic = source / "16x16" / "symbolic" / "apps" / "network-symbolic.svg"
            regular = source / "48x48" / "apps" / "network.svg"
            symbolic.parent.mkdir(parents=True)
            regular.parent.mkdir(parents=True)
            (source / "index.theme").write_text(
                "[Icon Theme]\nName=Papirus\nDirectories=16x16/symbolic/apps,48x48/apps\n",
                encoding="utf-8",
            )
            symbolic.write_text(SVG, encoding="utf-8")
            regular.write_text(SVG, encoding="utf-8")

            applications, system_icons, aliases = transform_theme(
                source,
                destination,
                "OBLinux Horizon",
                "hicolor",
            )

            transformed_symbolic = (
                destination / "16x16" / "symbolic" / "apps" / "network-symbolic.svg"
            ).read_text(encoding="utf-8")
            transformed_regular = (
                destination / "48x48" / "apps" / "network.svg"
            ).read_text(encoding="utf-8")

            self.assertNotIn(APP_FRAME, transformed_symbolic)
            self.assertIn(APP_FRAME, transformed_regular)
            self.assertEqual((applications, system_icons, aliases), (1, 1, 0))


if __name__ == "__main__":
    unittest.main()

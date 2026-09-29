"""Regression tests for the capsule bar's weather display."""
import unittest

from qtile_config.widgets import weather_text


class WeatherTextTests(unittest.TestCase):
    def test_temperature_is_the_only_bar_text(self):
        text, tooltip = weather_text(
            '{"location":"Delhi","condition":"Sunny","temperature":"+31°C",'
            '"feels_like":"+33°C","humidity":"40%","wind":"12 km/h"}'
        )
        self.assertEqual(text, "+31°C")
        self.assertIn("Delhi", tooltip)
        self.assertIn("Sunny", tooltip)
        self.assertIn("Feels like +33°C", tooltip)
        self.assertIn("Humidity 40%", tooltip)
        self.assertIn("Wind 12 km/h", tooltip)

    def test_missing_temperature_has_safe_fallback(self):
        text, tooltip = weather_text("{}")
        self.assertEqual(text, "Weather N/A")
        self.assertIn("unavailable", tooltip.lower())

    def test_invalid_json_has_safe_fallback(self):
        text, tooltip = weather_text("not-json")
        self.assertEqual(text, "Weather N/A")
        self.assertIn("unavailable", tooltip.lower())


if __name__ == "__main__":
    unittest.main()

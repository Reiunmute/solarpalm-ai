"""Static website checks for the SolarPalm landing page."""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def read_site_file(name):
    return (SITE / name).read_text(encoding="utf-8")


class TestStaticSite(unittest.TestCase):
    def test_site_files_exist(self):
        for name in [
            "index.html",
            "styles.css",
            "app.js",
            "DESIGN-TOKENS.md",
            "assets/solar-install-hero.png",
            "assets/solar-install-detail.png",
            "assets/solar-finished-home.png",
        ]:
            self.assertTrue((SITE / name).exists(), name)

    def test_landing_page_has_product_sections(self):
        html = read_site_file("index.html")
        for text in [
            "Find out if solar makes sense for your home",
            "Check savings",
            "Start with your roof",
            "See the payback before you commit",
            "Contact us",
        ]:
            self.assertIn(text, html)

    def test_removed_source_and_technical_homepage_copy(self):
        html = read_site_file("index.html")
        for removed in [
            "PVGIS primary",
            "NASA fallback",
            "FJD economics",
            "Every number keeps its source label",
            "This browser panel mirrors the documented default formula",
            "calculation core",
            "Solar starts with a simple question",
            "can your roof produce enough power",
            "github.com/Reiunmute/solarpalm-ai</a>",
            "reisummermute@gmail.com</a>",
            "@Reiunmute",
            "source-grid",
            "source-section",
        ]:
            self.assertNotIn(removed, html)

    def test_contact_links(self):
        html = read_site_file("index.html")
        self.assertIn('href="https://github.com/Reiunmute/solarpalm-ai"', html)
        self.assertIn('href="mailto:reisummermute@gmail.com"', html)
        self.assertIn('class="contact-icon disabled"', html)
        self.assertIn('aria-label="X account coming soon"', html)
        self.assertNotIn('href="https://x.com/Reiunmute"', html)
        self.assertNotIn('href="https://x.com/', html)

    def test_landing_page_uses_generated_large_images(self):
        html = read_site_file("index.html")
        for asset in [
            "./assets/solar-install-hero.png",
            "./assets/solar-install-detail.png",
            "./assets/solar-finished-home.png",
        ]:
            self.assertIn(asset, html)

    def test_static_site_has_tesla_like_product_layout(self):
        css = read_site_file("styles.css")
        for token in [
            "full-bleed",
            "min-height: 100vh",
            "split-section",
            "grid-template-columns: 1fr 1fr",
            "border-radius: 999px",
            "object-fit: cover",
            "contact-grid",
            "font-size: 13px",
            "border-top: 1px solid rgba(255, 255, 255, 0.1)",
            "background: transparent",
        ]:
            self.assertIn(token, css)
        self.assertNotIn("source-grid", css)
        self.assertNotIn("source-section", css)

    def test_calculator_defaults_match_readme_example_shape(self):
        js = read_site_file("app.js")
        html = read_site_file("index.html")
        self.assertIn('id="savings-section"', html)
        self.assertIn('id="savings"', html)
        self.assertIn('value="3"', html)
        self.assertIn('value="1272"', html)
        self.assertIn('value="0.32"', html)
        self.assertIn('value="3000"', html)
        self.assertIn("const annualKwh = kwp * annualYield", js)
        self.assertIn("const payback = capex / savings", js)

    def test_no_em_dash_in_site_files(self):
        for path in SITE.glob("**/*"):
            if path.is_file() and path.suffix.lower() in {".html", ".css", ".js", ".md"}:
                self.assertNotIn("\u2014", path.read_text(encoding="utf-8"), str(path))


if __name__ == "__main__":
    unittest.main()

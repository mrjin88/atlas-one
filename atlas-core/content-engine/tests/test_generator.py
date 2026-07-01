import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from generator import ContentPackageGenerator
from pipeline import ContentPipeline


class TestContentPackageGenerator:
    """Tests for the content package generator."""

    def test_generate_creates_all_files(self) -> None:
        pipeline = ContentPipeline()
        plan = pipeline.run("Roman concrete")

        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ContentPackageGenerator(tmpdir)
            files = generator.generate(plan)

            assert len(files) == 6
            for section, filepath in files.items():
                assert Path(filepath).exists(), f"Missing file: {filepath}"

    def test_generate_research_md(self) -> None:
        pipeline = ContentPipeline()
        plan = pipeline.run("Roman concrete")

        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ContentPackageGenerator(tmpdir)
            files = generator.generate(plan)

            content = Path(files["research"]).read_text(encoding="utf-8")
            assert "# Research Notes" in content
            assert "Roman concrete" in content

    def test_generate_script_md(self) -> None:
        pipeline = ContentPipeline()
        plan = pipeline.run("Roman concrete")

        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ContentPackageGenerator(tmpdir)
            files = generator.generate(plan)

            content = Path(files["script"]).read_text(encoding="utf-8")
            assert "# Script Outline" in content
            assert "Draft a script" in content

    def test_generate_seo_json(self) -> None:
        pipeline = ContentPipeline()
        plan = pipeline.run("Roman concrete")

        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ContentPackageGenerator(tmpdir)
            files = generator.generate(plan)

            data = json.loads(Path(files["seo"]).read_text(encoding="utf-8"))
            assert "seo_guidance" in data
            assert len(data["seo_guidance"]) > 0

    def test_generate_publish_checklist_md(self) -> None:
        pipeline = ContentPipeline()
        plan = pipeline.run("Roman concrete")

        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ContentPackageGenerator(tmpdir)
            files = generator.generate(plan)

            content = Path(files["publish_checklist"]).read_text(encoding="utf-8")
            assert "# Publishing Checklist" in content

    def test_generate_image_prompts_md(self) -> None:
        pipeline = ContentPipeline()
        plan = pipeline.run("Roman concrete")

        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ContentPackageGenerator(tmpdir)
            files = generator.generate(plan)

            content = Path(files["image_prompts"]).read_text(encoding="utf-8")
            assert "# Image Prompts" in content

    def test_generate_video_prompts_md(self) -> None:
        pipeline = ContentPipeline()
        plan = pipeline.run("Roman concrete")

        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ContentPackageGenerator(tmpdir)
            files = generator.generate(plan)

            content = Path(files["video_prompts"]).read_text(encoding="utf-8")
            assert "# Video Prompts" in content

    def test_generate_output_directory_created(self) -> None:
        pipeline = ContentPipeline()
        plan = pipeline.run("Test")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "nested" / "LA-0001"
            generator = ContentPackageGenerator(output_dir)
            files = generator.generate(plan)

            assert output_dir.exists()
            assert len(files) == 6

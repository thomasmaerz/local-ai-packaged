import tempfile
import unittest
from pathlib import Path

import start_services


class LiteLLMEnvTests(unittest.TestCase):
    def test_generate_litellm_keys_when_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text("POSTGRES_PASSWORD=test\n", encoding="utf-8")

            values = start_services.ensure_litellm_env(str(env_path))

            self.assertIn("LITELLM_MASTER_KEY", values)
            self.assertIn("LITELLM_SALT_KEY", values)
            self.assertTrue(values["LITELLM_MASTER_KEY"].startswith("sk-"))
            self.assertTrue(values["LITELLM_SALT_KEY"].startswith("sk-"))

            env_data = env_path.read_text(encoding="utf-8")
            self.assertIn("LITELLM_MASTER_KEY=", env_data)
            self.assertIn("LITELLM_SALT_KEY=", env_data)

    def test_preserve_existing_litellm_keys(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "POSTGRES_PASSWORD=test",
                        "LITELLM_MASTER_KEY=sk-existing-master",
                        "LITELLM_SALT_KEY=sk-existing-salt",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            values = start_services.ensure_litellm_env(str(env_path))

            self.assertEqual(values["LITELLM_MASTER_KEY"], "sk-existing-master")
            self.assertEqual(values["LITELLM_SALT_KEY"], "sk-existing-salt")

    def test_parse_env_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "# comment",
                        "KEY_ONE=value-one",
                        "KEY_TWO=\"value-two\"",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            parsed = start_services.parse_env_file(str(env_path))
            self.assertEqual(parsed["KEY_ONE"], "value-one")
            self.assertEqual(parsed["KEY_TWO"], "value-two")


if __name__ == "__main__":
    unittest.main()

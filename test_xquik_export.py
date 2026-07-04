import unittest

from xquik_export import normalize_xquik_csv


class XquikExportTest(unittest.TestCase):
    def test_maps_common_xquik_columns(self):
        rows = normalize_xquik_csv(
            "tweet_id,created_at,full_text\n"
            "t1,2026-07-04T12:00:00Z,Launch update\n"
        )

        self.assertEqual(
            rows,
            [
                {
                    "text": "Launch update",
                    "tweet_id": "t1",
                    "created_at": "2026-07-04T12:00:00Z",
                }
            ],
        )

    def test_skips_blank_text_rows(self):
        rows = normalize_xquik_csv("id,text\n1,\n2,Useful post\n")

        self.assertEqual([row["text"] for row in rows], ["Useful post"])

    def test_requires_text_column(self):
        with self.assertRaises(ValueError):
            normalize_xquik_csv("id,likes\n1,3\n")


if __name__ == "__main__":
    unittest.main()

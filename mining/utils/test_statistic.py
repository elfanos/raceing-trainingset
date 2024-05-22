
import unittest
import pandas as pd
from pandas.testing import assert_frame_equal

class TestTotalEarnings(unittest.TestCase):
    def setUp(self):
        self.data = {
            "2023": {
                "starts": 375,
                "earnings": 338424900,
                "placement": {
                    "1": 49,
                    "2": 40,
                    "3": 32
                },
                "winPercentage": 1306
            },
            "2024": {
                "starts": 126,
                "earnings": 138823300,
                "placement": {
                    "1": 29,
                    "2": 15,
                    "3": 9
                },
                "winPercentage": 2301
            }
        }

    def test_total_earnings(self):
        from statistic import statistic_df  # replace 'statistic' with the name of your module
        result = statistic_df(self.data)
        
        # Define the expected DataFrame
        expected_data = {
            "starts": [375, 126],
            "earnings": [338424900, 138823300],
            "placement_1": [49, 29],
            "placement_2": [40, 15],
            "placement_3": [32, 9],
            "winPercentage": [1306, 2301]
        }
        expected_df = pd.DataFrame(expected_data)
        
        # Compare the resulting DataFrame with the expected DataFrame
        assert_frame_equal(result, expected_df)


if __name__ == '__main__':
    unittest.main()


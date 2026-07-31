import unittest
from unittest.mock import MagicMock, patch

from guardian.intelligence.token.analyzer import MAJOR_TOKENS, TokenAnalyzer
from guardian.intelligence.token.providers import (
    DexScreenerTokenDataProvider,
    MockTokenDataProvider,
)


class TestMockTokenDataProvider(unittest.TestCase):
    def test_returns_a_numeric_liquidity_not_just_unknown(self):
        provider = MockTokenDataProvider()
        profile = provider.get_liquidity_profile("SOMECOIN", "ethereum")
        self.assertIsNotNone(profile.liquidity_usd)


class TestDexScreenerTokenDataProvider(unittest.TestCase):
    def test_picks_highest_liquidity_pair_on_matching_chain(self):
        provider = DexScreenerTokenDataProvider(base_url="https://api.dexscreener.com")
        fake_response = MagicMock()
        fake_response.raise_for_status = MagicMock()
        fake_response.json.return_value = {
            "pairs": [
                {"chainId": "ethereum", "liquidity": {"usd": 1000}},
                {"chainId": "ethereum", "liquidity": {"usd": 50000}},
                {"chainId": "base", "liquidity": {"usd": 999999}},  # wrong chain, should be ignored
            ]
        }
        with patch("httpx.get", return_value=fake_response):
            profile = provider.get_liquidity_profile("PEPE", "ethereum")
        self.assertEqual(profile.liquidity_usd, 50000)
        self.assertFalse(profile.is_concentrated)

    def test_no_pairs_found_is_low_confidence_not_a_guess(self):
        provider = DexScreenerTokenDataProvider(base_url="https://api.dexscreener.com")
        fake_response = MagicMock()
        fake_response.raise_for_status = MagicMock()
        fake_response.json.return_value = {"pairs": []}
        with patch("httpx.get", return_value=fake_response):
            profile = provider.get_liquidity_profile("MADEUPTOKEN", "ethereum")
        self.assertEqual(profile.match_confidence, 0.0)

    def test_network_failure_degrades_to_unknown(self):
        provider = DexScreenerTokenDataProvider(base_url="https://api.dexscreener.com")
        with patch("httpx.get", side_effect=ConnectionError("timeout")):
            profile = provider.get_liquidity_profile("PEPE", "ethereum")
        self.assertIsNone(profile.liquidity_usd)
        self.assertEqual(profile.data_source, "dexscreener_error")


class TestTokenAnalyzerMajorTokenFastPath(unittest.TestCase):
    """Real logic, not mock: major tokens should never touch the provider."""

    def test_major_token_skips_provider_entirely(self):
        provider = MagicMock()
        analyzer = TokenAnalyzer(provider)
        signals = analyzer.analyze("USDC", "ethereum")
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "major_token")
        provider.get_liquidity_profile.assert_not_called()

    def test_non_major_token_uses_provider(self):
        provider = MagicMock()
        provider.get_liquidity_profile.return_value = MagicMock(
            liquidity_usd=100.0, is_concentrated=True, data_source="mock", match_confidence=1.0,
        )
        analyzer = TokenAnalyzer(provider)
        analyzer.analyze("RANDOMTOKEN", "ethereum")
        provider.get_liquidity_profile.assert_called_once_with("RANDOMTOKEN", "ethereum")

    def test_major_tokens_set_matches_known_stables_and_majors(self):
        for sym in ("ETH", "USDC", "USDT", "DAI"):
            self.assertIn(sym, MAJOR_TOKENS)


if __name__ == "__main__":
    unittest.main()

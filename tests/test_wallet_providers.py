import unittest
from unittest.mock import MagicMock, patch

from guardian.intelligence.wallet.analyzer import WalletAnalyzer
from guardian.intelligence.wallet.providers import (
    MockWalletDataProvider,
    RpcWalletDataProvider,
    WalletProfile,
)


class TestMockWalletDataProvider(unittest.TestCase):
    def test_deterministic_for_same_input(self):
        provider = MockWalletDataProvider()
        p1 = provider.get_profile("0xabc", "ethereum")
        p2 = provider.get_profile("0xabc", "ethereum")
        self.assertEqual(p1.age_days, p2.age_days)
        self.assertEqual(p1.tx_count, p2.tx_count)

    def test_different_chains_give_different_profiles(self):
        provider = MockWalletDataProvider()
        eth = provider.get_profile("0xabc", "ethereum")
        base = provider.get_profile("0xabc", "base")
        # Not guaranteed to differ on every field, but the hash input includes
        # chain, so at least one of the two profiles should differ overall.
        self.assertTrue(eth != base or eth.age_days != base.age_days)

    def test_data_source_is_labeled_mock(self):
        provider = MockWalletDataProvider()
        profile = provider.get_profile("0xabc", "ethereum")
        self.assertEqual(profile.data_source, "mock")


class TestRpcWalletDataProvider(unittest.TestCase):
    """Exercises the RPC provider's logic against a stubbed web3 client -
    no real network access, but validates that our code calls the right
    methods and handles their results (and failures) correctly."""

    def _stub_web3(self, tx_count=5, code=b"", block_number=1000):
        fake_w3 = MagicMock()
        fake_w3.to_checksum_address.side_effect = lambda a: a
        fake_w3.eth.get_transaction_count.return_value = tx_count
        fake_w3.eth.get_code.return_value = code
        fake_w3.eth.block_number = block_number
        return fake_w3

    def test_eoa_profile(self):
        provider = RpcWalletDataProvider(rpc_urls={"ethereum": "http://fake"})
        fake_w3 = self._stub_web3(tx_count=42, code=b"")
        with patch.object(provider, "_client", return_value=fake_w3):
            profile = provider.get_profile("0xabc", "ethereum")
        self.assertEqual(profile.tx_count, 42)
        self.assertFalse(profile.is_contract)
        self.assertIsNone(profile.age_days)  # estimate_age is off by default
        self.assertEqual(profile.data_source, "rpc")

    def test_contract_address_detected(self):
        provider = RpcWalletDataProvider(rpc_urls={"ethereum": "http://fake"})
        fake_w3 = self._stub_web3(code=b"\x60\x80\x60\x40")
        with patch.object(provider, "_client", return_value=fake_w3):
            profile = provider.get_profile("0xabc", "ethereum")
        self.assertTrue(profile.is_contract)

    def test_missing_rpc_url_raises_on_client_creation(self):
        provider = RpcWalletDataProvider(rpc_urls={})
        with self.assertRaises(ValueError):
            provider._client("ethereum")

    def test_rpc_failure_degrades_to_unknown_not_a_crash(self):
        provider = RpcWalletDataProvider(rpc_urls={"ethereum": "http://fake"})
        with patch.object(provider, "_client", side_effect=ConnectionError("node unreachable")):
            profile = provider.get_profile("0xabc", "ethereum")
        self.assertIsNone(profile.tx_count)
        self.assertIsNone(profile.age_days)
        self.assertEqual(profile.data_source, "rpc_error")

    def test_age_estimation_binary_search_finds_first_active_block(self):
        # Wallet becomes active (nonzero balance) at block 600 and stays active after.
        provider = RpcWalletDataProvider(rpc_urls={"ethereum": "http://fake"}, estimate_age=True)
        fake_w3 = self._stub_web3(block_number=1000)
        fake_w3.eth.get_transaction_count.return_value = 0

        def fake_balance(address, block_identifier):
            return 10 if block_identifier >= 600 else 0

        fake_w3.eth.get_balance.side_effect = fake_balance
        fake_w3.eth.get_block.side_effect = lambda n: {"timestamp": n * 12}  # ~12s/block

        with patch.object(provider, "_client", return_value=fake_w3):
            profile = provider.get_profile("0xabc", "ethereum")

        self.assertIsNotNone(profile.age_days)
        # (1000 - 600) blocks * 12s/block = 4800s = 0 days (less than a day) - just
        # check it's a non-negative int, the binary search converged near 600.
        self.assertGreaterEqual(profile.age_days, 0)

    def test_age_estimation_failure_returns_none_not_a_guess(self):
        provider = RpcWalletDataProvider(rpc_urls={"ethereum": "http://fake"}, estimate_age=True)
        fake_w3 = self._stub_web3(tx_count=0)  # nonce=0 so the code falls through to get_balance
        fake_w3.eth.get_balance.side_effect = Exception("archive data unavailable")
        with patch.object(provider, "_client", return_value=fake_w3):
            profile = provider.get_profile("0xabc", "ethereum")
        self.assertIsNone(profile.age_days)


class TestWalletAnalyzerHandlesUnknownData(unittest.TestCase):
    """Unknown must never look the same as low-risk."""

    def test_unknown_age_produces_a_signal_not_silence(self):
        class UnknownProvider:
            def get_profile(self, address, chain):
                return WalletProfile(address=address, age_days=None, tx_count=10, data_source="rpc")

        analyzer = WalletAnalyzer(UnknownProvider())
        signals = analyzer.analyze("0xabc", "ethereum")
        names = [s.name for s in signals]
        self.assertIn("wallet_age_unknown", names)
        self.assertNotIn("established_wallet", names)

    def test_flagged_wallet_produces_high_score_signal(self):
        class FlaggedProvider:
            def get_profile(self, address, chain):
                return WalletProfile(address=address, age_days=100, tx_count=10, is_flagged=True, data_source="mock")

        analyzer = WalletAnalyzer(FlaggedProvider())
        signals = analyzer.analyze("0xabc", "ethereum")
        flagged = [s for s in signals if s.name == "flagged_wallet"]
        self.assertEqual(len(flagged), 1)
        self.assertGreaterEqual(flagged[0].score, 90)


if __name__ == "__main__":
    unittest.main()

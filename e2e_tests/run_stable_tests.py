#!/usr/bin/env python3
"""
Run tests that are likely to pass without requiring API access
"""

import subprocess
import sys
from typing import Dict, List


def print_header(message: str) -> None:
    """ヘッダーメッセージを表示"""
    print("=" * 60)
    print(message)
    print("=" * 60)


def run_test_command(test_paths: List[str], dotenv_file: str = ".env.local") -> bool:
    """テストコマンドを実行"""
    cmd = (
        ["dotenvx", "run", "-f", dotenv_file, "--", "uv", "run", "python", "-m", "pytest"]
        + test_paths
        + ["-v"]
    )

    result = subprocess.run(cmd, check=False)
    return result.returncode == 0


def main() -> int:
    """メイン実行関数"""
    print_header("安定版e2eテストを実行中（時間のかかる操作は除外）")

    dotenv_file = ".env.local"
    print(f"環境変数を {dotenv_file} から読み込み中...")

    # 安定したテストのリスト
    stable_tests: Dict[str, List[str]] = {
        "NFT API": [
            "e2e_tests/test_nft.py::test_get_nfts_by_owner",
            "e2e_tests/test_nft.py::test_get_nft_metadata",
            "e2e_tests/test_nft.py::test_get_nft_holders",
        ],
        "Query API": [
            "e2e_tests/test_query.py::test_get_blockchain_stats",
            "e2e_tests/test_query.py::test_get_blocks",
            "e2e_tests/test_query.py::test_get_supported_networks",
        ],
        "Token API": [
            "e2e_tests/test_token.py::test_get_account_balance",
            "e2e_tests/test_token.py::test_get_token_price",
        ],
        "Mock Tests": [
            "e2e_tests/test_mock.py",
        ],
    }

    # テスト実行
    all_success = True
    for category, tests in stable_tests.items():
        print(f"\n{category}テストを実行中...")
        success = run_test_command(tests, dotenv_file)
        if not success:
            all_success = False

    # 結果表示
    if all_success:
        print("\n全ての安定テストは正常に完了しました！")
        return 0
    else:
        print("\n一部のテストが失敗しました。ログを確認してください。")
        return 1


if __name__ == "__main__":
    sys.exit(main())

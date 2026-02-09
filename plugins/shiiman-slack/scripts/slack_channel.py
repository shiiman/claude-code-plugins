#!/usr/bin/env python3
"""Slack チャンネル操作スクリプト for shiiman-slack."""

import os
import sys
import argparse
from typing import List, Dict

# lib/ ディレクトリをパスに追加
lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib")
sys.path.insert(0, lib_dir)

from slack_utils import (
    get_slack_client,
    handle_api_error,
    format_output,
)


@handle_api_error
def search_channels(
    query: str,
    output_format: str = "table",
) -> None:
    """チャンネルを名前で検索する。

    プライベートチャンネルも検索対象にする。

    Args:
        query: 検索クエリ（チャンネル名の一部）
        output_format: 出力形式 ("table" or "json")
    """
    client = get_slack_client()

    # ページネーションを使用して全チャンネルを取得
    channels: List[Dict] = []
    cursor = None

    while True:
        kwargs = {
            "types": "public_channel,private_channel",
            "limit": 1000,
        }
        if cursor:
            kwargs["cursor"] = cursor

        result = client.conversations_list(**kwargs)
        channels.extend(result.get("channels", []))

        # 次のページがあるか確認
        cursor = result.get("response_metadata", {}).get("next_cursor", "")
        if not cursor:
            break
    
    # クエリでフィルタ
    query_lower = query.lower()
    matched_channels = []
    
    for ch in channels:
        if query_lower in ch.get("name", "").lower():
            matched_channels.append({
                "id": ch["id"],
                "name": ch["name"],
                "is_private": ch.get("is_private", False),
                "topic": ch.get("topic", {}).get("value", ""),
                "purpose": ch.get("purpose", {}).get("value", ""),
                "num_members": ch.get("num_members", 0),
            })
    
    if not matched_channels:
        print(f"「{query}」に一致するチャンネルが見つかりませんでした。")
        return
    
    print(f"検索結果: {len(matched_channels)} 件")
    headers = ["id", "name", "is_private", "topic", "num_members"]
    format_output(matched_channels, headers, output_format)


@handle_api_error
def main() -> None:
    parser = argparse.ArgumentParser(description="Slack チャンネル操作ツール")
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        help="出力形式 (デフォルト: table)",
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # search サブコマンド
    search_parser = subparsers.add_parser("search", help="チャンネル検索")
    search_parser.add_argument("--query", required=True, help="検索クエリ（チャンネル名の一部）")
    
    args = parser.parse_args()
    
    if args.command == "search":
        search_channels(args.query, args.format)


if __name__ == "__main__":
    main()

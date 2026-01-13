#!/usr/bin/env python3
"""Slack チャンネル操作スクリプト for shiiman-slack."""

import argparse
from typing import List, Dict

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
    
    Args:
        query: 検索クエリ（チャンネル名の一部）
        output_format: 出力形式 ("table" or "json")
    """
    client = get_slack_client()
    
    # パブリックチャンネルとプライベートチャンネルを取得
    result = client.conversations_list(
        types="public_channel,private_channel",
        limit=1000,
    )
    
    channels = result.get("channels", [])
    
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

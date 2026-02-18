#!/usr/bin/env python3
"""Slack メッセージ操作スクリプト for shiiman-slack."""

import os
import sys
import argparse
from typing import List, Dict

from slack_sdk.errors import SlackApiError

# lib/ ディレクトリをパスに追加
lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib")
sys.path.insert(0, lib_dir)

from slack_utils import (
    get_slack_client,
    handle_api_error,
    format_output,
    get_user_name,
    resolve_user_names,
)


@handle_api_error
def get_unread_messages(
    channel: str,
    max_results: int = 20,
    output_format: str = "table",
) -> None:
    """未読メッセージを取得する。

    Args:
        channel: チャンネルID
        max_results: 最大取得件数
        output_format: 出力形式 ("table" or "json")
    """
    client = get_slack_client()

    # チャンネル情報を取得（最終既読位置を含む）
    channel_info = client.conversations_info(channel=channel)
    last_read = channel_info["channel"].get("last_read")

    # メッセージ履歴を取得
    result = client.conversations_history(
        channel=channel,
        limit=max_results,
    )

    messages = result.get("messages", [])

    # 未読メッセージをフィルタ
    unread_messages = []
    for msg in messages:
        if not last_read or float(msg["ts"]) > float(last_read):
            unread_messages.append({
                "ts": msg["ts"],
                "user": msg.get("user", ""),
                "text": msg.get("text", ""),
            })

    # ユーザー名を解決
    unread_messages = resolve_user_names(client, unread_messages)

    if not unread_messages:
        print("未読メッセージはありません。")
        return

    print(f"未読メッセージ数: {len(unread_messages)}")
    headers = ["ts", "user_name", "text"]
    format_output(unread_messages, headers, output_format)


@handle_api_error
def mark_as_read(channel: str) -> None:
    """チャンネルを既読にする。

    Args:
        channel: チャンネルID
    """
    client = get_slack_client()

    # 最新メッセージのタイムスタンプを取得
    result = client.conversations_history(
        channel=channel,
        limit=1,
    )

    messages = result.get("messages", [])
    if not messages:
        print("メッセージがありません。")
        return

    latest_ts = messages[0]["ts"]

    # 既読マークを設定
    client.conversations_mark(
        channel=channel,
        ts=latest_ts,
    )

    print(f"チャンネルを既読にしました。")
    print(f"  チャンネル: {channel}")


def _get_unread_mentions_accurate(
    client,
    user_id: str,
    max_results: int,
) -> List[Dict]:
    """conversations.info の last_read を使用して正確な未読メンションを取得する。

    Args:
        client: Slack WebClient
        user_id: 自分のユーザーID
        max_results: 最大取得件数

    Returns:
        未読メンションのリスト
    """
    mentions = []
    mention_pattern = f"<@{user_id}>"

    # 全チャンネル（パブリック・プライベート）を取得（ページング対応）
    cursor = None
    while True:
        channels_result = client.conversations_list(
            types="public_channel,private_channel",
            limit=200,
            cursor=cursor,
        )

        for channel in channels_result.get("channels", []):
            if not channel.get("is_member"):
                continue

            # チャンネル情報を取得（last_read を含む）
            try:
                info = client.conversations_info(channel=channel["id"])
            except SlackApiError:
                # アクセス権限がないチャンネルなどはスキップ
                continue

            channel_data = info.get("channel", {})
            last_read = channel_data.get("last_read")
            # unread_count_display が優先、なければ unread_count を使用
            unread_count_display = channel_data.get("unread_count_display")
            unread_count = unread_count_display if unread_count_display is not None else channel_data.get("unread_count", 0)

            # 未読がないチャンネルはスキップ
            if not unread_count or unread_count == 0:
                continue

            # last_read 以降のメッセージを取得
            try:
                history = client.conversations_history(
                    channel=channel["id"],
                    oldest=last_read,
                    limit=100,
                )
            except SlackApiError:
                # 履歴取得に失敗したチャンネルはスキップ
                continue

            for msg in history.get("messages", []):
                # 自分が送信したメッセージはスキップ
                if msg.get("user") == user_id:
                    continue

                # メンションを含まないメッセージはスキップ
                text = msg.get("text", "")
                if mention_pattern not in text:
                    continue

                # メンションを追加
                user_name = get_user_name(client, msg.get("user", ""))
                mentions.append({
                    "channel": channel.get("name", ""),
                    "user": user_name,
                    "text": text,
                    "ts": msg.get("ts", ""),
                    "permalink": f"https://slack.com/archives/{channel['id']}/p{msg['ts'].replace('.', '')}",
                })

                if len(mentions) >= max_results:
                    return mentions

        # 次のページがあるか確認
        cursor = channels_result.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    return mentions


@handle_api_error
def get_mentions(
    max_results: int = 20,
    output_format: str = "table",
    include_read: bool = False,
) -> None:
    """自分へのメンションを取得する。

    Args:
        max_results: 最大取得件数
        output_format: 出力形式 ("table" or "json")
        include_read: 既読メンションも含める（デフォルト: False = 未読のみ）
    """
    client = get_slack_client()

    # 自分のユーザーIDを取得
    auth_result = client.auth_test()
    user_id = auth_result["user_id"]

    if include_read:
        # 全メンション: search.messages を使用
        query = f"<@{user_id}> -from:me"
        result = client.search_messages(
            query=query,
            count=max_results,
        )

        matches = result.get("messages", {}).get("matches", [])

        if not matches:
            print("メンションはありません。")
            return

        mentions = []
        for match in matches:
            mentions.append({
                "channel": match.get("channel", {}).get("name", ""),
                "user": match.get("username", ""),
                "text": match.get("text", ""),
                "ts": match.get("ts", ""),
                "permalink": match.get("permalink", ""),
            })

        print(f"メンション数: {len(mentions)}")
    else:
        # 未読メンション: conversations.info の last_read を使用（正確）
        mentions = _get_unread_mentions_accurate(client, user_id, max_results)

        if not mentions:
            print("未読メンションはありません。")
            return

        print(f"未読メンション数: {len(mentions)}")

    headers = ["channel", "user", "text", "permalink"]
    format_output(mentions, headers, output_format)


@handle_api_error
def main() -> None:
    parser = argparse.ArgumentParser(description="Slack メッセージ操作ツール")
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        help="出力形式 (デフォルト: table)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # unread サブコマンド
    unread_parser = subparsers.add_parser("unread", help="未読メッセージ一覧")
    unread_parser.add_argument("--channel", required=True, help="チャンネルID")
    unread_parser.add_argument("--max", type=int, default=20, help="最大取得件数")

    # mark-read サブコマンド
    mark_parser = subparsers.add_parser("mark-read", help="既読化")
    mark_parser.add_argument("--channel", required=True, help="チャンネルID")

    # mentions サブコマンド
    mentions_parser = subparsers.add_parser("mentions", help="メンション一覧（デフォルト: 未読のみ）")
    mentions_parser.add_argument("--max", type=int, default=20, help="最大取得件数")
    mentions_parser.add_argument("--all", action="store_true", help="既読も含めて全て取得")

    args = parser.parse_args()

    if args.command == "unread":
        get_unread_messages(args.channel, args.max, args.format)

    elif args.command == "mark-read":
        mark_as_read(args.channel)

    elif args.command == "mentions":
        get_mentions(args.max, args.format, args.all)


if __name__ == "__main__":
    main()

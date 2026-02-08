"""plugin.json / marketplace.json のスキーマバリデーションテスト"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = ROOT / "plugins"
MARKETPLACE_JSON = ROOT / ".claude-plugin" / "marketplace.json"

# plugin.json の必須フィールド
REQUIRED_PLUGIN_FIELDS = {"name", "version", "description"}


# ── ヘルパー ──────────────────────────────────────────


def _load_json(path: Path) -> dict:
    """JSON ファイルを読み込んで dict を返す"""
    return json.loads(path.read_text(encoding="utf-8"))


def _discover_plugin_dirs() -> list[Path]:
    """plugins/ 配下のプラグインディレクトリ一覧を返す"""
    return sorted(
        d for d in PLUGINS_DIR.iterdir()
        if d.is_dir() and (d / ".claude-plugin" / "plugin.json").exists()
    )


def _load_marketplace() -> dict:
    """marketplace.json を読み込む"""
    return _load_json(MARKETPLACE_JSON)


# ── テストパラメータ ──────────────────────────────────


PLUGIN_DIRS = _discover_plugin_dirs()
PLUGIN_IDS = [d.name for d in PLUGIN_DIRS]


# ── marketplace.json テスト ───────────────────────────


class TestMarketplaceJson:
    """marketplace.json 自体のバリデーション"""

    def test_marketplace_json_exists(self):
        """marketplace.json が存在すること"""
        assert MARKETPLACE_JSON.exists(), f"{MARKETPLACE_JSON} が見つかりません"

    def test_marketplace_json_is_valid_json(self):
        """marketplace.json が正しい JSON であること"""
        _load_marketplace()

    def test_marketplace_has_required_fields(self):
        """marketplace.json に必須フィールドがあること"""
        data = _load_marketplace()
        for field in ("name", "description", "plugins"):
            assert field in data, f"marketplace.json に '{field}' フィールドがありません"

    def test_marketplace_plugins_is_list(self):
        """plugins が配列であること"""
        data = _load_marketplace()
        assert isinstance(data["plugins"], list), "plugins は配列である必要があります"

    def test_marketplace_plugin_entries_have_required_fields(self):
        """marketplace.json の各 plugin エントリに必須フィールドがあること"""
        data = _load_marketplace()
        required = {"name", "version", "description", "source"}
        for entry in data["plugins"]:
            missing = required - set(entry.keys())
            assert not missing, (
                f"marketplace.json の '{entry.get('name', '?')}' に "
                f"必須フィールドがありません: {missing}"
            )

    def test_marketplace_no_duplicate_plugin_names(self):
        """marketplace.json にプラグイン名の重複がないこと"""
        data = _load_marketplace()
        names = [p["name"] for p in data["plugins"]]
        duplicates = [n for n in names if names.count(n) > 1]
        assert not duplicates, f"プラグイン名が重複しています: {set(duplicates)}"


# ── plugin.json テスト ────────────────────────────────


class TestPluginJson:
    """各プラグインの plugin.json のバリデーション"""

    @pytest.mark.parametrize("plugin_dir", PLUGIN_DIRS, ids=PLUGIN_IDS)
    def test_plugin_json_is_valid_json(self, plugin_dir: Path):
        """plugin.json が正しい JSON であること"""
        path = plugin_dir / ".claude-plugin" / "plugin.json"
        _load_json(path)

    @pytest.mark.parametrize("plugin_dir", PLUGIN_DIRS, ids=PLUGIN_IDS)
    def test_plugin_json_has_required_fields(self, plugin_dir: Path):
        """plugin.json に必須フィールドがあること"""
        path = plugin_dir / ".claude-plugin" / "plugin.json"
        data = _load_json(path)
        missing = REQUIRED_PLUGIN_FIELDS - set(data.keys())
        assert not missing, (
            f"{plugin_dir.name}/plugin.json に必須フィールドがありません: {missing}"
        )

    @pytest.mark.parametrize("plugin_dir", PLUGIN_DIRS, ids=PLUGIN_IDS)
    def test_plugin_name_matches_directory(self, plugin_dir: Path):
        """plugin.json の name がディレクトリ名と一致すること"""
        path = plugin_dir / ".claude-plugin" / "plugin.json"
        data = _load_json(path)
        assert data["name"] == plugin_dir.name, (
            f"plugin.json の name '{data['name']}' が "
            f"ディレクトリ名 '{plugin_dir.name}' と一致しません"
        )

    @pytest.mark.parametrize("plugin_dir", PLUGIN_DIRS, ids=PLUGIN_IDS)
    def test_plugin_name_has_shiiman_prefix(self, plugin_dir: Path):
        """プラグイン名が shiiman- プレフィックスを持つこと"""
        path = plugin_dir / ".claude-plugin" / "plugin.json"
        data = _load_json(path)
        assert data["name"].startswith("shiiman-"), (
            f"プラグイン名 '{data['name']}' は 'shiiman-' で始まる必要があります"
        )

    @pytest.mark.parametrize("plugin_dir", PLUGIN_DIRS, ids=PLUGIN_IDS)
    def test_version_is_semver(self, plugin_dir: Path):
        """バージョンが SemVer 形式であること"""
        import re
        path = plugin_dir / ".claude-plugin" / "plugin.json"
        data = _load_json(path)
        version = data["version"]
        assert re.match(r"^\d+\.\d+\.\d+$", version), (
            f"{plugin_dir.name} のバージョン '{version}' が SemVer 形式ではありません"
        )


# ── バージョン一致テスト ──────────────────────────────


class TestVersionConsistency:
    """plugin.json と marketplace.json のバージョン一致を検証"""

    @pytest.fixture(scope="class")
    def marketplace_versions(self) -> dict[str, str]:
        """marketplace.json のプラグイン名 → バージョンマッピング"""
        data = _load_marketplace()
        return {p["name"]: p["version"] for p in data["plugins"]}

    @pytest.mark.parametrize("plugin_dir", PLUGIN_DIRS, ids=PLUGIN_IDS)
    def test_version_matches_marketplace(
        self, plugin_dir: Path, marketplace_versions: dict[str, str]
    ):
        """plugin.json のバージョンが marketplace.json と一致すること"""
        path = plugin_dir / ".claude-plugin" / "plugin.json"
        data = _load_json(path)
        name = data["name"]

        assert name in marketplace_versions, (
            f"'{name}' が marketplace.json に登録されていません"
        )
        assert data["version"] == marketplace_versions[name], (
            f"'{name}' のバージョン不一致: "
            f"plugin.json={data['version']}, "
            f"marketplace.json={marketplace_versions[name]}"
        )

    @pytest.mark.parametrize("plugin_dir", PLUGIN_DIRS, ids=PLUGIN_IDS)
    def test_description_matches_marketplace(
        self, plugin_dir: Path, marketplace_versions: dict[str, str]
    ):
        """plugin.json の description が marketplace.json と一致すること"""
        marketplace_data = _load_marketplace()
        marketplace_descs = {p["name"]: p["description"] for p in marketplace_data["plugins"]}

        path = plugin_dir / ".claude-plugin" / "plugin.json"
        data = _load_json(path)
        name = data["name"]

        if name not in marketplace_descs:
            pytest.skip(f"'{name}' が marketplace.json に未登録")

        assert data["description"] == marketplace_descs[name], (
            f"'{name}' の description 不一致:\n"
            f"  plugin.json:      {data['description']}\n"
            f"  marketplace.json: {marketplace_descs[name]}"
        )


# ── 網羅性テスト ──────────────────────────────────────


class TestCoverage:
    """plugins/ と marketplace.json の網羅性を検証"""

    def test_all_plugins_registered_in_marketplace(self):
        """全プラグインが marketplace.json に登録されていること"""
        data = _load_marketplace()
        marketplace_names = {p["name"] for p in data["plugins"]}
        plugin_names = {d.name for d in PLUGIN_DIRS}

        missing = plugin_names - marketplace_names
        assert not missing, (
            f"marketplace.json に未登録のプラグイン: {missing}"
        )

    def test_marketplace_entries_have_existing_plugins(self):
        """marketplace.json のエントリに対応するプラグインが存在すること"""
        data = _load_marketplace()
        marketplace_names = {p["name"] for p in data["plugins"]}
        plugin_names = {d.name for d in PLUGIN_DIRS}

        orphaned = marketplace_names - plugin_names
        assert not orphaned, (
            f"対応するプラグインが存在しない marketplace エントリ: {orphaned}"
        )

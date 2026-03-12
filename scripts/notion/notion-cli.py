#!/usr/bin/env python3
"""
notion-cli -- Notion API Abstraktionsschicht

Ersetzt den Notion MCP Server. Stabile CLI fuer Skills und Agents.
Notion API Version: 2022-06-28

Usage:
    notion-cli <command> [options]

Commands:
    create-page   Seite in Datenbank erstellen
    update-page   Properties einer Seite aktualisieren
    add-blocks    Bloecke zu einer Seite hinzufuegen
    search        Suche nach Titel
    query-db      Datenbank abfragen mit Filter
    get-page      Seite lesen (Properties)
    get-blocks    Block-Children lesen
    update-block  Einzelnen Block aktualisieren
    delete-block  Block loeschen
    config        Konfiguration verwalten (init, add-db, list-dbs, set-token)

Konfiguration:
    ~/.config/notion-cli/config.json (Token + DB-Registry)
    Erstmalig: notion-cli config init
"""

import sys
import os
import json
import argparse
from pathlib import Path

# Adjust path to use project venv
SCRIPT_DIR = Path(__file__).resolve().parent
VENV_PACKAGES = SCRIPT_DIR.parent / ".venv" / "lib"
for p in VENV_PACKAGES.glob("python*/site-packages"):
    sys.path.insert(0, str(p))

import requests

# --- Konstanten ---

API_BASE = "https://api.notion.com/v1"
API_VERSION = "2022-06-28"
CONFIG_DIR = Path.home() / ".config" / "notion-cli"
CONFIG_FILE = CONFIG_DIR / "config.json"

SUPPORTED_BLOCK_TYPES = {
    "paragraph", "heading_1", "heading_2", "heading_3",
    "bulleted_list_item", "numbered_list_item", "to_do",
    "toggle", "code", "quote", "callout", "divider",
    "image", "bookmark", "embed",
}


# --- Config ---

def load_config():
    """Laedt config.json. Gibt leeres Dict zurueck wenn nicht vorhanden."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


def save_config(config):
    """Schreibt config.json."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    # Restrict permissions (contains token)
    CONFIG_FILE.chmod(0o600)


def get_token():
    """Token aus Config oder Env-Variable."""
    # Env hat Vorrang (fuer CI/Scripts)
    token = os.environ.get("NOTION_TOKEN")
    if token:
        return token
    config = load_config()
    token = config.get("token")
    if token:
        return token
    print(json.dumps({"error": "Kein Token. Setze NOTION_TOKEN oder fuehre 'notion-cli config init' aus."}),
          file=sys.stderr)
    sys.exit(1)


def resolve_db_id(db_ref):
    """Loest DB-Name oder ID auf. Name schaut in Config nach, UUID wird direkt verwendet."""
    if not db_ref:
        config = load_config()
        default = config.get("default_db")
        if default:
            dbs = config.get("databases", {})
            if default in dbs:
                return dbs[default]["id"]
        return None
    # Wenn es wie eine UUID aussieht, direkt verwenden
    if len(db_ref) >= 32 and "-" in db_ref:
        return db_ref
    # Sonst als Name in Config nachschlagen
    config = load_config()
    dbs = config.get("databases", {})
    if db_ref in dbs:
        return dbs[db_ref]["id"]
    print(json.dumps({"error": f"Datenbank '{db_ref}' nicht in Config. Verfuegbar: {list(dbs.keys())}"}),
          file=sys.stderr)
    sys.exit(1)


# --- HTTP-Client ---

def get_headers():
    token = get_token()
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": API_VERSION,
        "Content-Type": "application/json",
    }


def api_get(path, params=None):
    resp = requests.get(f"{API_BASE}{path}", headers=get_headers(), params=params)
    resp.raise_for_status()
    return resp.json()


def api_post(path, body):
    resp = requests.post(f"{API_BASE}{path}", headers=get_headers(), json=body)
    resp.raise_for_status()
    return resp.json()


def api_patch(path, body):
    resp = requests.patch(f"{API_BASE}{path}", headers=get_headers(), json=body)
    resp.raise_for_status()
    return resp.json()


def api_delete(path):
    resp = requests.delete(f"{API_BASE}{path}", headers=get_headers())
    resp.raise_for_status()
    return resp.json()


# --- Block-Builder ---

def build_rich_text(text):
    """Wandelt String in Notion-RichText-Objekt um."""
    return [{"type": "text", "text": {"content": text}}]


def build_block(block_type, content):
    """
    Baut ein Notion-Block-Objekt.

    content-Format je nach block_type:
      - paragraph / heading_* / bulleted_list_item / numbered_list_item /
        to_do / toggle / quote / callout:
          String oder {"text": str, "checked": bool (nur to_do)}
      - code:
          {"text": str, "language": str}
      - divider:
          content wird ignoriert
      - image / bookmark / embed:
          {"url": str} oder String (URL)
    """
    if block_type not in SUPPORTED_BLOCK_TYPES:
        raise ValueError(f"Unbekannter Block-Typ: {block_type}. "
                         f"Erlaubt: {sorted(SUPPORTED_BLOCK_TYPES)}")

    if block_type == "divider":
        return {"type": "divider", "divider": {}}

    if block_type in ("image", "bookmark", "embed"):
        url = content if isinstance(content, str) else content["url"]
        return {"type": block_type, block_type: {"type": "external", "external": {"url": url}}}

    if block_type == "code":
        text = content if isinstance(content, str) else content.get("text", "")
        lang = content.get("language", "plain text") if isinstance(content, dict) else "plain text"
        return {"type": "code", "code": {
            "rich_text": build_rich_text(text),
            "language": lang,
        }}

    # Alle Text-Blocks
    text = content if isinstance(content, str) else content.get("text", "")
    block_body = {"rich_text": build_rich_text(text)}

    if block_type == "to_do":
        checked = content.get("checked", False) if isinstance(content, dict) else False
        block_body["checked"] = checked

    return {"type": block_type, block_type: block_body}


# --- API Commands ---

def cmd_create_page(args):
    """Seite in einer Datenbank erstellen."""
    db_id = resolve_db_id(args.db)
    if not db_id:
        print(json.dumps({"error": "Keine Datenbank angegeben und kein Default gesetzt."}), file=sys.stderr)
        sys.exit(1)
    properties = json.loads(args.properties) if args.properties else {}
    body = {
        "parent": {"database_id": db_id},
        "properties": properties,
    }
    result = api_post("/pages", body)
    return {
        "page_id": result["id"],
        "url": result.get("url"),
    }


def cmd_update_page(args):
    """Properties einer Seite aktualisieren."""
    properties = json.loads(args.properties)
    result = api_patch(f"/pages/{args.page_id}", {"properties": properties})
    return {"page_id": result["id"], "updated": True}


def cmd_add_blocks(args):
    """Bloecke zu einer Seite hinzufuegen."""
    blocks_input = json.loads(args.blocks)
    children = []
    for item in blocks_input:
        block_type = item.get("type", "paragraph")
        content = item.get("content", "")
        children.append(build_block(block_type, content))

    body = {"children": children}
    if args.after:
        body["after"] = args.after

    result = api_patch(f"/blocks/{args.page_id}/children", body)
    return {
        "page_id": args.page_id,
        "blocks_added": len(children),
        "block_ids": [b["id"] for b in result.get("results", [])],
    }


def cmd_search(args):
    """Suche nach Titel."""
    body = {
        "query": args.query,
        "page_size": args.limit or 10,
    }
    if args.filter_type:
        body["filter"] = {"value": args.filter_type, "property": "object"}
    result = api_post("/search", body)
    items = []
    for obj in result.get("results", []):
        title = ""
        if obj["object"] == "page":
            for val in obj.get("properties", {}).values():
                if val.get("type") == "title":
                    title = "".join(p.get("plain_text", "") for p in val.get("title", []))
                    break
        elif obj["object"] in ("database", "data_source"):
            parts = obj.get("title", []) or obj.get("name", [])
            title = "".join(p.get("plain_text", "") for p in parts)
        items.append({
            "id": obj["id"],
            "object": obj["object"],
            "title": title,
            "url": obj.get("url"),
        })
    return {"results": items, "count": len(items)}


def cmd_query_db(args):
    """Datenbank abfragen."""
    db_id = resolve_db_id(args.db)
    if not db_id:
        print(json.dumps({"error": "Keine Datenbank angegeben und kein Default gesetzt."}), file=sys.stderr)
        sys.exit(1)
    body = {"page_size": args.limit or 100}
    if args.filter:
        body["filter"] = json.loads(args.filter)
    if args.sorts:
        body["sorts"] = json.loads(args.sorts)

    # filter_properties gehoert in URL-Parameter, nicht Body
    params = {}
    if args.properties:
        props = json.loads(args.properties)
        params["filter_properties"] = props

    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": API_VERSION,
        "Content-Type": "application/json",
    }
    resp = requests.post(f"{API_BASE}/databases/{db_id}/query",
                         headers=headers, json=body, params=params)
    resp.raise_for_status()
    result = resp.json()
    pages = []
    for page in result.get("results", []):
        pages.append({
            "id": page["id"],
            "url": page.get("url"),
            "properties": page.get("properties", {}),
        })
    return {
        "results": pages,
        "count": len(pages),
        "has_more": result.get("has_more", False),
        "next_cursor": result.get("next_cursor"),
    }


def cmd_get_page(args):
    """Seite lesen (Properties)."""
    params = {}
    if args.properties:
        params["filter_properties"] = args.properties.split(",")
    result = api_get(f"/pages/{args.page_id}", params=params)
    return {
        "id": result["id"],
        "url": result.get("url"),
        "properties": result.get("properties", {}),
    }


def cmd_get_blocks(args):
    """Block-Children lesen."""
    params = {"page_size": args.limit or 100}
    if args.cursor:
        params["start_cursor"] = args.cursor
    result = api_get(f"/blocks/{args.page_id}/children", params=params)
    blocks = []
    for block in result.get("results", []):
        block_type = block["type"]
        content_obj = block.get(block_type, {})
        rich = content_obj.get("rich_text", [])
        plain_text = "".join(r.get("plain_text", "") for r in rich)
        blocks.append({
            "id": block["id"],
            "type": block_type,
            "text": plain_text,
            "has_children": block.get("has_children", False),
        })
    return {
        "results": blocks,
        "count": len(blocks),
        "has_more": result.get("has_more", False),
        "next_cursor": result.get("next_cursor"),
    }


def cmd_update_block(args):
    """Einzelnen Block aktualisieren."""
    body = build_block(args.type, args.content)
    result = api_patch(f"/blocks/{args.block_id}", body)
    return {"block_id": result["id"], "updated": True}


def cmd_delete_block(args):
    """Block loeschen."""
    result = api_delete(f"/blocks/{args.block_id}")
    return {"block_id": result["id"], "archived": result.get("archived", True)}


# --- Config Commands ---

def cmd_config(args):
    """Konfiguration verwalten."""
    if args.config_cmd == "init":
        return config_init(args)
    elif args.config_cmd == "add-db":
        return config_add_db(args)
    elif args.config_cmd == "list-dbs":
        return config_list_dbs(args)
    elif args.config_cmd == "set-token":
        return config_set_token(args)
    elif args.config_cmd == "set-default":
        return config_set_default(args)
    elif args.config_cmd == "show":
        return config_show(args)


def config_init(args):
    """Interaktives Setup."""
    config = load_config()

    # Token
    if args.token:
        token = args.token
    else:
        token = input("Notion Integration Token: ").strip()
    if not token:
        return {"error": "Kein Token angegeben."}
    config["token"] = token

    # Datenbanken suchen
    print("\nSuche verfuegbare Datenbanken...", file=sys.stderr)
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": API_VERSION,
        "Content-Type": "application/json",
    }
    resp = requests.post(f"{API_BASE}/search", headers=headers,
                         json={"filter": {"value": "data_source", "property": "object"}, "page_size": 50})
    if resp.status_code != 200:
        # Fallback: try with "database" filter (older API)
        resp = requests.post(f"{API_BASE}/search", headers=headers,
                             json={"filter": {"value": "database", "property": "object"}, "page_size": 50})

    if resp.status_code == 200:
        results = resp.json().get("results", [])
        if results:
            print(f"\n{len(results)} Datenbank(en) gefunden:", file=sys.stderr)
            dbs = config.get("databases", {})
            for i, r in enumerate(results):
                title_parts = r.get("title", []) or r.get("name", [])
                title = "".join(p.get("plain_text", "") for p in title_parts)
                rid = r["id"]
                # Versuche die echte database_id zu finden
                parent = r.get("parent", {})
                real_db_id = parent.get("database_id", rid)
                print(f"  [{i+1}] {title} ({rid})", file=sys.stderr)

                # Auto-Name: lowercase, spaces zu dashes
                name = title.lower().replace(" ", "-").replace("[", "").replace("]", "").strip("-")
                if name and name not in dbs:
                    dbs[name] = {"id": rid, "description": title}

            config["databases"] = dbs
            if dbs and "default_db" not in config:
                first_name = list(dbs.keys())[0]
                config["default_db"] = first_name
                print(f"\nDefault-DB: {first_name}", file=sys.stderr)
        else:
            print("Keine Datenbanken gefunden. Integration mit Datenbanken teilen!", file=sys.stderr)
    else:
        print(f"Suche fehlgeschlagen (HTTP {resp.status_code}). Token pruefen.", file=sys.stderr)

    save_config(config)
    return {"status": "init complete", "config_path": str(CONFIG_FILE), "databases": list(config.get("databases", {}).keys())}


def config_add_db(args):
    """Datenbank zur Config hinzufuegen."""
    config = load_config()
    dbs = config.get("databases", {})
    dbs[args.name] = {"id": args.id, "description": args.description or ""}
    config["databases"] = dbs
    save_config(config)
    return {"added": args.name, "id": args.id}


def config_list_dbs(args):
    """Alle konfigurierten Datenbanken auflisten."""
    config = load_config()
    dbs = config.get("databases", {})
    default = config.get("default_db")
    result = []
    for name, info in dbs.items():
        result.append({
            "name": name,
            "id": info["id"],
            "description": info.get("description", ""),
            "default": name == default,
        })
    return {"databases": result}


def config_set_token(args):
    """Token setzen oder aktualisieren."""
    config = load_config()
    if args.token:
        config["token"] = args.token
    else:
        config["token"] = input("Notion Integration Token: ").strip()
    save_config(config)
    return {"status": "token updated"}


def config_set_default(args):
    """Default-Datenbank setzen."""
    config = load_config()
    dbs = config.get("databases", {})
    if args.db not in dbs:
        return {"error": f"'{args.db}' nicht in Config. Verfuegbar: {list(dbs.keys())}"}
    config["default_db"] = args.db
    save_config(config)
    return {"default_db": args.db}


def config_show(args):
    """Aktuelle Config anzeigen (Token maskiert)."""
    config = load_config()
    display = dict(config)
    if "token" in display:
        t = display["token"]
        display["token"] = t[:8] + "..." + t[-4:] if len(t) > 12 else "***"
    return {"config_path": str(CONFIG_FILE), "config": display}


# --- CLI-Parser ---

def build_parser():
    parser = argparse.ArgumentParser(
        description="notion-cli -- Notion API Abstraktionsschicht",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--pretty", action="store_true",
                        help="JSON-Output mit Einrueckung")
    sub = parser.add_subparsers(dest="command", required=True)

    # create-page
    p = sub.add_parser("create-page", help="Seite in Datenbank erstellen")
    p.add_argument("--db", help="DB-Name oder ID (Default: config default_db)")
    p.add_argument("--properties", help="Properties als JSON-Objekt")

    # update-page
    p = sub.add_parser("update-page", help="Properties aktualisieren")
    p.add_argument("page_id", help="Notion Page ID")
    p.add_argument("--properties", required=True, help="Properties als JSON-Objekt")

    # add-blocks
    p = sub.add_parser("add-blocks", help="Bloecke hinzufuegen")
    p.add_argument("page_id", help="Page oder Block ID")
    p.add_argument("--blocks", required=True,
                   help='JSON-Array: [{"type": "heading_2", "content": "Titel"}, ...]')
    p.add_argument("--after", help="Block-ID nach der eingefuegt werden soll")

    # search
    p = sub.add_parser("search", help="Suche nach Titel")
    p.add_argument("query", help="Suchbegriff")
    p.add_argument("--filter-type", choices=["page", "database", "data_source"],
                   help="Nur Pages oder nur Databases")
    p.add_argument("--limit", type=int, default=10, help="Max. Ergebnisse")

    # query-db
    p = sub.add_parser("query-db", help="Datenbank abfragen")
    p.add_argument("--db", help="DB-Name oder ID (Default: config default_db)")
    p.add_argument("--filter", help="Filter als JSON")
    p.add_argument("--sorts", help="Sortierung als JSON-Array")
    p.add_argument("--properties", help="Filter-Properties als JSON-Array (Token sparen)")
    p.add_argument("--limit", type=int, default=100, help="Max. Ergebnisse")

    # get-page
    p = sub.add_parser("get-page", help="Seite lesen (Properties)")
    p.add_argument("page_id", help="Notion Page ID")
    p.add_argument("--properties", help="Kommagetrennte Property-IDs")

    # get-blocks
    p = sub.add_parser("get-blocks", help="Block-Children lesen")
    p.add_argument("page_id", help="Page oder Block ID")
    p.add_argument("--limit", type=int, default=100, help="Max. Bloecke")
    p.add_argument("--cursor", help="Pagination Cursor")

    # update-block
    p = sub.add_parser("update-block", help="Block aktualisieren")
    p.add_argument("block_id", help="Block ID")
    p.add_argument("--type", required=True, help="Block-Typ")
    p.add_argument("--content", required=True, help="Neuer Inhalt")

    # delete-block
    p = sub.add_parser("delete-block", help="Block loeschen")
    p.add_argument("block_id", help="Block ID")

    # config
    p = sub.add_parser("config", help="Konfiguration verwalten")
    config_sub = p.add_subparsers(dest="config_cmd", required=True)

    cp = config_sub.add_parser("init", help="Interaktives Setup")
    cp.add_argument("--token", help="Token direkt angeben (statt interaktiv)")

    cp = config_sub.add_parser("add-db", help="Datenbank hinzufuegen")
    cp.add_argument("--name", required=True, help="Kurzname (z.B. all-notes)")
    cp.add_argument("--id", required=True, help="Notion Database ID")
    cp.add_argument("--description", help="Beschreibung")

    config_sub.add_parser("list-dbs", help="Datenbanken auflisten")

    cp = config_sub.add_parser("set-token", help="Token setzen")
    cp.add_argument("--token", help="Token direkt angeben")

    cp = config_sub.add_parser("set-default", help="Default-DB setzen")
    cp.add_argument("--db", required=True, help="DB-Name")

    config_sub.add_parser("show", help="Config anzeigen (Token maskiert)")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    commands = {
        "create-page": cmd_create_page,
        "update-page": cmd_update_page,
        "add-blocks": cmd_add_blocks,
        "search": cmd_search,
        "query-db": cmd_query_db,
        "get-page": cmd_get_page,
        "get-blocks": cmd_get_blocks,
        "update-block": cmd_update_block,
        "delete-block": cmd_delete_block,
        "config": cmd_config,
    }

    try:
        result = commands[args.command](args)
        if result is not None:
            if args.pretty:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(json.dumps(result, ensure_ascii=False))
    except requests.HTTPError as e:
        error = {"error": str(e), "status": e.response.status_code if e.response else None}
        try:
            error["detail"] = e.response.json()
        except Exception:
            pass
        print(json.dumps(error, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

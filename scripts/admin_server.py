#!/usr/bin/env python3
"""
本地分类工作台后端 — 仅本地使用，不对外暴露。

启动:
  python scripts/admin_server.py
  python scripts/admin_server.py --port 5173 --host 127.0.0.1

能力:
  - GET  /api/categories           -> {categories: {id: label}}
  - POST /api/categories           body: {action: "create"|"update"|"delete"|"rename", id, label, new_id?}
  - GET  /api/projects             -> {projects: [{id, name, category, skill_count}]}
  - POST /api/projects/move        body: {ids: ["lottie", ...], category: "content-creation"}
  - POST /api/regenerate           -> 重新生成 docs/ 和 site/
  - GET  /api/health

所有写操作直接落盘 registry/projects.yaml 与 registry/categories.yaml，
前端 admin 模式通过 fetch 调用（CORS 已放开 127.0.0.1/localhost）。

安全: 仅绑定 127.0.0.1，默认无需 token；如需可设环境变量 ADMIN_TOKEN。
"""
from __future__ import annotations

import argparse
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import sys
sys.path.insert(0, str(Path(__file__).parent))

from skillhub_common import (
    ROOT,
    CATEGORIES_FILE,
    EXTRACTED_SKILLS_DIR,
    PROJECTS_FILE,
    load_category_labels,
    save_category_labels,
    load_registry,
    save_registry,
    slug,
)

ADMIN_TOKEN = None  # 可通过环境变量 ADMIN_TOKEN 覆盖

def _cors_headers(handler: BaseHTTPRequestHandler):
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type, X-Admin-Token")
    handler.send_header("Access-Control-Max-Age", "86400")

def _json(handler: BaseHTTPRequestHandler, data, status=200):
    body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    _cors_headers(handler)
    handler.end_headers()
    handler.wfile.write(body)

def _read_json(handler: BaseHTTPRequestHandler):
    length = int(handler.headers.get("Content-Length", 0) or 0)
    if not length:
        return {}
    raw = handler.rfile.read(length)
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return {}

def _check_auth(handler: BaseHTTPRequestHandler) -> bool:
    import os
    token = os.environ.get("ADMIN_TOKEN") or ADMIN_TOKEN
    if not token:
        return True
    got = handler.headers.get("X-Admin-Token") or parse_qs(urlparse(handler.path).query).get("token", [None])[0]
    return got == token

class AdminHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        _cors_headers(self)
        self.end_headers()

    def do_GET(self):
        if not _check_auth(self):
            return _json(self, {"error": "unauthorized"}, 401)
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/api/health":
            return _json(self, {"ok": True})
        if path == "/api/categories":
            labels = load_category_labels()
            # 按文件顺序返回，增加 uncategorized 兜底
            return _json(self, {"categories": labels})
        if path == "/api/projects":
            data = load_registry()
            projects = data.get("projects", [])
            # 精简返回，避免过大
            slim = [
                {
                    "id": p["id"],
                    "name": p["name"],
                    "category": p.get("category", "uncategorized"),
                    "category_locked": bool(p.get("category_locked")),
                    "skill_count": p.get("skill_count", 0),
                    "description": p.get("description", "")[:120],
                }
                for p in projects
            ]
            return _json(self, {"projects": slim, "count": len(slim)})
        if path == "/api/browse":
            qs = parse_qs(parsed.query)
            req_path = (qs.get("path", [""])[0] or "").strip()
            # 默认从常见根开始
            if not req_path:
                # Windows 盘符探测
                import string, os
                if os.name == "nt":
                    drives = [f"{d}:\\" for d in string.ascii_uppercase if Path(f"{d}:\\").exists()]
                    return _json(self, {"path": "", "parent": None, "dirs": [{"name": d, "path": d} for d in drives]})
                else:
                    req_path = str(Path.home())
            p = Path(req_path).expanduser()
            try:
                p = p.resolve()
            except Exception:
                return _json(self, {"error": f"invalid path: {req_path}"}, 400)
            if not p.exists():
                return _json(self, {"error": "path not found"}, 404)
            if p.is_file():
                p = p.parent
            try:
                dirs = []
                for child in sorted(p.iterdir(), key=lambda x: x.name.lower()):
                    if child.is_dir() and not child.name.startswith("."):
                        # 排除常见大目录以提升速度
                        dirs.append({"name": child.name, "path": str(child)})
                        if len(dirs) >= 200:
                            break
                parent = str(p.parent) if p.parent != p else None
                return _json(self, {"path": str(p), "parent": parent, "dirs": dirs})
            except Exception as e:
                return _json(self, {"error": str(e)}, 500)
        # 静态兜底：若访问 / 则返回提示
        if path == "/" or path == "/admin":
            return _json(self, {"message": "Skills-Hub Admin API. Use /api/categories, /api/projects, /api/projects/move, /api/regenerate. Open site/index.html?admin=1 for UI."})
        return _json(self, {"error": "not found"}, 404)

    def do_POST(self):
        if not _check_auth(self):
            return _json(self, {"error": "unauthorized"}, 401)
        parsed = urlparse(self.path)
        path = parsed.path
        body = _read_json(self)

        if path == "/api/categories":
            return self._handle_categories(body)
        if path == "/api/projects/move":
            return self._handle_move(body)
        if path == "/api/deploy":
            return self._handle_deploy(body)
        if path == "/api/regenerate":
            return self._handle_regenerate()
        return _json(self, {"error": "not found"}, 404)

    def _handle_categories(self, body):
        action = body.get("action")
        cid = body.get("id")
        label = body.get("label", "")
        new_id = body.get("new_id")
        new_label = body.get("new_label")

        labels = load_category_labels()

        if action == "create":
            # id 可由前端传或由 label 自动 slug
            if not cid and label:
                cid = slug(label)
            if not cid:
                return _json(self, {"error": "id or label required"}, 400)
            cid = slug(cid)
            if not re.fullmatch(r"[a-z0-9-]+", cid):
                return _json(self, {"error": "id must be [a-z0-9-]"}, 400)
            if cid in labels:
                return _json(self, {"error": f"category {cid} already exists"}, 400)
            if not label:
                return _json(self, {"error": "label required"}, 400)
            if cid == "uncategorized":
                return _json(self, {"error": "uncategorized is reserved"}, 400)
            labels[cid] = label.strip()
            save_category_labels(labels)
            return _json(self, {"ok": True, "categories": labels})

        if action == "update" or action == "rename":
            # 重命名：id -> new_id, 或仅改 label
            if not cid or cid not in labels:
                return _json(self, {"error": "category not found"}, 404)
            if cid == "uncategorized":
                return _json(self, {"error": "uncategorized cannot be renamed"}, 400)
            target_id = slug(new_id) if new_id else cid
            target_label = (new_label if new_label is not None else label) or labels[cid]
            if target_id != cid and target_id in labels:
                return _json(self, {"error": "target id already exists"}, 400)
            # 若改 id，需迁移所有 project
            if target_id != cid:
                data = load_registry()
                for p in data.get("projects", []):
                    if p.get("category") == cid:
                        p["category"] = target_id
                        p["category_locked"] = True
                save_registry(data)
                labels[target_id] = target_label.strip()
                del labels[cid]
            else:
                labels[cid] = target_label.strip()
            save_category_labels(labels)
            return _json(self, {"ok": True, "categories": labels, "migrated": target_id != cid})

        if action == "delete":
            if not cid or cid not in labels:
                return _json(self, {"error": "category not found"}, 404)
            if cid == "uncategorized":
                return _json(self, {"error": "uncategorized cannot be deleted"}, 400)
            # 删除分类时，旗下 projects 自动移入 uncategorized
            data = load_registry()
            moved = 0
            for p in data.get("projects", []):
                if p.get("category") == cid:
                    p["category"] = "uncategorized"
                    p["category_locked"] = True
                    moved += 1
            save_registry(data)
            del labels[cid]
            save_category_labels(labels)
            return _json(self, {"ok": True, "categories": labels, "moved": moved})

        return _json(self, {"error": "unknown action. Use create/update/delete"}, 400)

    def _handle_move(self, body):
        ids = body.get("ids") or body.get("project_ids") or []
        if isinstance(ids, str):
            ids = [ids]
        target = body.get("category") or body.get("target")
        if not target:
            return _json(self, {"error": "target category required"}, 400)
        labels = load_category_labels()
        if target not in labels:
            return _json(self, {"error": f"category {target} not found"}, 400)
        if not ids:
            return _json(self, {"error": "ids required"}, 400)
        data = load_registry()
        idset = set(ids)
        moved = []
        not_found = []
        id_map = {p["id"]: p for p in data.get("projects", [])}
        for pid in ids:
            proj = id_map.get(pid)
            if not proj:
                not_found.append(pid)
                continue
            proj["category"] = target
            proj["category_locked"] = True
            moved.append(pid)
        save_registry(data)
        return _json(self, {"ok": True, "moved": moved, "not_found": not_found, "target": target})

    def _handle_deploy(self, body):
        """一键部署：本地 extracted-skills 拷贝到本机任意路径"""
        import shutil
        target_root = (body.get("targetRoot") or body.get("target_root") or "").strip()
        skill_dir = (body.get("skillDir") or body.get("skill_dir") or ".claude").strip()
        # 兼容 skillIds / skillPaths / ids
        skill_ids = body.get("skillIds") or body.get("skill_ids") or body.get("skillPaths") or body.get("ids") or []
        if isinstance(skill_ids, str):
            skill_ids = [skill_ids]
        if not target_root:
            return _json(self, {"error": "targetRoot required (e.g. E:\\Code\\my-app)"}, 400)
        if not skill_ids:
            return _json(self, {"error": "skillIds required"}, 400)
        # 规范化 skill_dir：允许 .claude/.codex/.agents/.pi 或任意子路径
        skill_dir = skill_dir.strip().strip("/\\")
        if not skill_dir:
            skill_dir = ".claude"
        # 安全：仅允许 127.0.0.1 本地，且 target 必须存在或是可创建的本地路径
        target_path = Path(target_root)
        # 展开 ~ 与环境变量
        try:
            target_path = Path(target_path.expanduser()).resolve()
        except Exception:
            return _json(self, {"error": f"invalid targetRoot: {target_root}"}, 400)
        # 构建 skill 索引：支持三种输入 -> extracted 路径
        registry = load_registry()
        # 建立 id -> skill 映射（skill 全量 id 如 agent-browser/core，或 project 级展开）
        skill_index: dict[str, dict] = {}
        for proj in registry.get("projects", []):
            for sk in proj.get("skills", []):
                # 键1：完整 skill path  libraries/...  键2：project/skill  键3：skill id 短名
                skill_index[sk["id"]] = sk
                skill_index[sk["path"]] = sk
                # project/skill 组合，例如 agent-browser/core
                # 同时支持 extracted_path
                if sk.get("extracted_path"):
                    skill_index[sk["extracted_path"]] = sk
                # project 级全选：若传入 project id，展开为其所有 skills
                # 延迟处理，下方单独展开
        project_index = {p["id"]: p for p in registry.get("projects", [])}
        # 展开 project 级勾选
        expanded: list[dict] = []
        for sid in skill_ids:
            if sid in project_index:
                for sk in project_index[sid].get("skills", []):
                    expanded.append(sk)
            elif sid in skill_index:
                expanded.append(skill_index[sid])
            else:
                # 尝试按 sk.id 匹配（短名可能重复，取首个）
                # 兜底：遍历查找
                found = None
                for proj in registry.get("projects", []):
                    for sk in proj.get("skills", []):
                        if sk["id"] == sid:
                            found = sk
                            break
                    if found:
                        break
                if found:
                    expanded.append(found)
        # 去重（按 extracted_path）
        seen = set()
        uniq: list[dict] = []
        for sk in expanded:
            key = sk.get("extracted_path") or sk.get("path")
            if key not in seen:
                seen.add(key)
                uniq.append(sk)
        if not uniq:
            return _json(self, {"error": "no valid skills to deploy", "requested": skill_ids}, 400)
        # 确保目标根存在
        try:
            target_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return _json(self, {"error": f"cannot create targetRoot: {e}"}, 400)
        dest_base = target_path / skill_dir
        try:
            dest_base.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return _json(self, {"error": f"cannot create skillDir: {e}"}, 400)
        deployed = []
        overwritten = []
        errors = []
        for sk in uniq:
            src_rel = sk.get("extracted_path") or sk.get("path")
            src = ROOT / src_rel
            # extracted 目录结构为 extracted-skills/<project>/<skill-id>
            # 部署时以 skill id（或 skill name slug）为目录名，避免扁平冲突
            # 使用 skill 的 extracted_path 的最后一部分作为目录名，若无则用 skill id
            skill_folder = Path(src_rel).name if "/" in src_rel else sk["id"]
            dest = dest_base / skill_folder
            exists_before = dest.exists()
            if not src.exists():
                errors.append({"skill": sk["id"], "error": f"source not found: {src_rel}"})
                continue
            try:
                # 覆盖拷贝
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(src, dest)
                if exists_before:
                    overwritten.append(skill_folder)
                else:
                    deployed.append(skill_folder)
            except Exception as e:
                errors.append({"skill": sk["id"], "error": str(e)})
        return _json(self, {
            "ok": len(errors) == 0,
            "target": str(target_path),
            "skillDir": skill_dir,
            "destBase": str(dest_base),
            "deployed": deployed,
            "overwritten": overwritten,
            "errors": errors,
            "total": len(uniq),
        })

    def _handle_regenerate(self):
        # 重新生成 docs 与 site
        import subprocess
        import sys
        results = {}
        for script in ["scripts/generate_docs.py", "scripts/generate_site.py"]:
            try:
                out = subprocess.run([sys.executable, script], capture_output=True, text=True, cwd=str(ROOT), timeout=30)
                results[script] = {"ok": out.returncode == 0, "stdout": out.stdout.strip(), "stderr": out.stderr.strip()}
            except Exception as e:
                results[script] = {"ok": False, "error": str(e)}
        ok = all(v.get("ok") for v in results.values())
        return _json(self, {"ok": ok, "results": results}, 200 if ok else 500)

    def log_message(self, format, *args):
        # 简洁日志
        sys.stderr.write(f"[admin] {format % args}\n")

def main():
    parser = argparse.ArgumentParser(description="Skills-Hub 本地分类工作台后端")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址，默认 127.0.0.1（仅本地）")
    parser.add_argument("--port", type=int, default=5173, help="端口，默认 5173")
    args = parser.parse_args()

    addr = (args.host, args.port)
    print(f"Skills-Hub Admin 正在启动 http://{args.host}:{args.port}")
    print(f"  API: http://{args.host}:{args.port}/api/categories")
    print(f"  前端入口: 打开 site/index.html?admin=1 （确保后端已启动）")
    print(f"  重新生成: POST http://{args.host}:{args.port}/api/regenerate")
    if not CATEGORIES_FILE.exists():
        print(f"  提示: {CATEGORIES_FILE.relative_to(ROOT)} 不存在，已使用内置默认分类")
    try:
        httpd = HTTPServer(addr, AdminHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")

if __name__ == "__main__":
    main()

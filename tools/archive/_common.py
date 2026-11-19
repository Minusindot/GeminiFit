"""tools/*.py 공용 헬퍼.

- Unity 프로젝트 루트 자동 감지(이 repo는 git 루트 안에 Unity 프로젝트 폴더가 한 겹 더 있는 2중 구조라서,
  tools/ 위치에서 Assets+ProjectSettings가 있는 폴더를 찾아 내려간다).
- "Assets/..." 상대 경로 해석.
- 흰(단색) 배경 제거: 이미지 테두리와 이어진 배경색 영역만 투명하게 만든다. 흰 옷/하이라이트처럼
  캐릭터 안쪽의 흰색은 외곽선에 막혀 테두리와 이어지지 않으므로 지워지지 않는다.
"""
from __future__ import annotations

import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent


def find_unity_project() -> Path:
    """Assets/와 ProjectSettings/를 함께 가진 폴더를 찾는다(repo 루트 자신 → 바로 아래 하위 폴더 순)."""
    candidates = [REPO_ROOT] + [p for p in REPO_ROOT.iterdir() if p.is_dir() and not p.name.startswith(".")]
    for c in candidates:
        if (c / "Assets").is_dir() and (c / "ProjectSettings").is_dir():
            return c
    sys.exit(f"[tools] Unity 프로젝트 폴더를 찾지 못했습니다: {REPO_ROOT}")


def resolve_asset_path(path_str: str) -> Path:
    """'Assets/...'로 시작하면 Unity 프로젝트 기준, 절대 경로면 그대로, 그 외는 현재 폴더 기준."""
    p = Path(path_str)
    if p.is_absolute():
        return p
    norm = path_str.replace("\\", "/")
    if norm.startswith("Assets/") or norm == "Assets":
        return find_unity_project() / norm
    return Path.cwd() / p


def remove_flat_background(img, threshold: int = 18, feather: float = 0.8,
                           enclosed_tolerance: int = 6, enclosed_pure_ratio: float = 0.6,
                           enclosed_min_size: int = 15, defringe: bool = True):
    """테두리와 연결된 '배경색에 가까운' 픽셀을 투명하게 만든 RGBA 이미지를 돌려준다.

    배경색은 네 모서리 픽셀의 중앙값으로 추정한다(흰 배경이 기본이지만 회색/단색 배경도 처리).
    threshold: 배경색과의 채널별 최대 차이 허용치. 외곽선이 흐릿해 옷 안쪽까지 새면 낮추고,
    배경 찌꺼기가 남으면 올린다.
    """
    import numpy as np
    from PIL import Image, ImageFilter
    from scipy import ndimage

    rgba = img.convert("RGBA")
    arr = np.asarray(rgba).astype(np.int16)
    h, w = arr.shape[:2]
    corners = np.array([arr[0, 0, :3], arr[0, w - 1, :3], arr[h - 1, 0, :3], arr[h - 1, w - 1, :3]])
    bg = np.median(corners, axis=0)

    near = (np.abs(arr[:, :, :3] - bg) <= threshold).all(axis=2)
    labels, _ = ndimage.label(near)
    border_labels = np.unique(np.concatenate([labels[0, :], labels[-1, :], labels[:, 0], labels[:, -1]]))
    border_labels = border_labels[border_labels != 0]
    background = np.isin(labels, border_labels)

    # 갇힌 배경: 머리카락 가닥/팔 사이로 보이는 배경은 테두리와 이어지지 않아 위에서 안 지워진다. 그렇다고
    # 배경색에 가까운 칸을 전부 지우면 흰 옷까지 사라지므로, 덩어리별로 "거의 완벽히 배경색인 픽셀 비율"을 본다 -
    # 배경은 단색이라 비율이 매우 높고, 흰 옷은 음영·결 때문에 낮다.
    pure = (np.abs(arr[:, :, :3] - bg) <= enclosed_tolerance).all(axis=2)
    enclosed_ids = np.setdiff1d(np.unique(labels[near & ~background]), [0])
    if len(enclosed_ids):
        sizes = ndimage.sum(np.ones_like(labels), labels, enclosed_ids)
        pure_ratio = ndimage.mean(pure, labels, enclosed_ids)
        hole_ids = enclosed_ids[(pure_ratio >= enclosed_pure_ratio) & (sizes >= enclosed_min_size)]
        background |= np.isin(labels, hole_ids)

    alpha = np.where(background, 0, 255).astype(np.uint8)

    # 디프린지: 배경과 맞닿은 가장자리 몇 픽셀(머리카락 가닥 등)은 원래 그림에서 배경색과 반쯤 섞여 그려져 있어,
    # 그대로 두면 어두운 화면 위에서 흰 테두리(헤일로)로 보인다. 그 띠 안에서는 "배경색에서 얼마나 멀어졌나"를
    # 알파로 보고(배경과의 최대 채널 차 / 배경의 여유폭), 배경색을 빼서 원래 색을 복원한다(언프리멀티플라이).
    band = ndimage.binary_dilation(background, iterations=2) & ~background
    if defringe and band.any():
        rgb = arr[:, :, :3].astype(np.float32)
        room = np.maximum(np.maximum(bg, 255 - bg), 1).astype(np.float32)  # 채널별로 배경에서 갈 수 있는 최대 거리
        est = (np.abs(rgb - bg) / room).max(axis=2).clip(0, 1)
        est = np.where(band, est, 1.0)
        a = np.maximum(est, 1e-3)[:, :, None]
        restored = ((rgb - (1 - a) * bg) / a).clip(0, 255)
        arr[:, :, :3] = np.where(band[:, :, None], restored, rgb).astype(np.int16)
        alpha = np.where(band, (est * 255).astype(np.uint8), alpha)
        rgba = Image.fromarray(arr.astype(np.uint8), "RGBA")

    alpha_img = Image.fromarray(alpha, "L")
    if feather > 0:
        # 캐릭터 쪽 가장자리만 살짝 부드럽게(계단 현상 완화). 배경 쪽으로 번지게 하면 흰 배경색이 반투명으로
        # 남아 테두리에 흰 띠(헤일로)가 생기므로, 원래 배경이던 픽셀은 계속 0으로 둔다.
        soft = np.asarray(alpha_img.filter(ImageFilter.GaussianBlur(feather)))
        alpha_img = Image.fromarray(np.where(alpha > 0, np.minimum(soft, alpha), 0).astype(np.uint8), "L")
    out = rgba.copy()
    out.putalpha(alpha_img)
    return out


def add_stroke(img, width: int, color=(238, 240, 244)):
    """알파를 원형으로 width만큼 팽창시킨 단색 테두리를 아이템 뒤에 깐다(기존 아이콘 시트의 스티커 테두리)."""
    import numpy as np
    from PIL import Image, ImageFilter
    from scipy import ndimage

    if width <= 0:
        return img
    a = np.asarray(img.getchannel("A")) > 24
    yy, xx = np.ogrid[-width:width + 1, -width:width + 1]
    grown = ndimage.binary_dilation(a, structure=(xx * xx + yy * yy <= width * width))
    mask = Image.fromarray((grown * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(0.8))
    base = Image.new("RGBA", img.size, tuple(color) + (0,))
    base.putalpha(mask)
    base.alpha_composite(img)
    return base


def clean_icon_image(img, stroke: int = 5, stroke_color=(238, 240, 244), threshold=None, scale: float = 1.0):
    """AI 아이콘(시트 또는 단일) 정리: 배경색 자동 감지 → 투명화 → (배율) → 스티커 테두리.
    검정 배경은 굵은 검은 외곽선을 지키려고 좁은 허용치(8) + 디프린지 끔, 밝은 배경은 18 + 디프린지."""
    import numpy as np
    from PIL import Image

    rgb = img.convert("RGB")
    arr = np.asarray(rgb)
    corner = np.median(np.array([arr[0, 0], arr[0, -1], arr[-1, 0], arr[-1, -1]]), axis=0)
    dark_bg = corner.max() < 60
    th = threshold if threshold is not None else (8 if dark_bg else 18)
    cut = remove_flat_background(rgb, threshold=th, defringe=not dark_bg, feather=0.6)
    if scale != 1.0:
        cut = cut.resize((round(cut.width * scale), round(cut.height * scale)), Image.LANCZOS)
    return add_stroke(cut, stroke, stroke_color), dark_bg, th


def parse_hex_color(s: str):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def alpha_bbox(img, min_alpha: int = 16):
    """알파가 min_alpha 이상인 영역의 (left, top, right, bottom). 전부 투명이면 None."""
    import numpy as np

    a = np.asarray(img.getchannel("A"))
    ys, xs = np.where(a >= min_alpha)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def refresh_hint(path: Path) -> None:
    print(f"[tools] 저장: {path}")
    print("[tools] Unity에서 Asset Database Refresh가 필요합니다(Claude는 Unity MCP refresh_unity로 동기화).")

from dash import html, dcc, no_update
import feffery_antd_components as fac
from dash.dependencies import Input, Output, State
from pathlib import Path
import re
from server import app


def _sort_key(image_path: Path) -> int:
    """
    按文件名中的数字排序，未匹配数字的图片放到末尾。
    """
    match = re.search(r"\d+", image_path.stem)
    return int(match.group()) if match else 10 ** 9


def _load_images() -> list[str]:
    photo_dir = Path("./assets/imgs/")
    if not photo_dir.exists():
        return []

    return [
        p.as_posix()
        for p in sorted(
            [p for p in photo_dir.rglob("*.*") if p.is_file()],
            key=_sort_key
        )
    ]


IMGS = _load_images()

CHART_CATEGORIES = [
    {
        "key": "line",
        "title_zh": "折线图",
        "title_en": "Line Chart",
        "icon": "antd-line-chart",
        "description_zh": "适合展示趋势变化，支持多序列对比和时间维度分析。",
        "description_en": "Good for trends over time and multi-series comparison.",
        "keywords": ["line", "trend", "timeseries", "折线", "曲线", "趋势"],
    },
    {
        "key": "scatter",
        "title_zh": "散点图",
        "title_en": "Scatter Plot",
        "icon": "antd-dot-chart",
        "description_zh": "适合观察变量相关性、离群点与聚类分布。",
        "description_en": "Great for correlation, outliers, and cluster distribution.",
        "keywords": ["scatter", "dot", "point", "散点", "点图"],
    },
    {
        "key": "heatmap",
        "title_zh": "热力图",
        "title_en": "Heatmap",
        "icon": "antd-area-chart",
        "description_zh": "适合展示二维矩阵强度、空间热点和密度变化。",
        "description_en": "Useful for matrix intensity, hotspots, and density shifts.",
        "keywords": ["heatmap", "heat", "matrix", "热点", "热力", "矩阵"],
    },
    {
        "key": "bubble",
        "title_zh": "气泡图",
        "title_en": "Bubble Chart",
        "icon": "antd-bulb",
        "description_zh": "适合展示三维信息：横轴、纵轴与气泡大小。",
        "description_en": "Shows three dimensions: x, y, and bubble size.",
        "keywords": ["bubble", "气泡", "气泡图"],
    },
    {
        "key": "bar",
        "title_zh": "柱形图",
        "title_en": "Bar Chart",
        "icon": "antd-bar-chart",
        "description_zh": "适合展示类别间数值比较，例如分组对比和排序。",
        "description_en": "Best for category comparison, grouping, and ranking.",
        "keywords": ["bar", "column", "hist", "柱", "条形", "柱形", "柱状"],
    },
    {
        "key": "tree",
        "title_zh": "进化树",
        "title_en": "Phylogenetic Tree",
        "icon": "antd-apartment",
        "description_zh": "适合展示系统发育关系、层级结构和分支演化。",
        "description_en": "Ideal for phylogeny, hierarchy, and branch evolution.",
        "keywords": ["tree", "phylo", "clade", "dendro", "进化树", "系统发育", "树图"],
    },
    {
        "key": "other",
        "title_zh": "其他图表",
        "title_en": "Other Charts",
        "icon": "antd-app-store",
        "description_zh": "未命中关键词的图片会自动归入此分类。",
        "description_en": "Images unmatched by keywords are grouped here.",
        "keywords": [],
    },
]

CATEGORY_MAP = {item["key"]: item for item in CHART_CATEGORIES}

I18N = {
    "zh": {
        "home": "主页",
        "welcome_title": "欢迎来到《在模仿中精进数据可视化》系列推文",
        "welcome_desc": "这里展示项目精选图片与可视化分类导航，你可以从左侧栏进入不同图表模块。",
        "home_count": "当前共收录 {count} 张图片，已按文件名进行自动分类。",
        "category_page": "分类页面",
        "category_count": "当前分类匹配到 {count} 张图片（依据文件名关键词自动识别）。",
        "module_note_title": "模块说明",
        "module_note_desc": "该页面展示此类型的图片 box，点击任意图片可进入独立详情页查看脚本。",
        "image_missing": "该分类暂时没有图片，请调整文件名关键词后重试。",
        "not_found": "页面不存在",
        "not_found_category": "该分类不存在。",
        "not_found_route": "未匹配到路由，请从左侧菜单重新选择。",
        "not_found_image": "未找到对应图片，请返回分类页重新选择。",
        "detail": "详情",
        "back_to_category": "← 返回该分类",
        "r_markdown": "R 脚本（Markdown）",
        "menu_home": "主页",
        "bw_mode": "黑白模式",
        "language": "语言",
        "lang_zh": "中文",
        "lang_en": "English",
        "empty_images": "当前分类没有匹配图片，请检查文件名关键词或补充图片。",
    },
    "en": {
        "home": "Home",
        "welcome_title": "Welcome to Improve Data Visualization Through Imitation",
        "welcome_desc": "Browse selected figures and enter modules from the left navigation.",
        "home_count": "A total of {count} images are currently collected and auto-categorized.",
        "category_page": "Category",
        "category_count": "{count} images matched in this category (auto detected by filename keywords).",
        "module_note_title": "Module Note",
        "module_note_desc": "This page shows image boxes. Click any image to open an individual detail page.",
        "image_missing": "No images found in this category. Please adjust filename keywords and retry.",
        "not_found": "Page Not Found",
        "not_found_category": "The category does not exist.",
        "not_found_route": "Route not found. Please reselect from the left menu.",
        "not_found_image": "Target image was not found. Please go back and select again.",
        "detail": "Detail",
        "back_to_category": "<- Back to category",
        "r_markdown": "R Script (Markdown)",
        "menu_home": "Home",
        "bw_mode": "B/W Mode",
        "language": "Language",
        "lang_zh": "中文",
        "lang_en": "English",
        "empty_images": "No images matched in this category. Please add files or adjust naming keywords.",
    },
}


def tr(lang: str, key: str, **kwargs) -> str:
    lang_key = lang if lang in I18N else "zh"
    template = I18N[lang_key].get(key, key)
    return template.format(**kwargs) if kwargs else template


def get_category_title(category_key: str, lang: str) -> str:
    category = CATEGORY_MAP.get(category_key)
    if not category:
        return tr(lang, "category_page")
    return category["title_en"] if lang == "en" else category["title_zh"]


def get_category_desc(category_key: str, lang: str) -> str:
    category = CATEGORY_MAP.get(category_key)
    if not category:
        return ""
    return category["description_en"] if lang == "en" else category["description_zh"]


def get_menu_items(lang: str) -> list[dict]:
    return [
        {"component": "Item", "props": {"key": "home", "title": tr(lang, "menu_home"), "icon": "antd-home"}},
        *[
            {
                "component": "Item",
                "props": {
                    "key": category["key"],
                    "title": category["title_en"] if lang == "en" else category["title_zh"],
                    "icon": category["icon"],
                },
            }
            for category in CHART_CATEGORIES
        ],
    ]


def get_theme_tokens(is_dark: bool) -> dict:
    if is_dark:
        return {
            "page_bg": "#0d0d0d",
            "panel_bg": "#141414",
            "card_bg": "#1f1f1f",
            "title_text": "#f5f5f5",
            "text": "#e8e8e8",
            "subtext": "#bfbfbf",
            "border": "#303030",
            "carousel_bg": "#1a1a1a",
            "empty_bg": "#222222",
        }

    return {
        "page_bg": "#f8f9fa",
        "panel_bg": "#ffffff",
        "card_bg": "#ffffff",
        "title_text": "#262626",
        "text": "#595959",
        "subtext": "#8c8c8c",
        "border": "#f0f0f0",
        "carousel_bg": "#364d79",
        "empty_bg": "#f5f5f5",
    }


DEFAULT_THEME = get_theme_tokens(False)


def _normalize_name(image_path: str) -> str:
    stem = Path(image_path).stem
    return re.sub(r"[_\-\s]+", "", stem).lower()


def _detect_category(image_path: str) -> str:
    normalized_name = _normalize_name(image_path)

    for category in CHART_CATEGORIES:
        if category["key"] == "other":
            continue

        for keyword in category["keywords"]:
            normalized_keyword = re.sub(r"[_\-\s]+", "", keyword).lower()
            if normalized_keyword and normalized_keyword in normalized_name:
                return category["key"]

    return "other"


def _group_images_by_category(images: list[str]) -> dict[str, list[str]]:
    grouped = {category["key"]: [] for category in CHART_CATEGORIES}
    for image in images:
        grouped[_detect_category(image)].append(image)

    return grouped


IMAGES_BY_CATEGORY = _group_images_by_category(IMGS)
R_MARKDOWN_DIR = Path("./public/r_scripts")

# 第三方访客地理分布组件（替换成你的统计系统嵌入地址）
VISITOR_IP_LAT = 31.2304
VISITOR_IP_LON = 121.4737
VISITOR_GEO_WIDGET_URL = f"https://maps.google.com/maps?q={VISITOR_IP_LAT},{VISITOR_IP_LON}&z=2&output=embed"

MENU_ITEMS = get_menu_items("zh")


def build_carousel(images: list[str] | None = None, lang: str = "zh", theme: dict | None = None):
    active_theme = theme or get_theme_tokens(False)
    target_images = IMGS if images is None else images

    if not target_images:
        return fac.AntdCenter(
            tr(lang, "empty_images"),
            style={
                "height": 360,
                "background": active_theme["empty_bg"],
                "borderRadius": 8,
                "color": active_theme["subtext"],
            },
        )

    return fac.AntdCarousel(
        [
            html.Div(
                html.Div(
                    fac.AntdCenter(
                        fac.AntdImage(
                            src=img,
                            preview=True,
                            style={
                                "width": "auto",
                                "height": "auto",
                                "maxWidth": "100%",
                                "maxHeight": "100%",
                                "objectFit": "contain",
                                "display": "block",
                                "margin": "0 auto",
                            },
                        ),
                        inline=True,
                        style={"width": "100%", "height": "100%"},
                    ),
                    style={
                        "width": "100%",
                        "maxWidth": "620px",
                        "height": "min(68vh, 560px)",
                        "margin": "0 auto",
                        "padding": "12px",
                        "background": "#ffffff",
                        "borderRadius": "8px",
                        "overflow": "hidden",
                    },
                ),
                style={
                    "height": "min(76vh, 640px)",
                    "padding": "24px 12px",
                    "backgroundColor": active_theme["carousel_bg"],
                    "borderRadius": 8,
                },
            )
            for img in target_images
        ],
        autoplay=True,
        autoplaySpeed=2500,
        slidesToShow=2,
        slidesToScroll=1,
        arrows=True,
    )


def _build_chart_route(category_key: str, image_index: int) -> str:
    return f"/chart/{category_key}/{image_index}"


def _load_r_markdown(category_key: str, image_path: str, lang: str) -> str:
    """
    按优先级加载 markdown：
    1) public/r_scripts/<图片名>.md
    2) public/r_scripts/<分类key>.md
    3) 默认模板 markdown
    """
    image_stem = Path(image_path).stem
    candidate_files = [
        R_MARKDOWN_DIR / f"{image_stem}.md",
        R_MARKDOWN_DIR / f"{category_key}.md",
    ]

    for file_path in candidate_files:
        if file_path.exists() and file_path.is_file():
            return file_path.read_text(encoding="utf-8")

    category_name = get_category_title(category_key, lang)
    if lang == "en":
        return f"""# {category_name} - R Script Example

Current image: `{image_stem}`

Create files under `public/r_scripts/` to override this template:

- `{image_stem}.md` (highest priority)
- `{category_key}.md`

```r
# Example: replace with your actual R script
library(ggplot2)

df <- data.frame(
  x = 1:10,
  y = c(2, 5, 3, 8, 6, 7, 4, 9, 10, 11)
)

ggplot(df, aes(x, y)) +
  geom_line(color = "#2ca9e1", linewidth = 1.2) +
  theme_minimal(base_size = 14)
```
"""

    return f"""# {category_name} - R 脚本示例

当前图片：`{image_stem}`

你可以在 `public/r_scripts/` 下创建以下文件来覆盖此模板：

- `{image_stem}.md`（优先级最高）
- `{category_key}.md`

```r
# 示例：请替换为你的真实 R 脚本
library(ggplot2)

df <- data.frame(
  x = 1:10,
  y = c(2, 5, 3, 8, 6, 7, 4, 9, 10, 11)
)

ggplot(df, aes(x, y)) +
  geom_line(color = "#2ca9e1", linewidth = 1.2) +
  theme_minimal(base_size = 14)
```
"""


def render_home_page(lang: str, theme: dict):
    home_image_count = len(IMGS)
    return html.Div(
        [
            html.H2(
                tr(lang, "welcome_title"),
                style={"marginBottom": "10px", "color": theme["title_text"]},
            ),
            html.P(
                tr(lang, "welcome_desc"),
                style={"marginBottom": "16px", "color": theme["text"]},
            ),
            html.P(
                tr(lang, "home_count", count=home_image_count),
                style={"marginBottom": "16px", "color": theme["subtext"]},
            ),
            build_carousel(lang=lang, theme=theme),
        ],
        style={"padding": "20px"},
    )


def render_category_page(menu_key: str, lang: str, theme: dict):
    category_images = IMAGES_BY_CATEGORY.get(menu_key, [])
    category_name = get_category_title(menu_key, lang)
    category_desc = get_category_desc(menu_key, lang)

    image_boxes = [
        dcc.Link(
            html.Div(
                [
                    html.Div(
                        fac.AntdImage(
                            src=image,
                            preview=True,
                            style={
                                "width": "100%",
                                "height": "100%",
                                "objectFit": "contain",
                            },
                        ),
                        style={
                            "height": "220px",
                            "background": theme["card_bg"],
                            "padding": "8px",
                            "borderRadius": "8px",
                            "border": f"1px solid {theme['border']}",
                        },
                    ),
                    html.Div(
                        f"#{index + 1} · {Path(image).stem}",
                        style={
                            "marginTop": "8px",
                            "fontSize": "13px",
                            "color": theme["text"],
                            "whiteSpace": "nowrap",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                        },
                    ),
                ],
                style={
                    "background": theme["panel_bg"],
                    "padding": "10px",
                    "borderRadius": "10px",
                    "border": f"1px solid {theme['border']}",
                },
            ),
            href=_build_chart_route(menu_key, index),
            style={"width": "calc(33.33% - 12px)", "minWidth": "240px", "textDecoration": "none"},
        )
        for index, image in enumerate(category_images)
    ]

    return html.Div(
        [
            html.H2(category_name, style={"marginBottom": "10px", "color": theme["title_text"]}),
            html.P(
                category_desc,
                style={"color": theme["text"]},
            ),
            html.P(
                tr(lang, "category_count", count=len(category_images)),
                style={"marginBottom": "16px", "color": theme["subtext"]},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H4(tr(lang, "module_note_title"), style={"color": theme["title_text"]}),
                            html.P(tr(lang, "module_note_desc"), style={"color": theme["text"]}),
                        ],
                        style={
                            "background": theme["card_bg"],
                            "border": f"1px solid {theme['border']}",
                            "borderRadius": "8px",
                            "padding": "16px",
                            "marginBottom": "16px",
                        },
                    )
                ],
                style={"marginTop": "18px"},
            ),
            html.Div(
                image_boxes
                if image_boxes
                else [
                    fac.AntdCenter(
                        tr(lang, "image_missing"),
                        style={
                            "height": 180,
                            "background": theme["empty_bg"],
                            "borderRadius": 8,
                            "color": theme["subtext"],
                        },
                    )
                ],
                style={"display": "flex", "gap": "12px", "flexWrap": "wrap", "marginTop": "16px"},
            ),
        ],
        style={"padding": "20px"},
    )


def render_chart_detail_page(category_key: str, image_index: int, lang: str, theme: dict):
    category_images = IMAGES_BY_CATEGORY.get(category_key, [])
    category_name = get_category_title(category_key, lang)

    if image_index < 0 or image_index >= len(category_images):
        return tr(lang, "not_found"), fac.AntdCenter(
            tr(lang, "not_found_image"),
            style={"height": 240, "color": theme["subtext"]},
        )

    image_path = category_images[image_index]
    markdown_content = _load_r_markdown(category_key, image_path, lang)

    content = html.Div(
        [
            dcc.Link(
                tr(lang, "back_to_category"),
                href=f"/category/{category_key}",
                style={"display": "inline-block", "marginBottom": "12px", "color": theme["text"]},
            ),
            html.H2(
                f"{category_name} · #{image_index + 1}",
                style={"marginBottom": "14px", "color": theme["title_text"]},
            ),
            html.Div(
                fac.AntdImage(
                    src=image_path,
                    preview=True,
                    style={
                        "maxWidth": "100%",
                        "maxHeight": "520px",
                        "objectFit": "contain",
                    },
                ),
                style={
                    "background": theme["card_bg"],
                    "border": f"1px solid {theme['border']}",
                    "borderRadius": "10px",
                    "padding": "16px",
                    "marginBottom": "16px",
                },
            ),
            html.Div(
                [
                    html.H3(tr(lang, "r_markdown"), style={"marginBottom": "10px", "color": theme["title_text"]}),
                    dcc.Markdown(markdown_content, style={"color": theme["text"]}),
                ],
                style={
                    "background": theme["card_bg"],
                    "border": f"1px solid {theme['border']}",
                    "borderRadius": "10px",
                    "padding": "16px",
                },
            ),
        ],
        style={"padding": "20px"},
    )

    return f"{category_name} {tr(lang, 'detail')}", content


def render_site_footer(theme: dict):
    return html.Div(
        [
            html.Div(
                [
                    fac.AntdIcon(icon="antd-copyright"),
                    html.Div(
                        "版权所有： © 公众号RPython， 邮箱：Jiawang1209@163.com",
                        style={"color": theme["title_text"], "fontSize": "14px"},
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "10px",
                    "height": "110px",
                    "padding": "0 12px",
                    "background": theme["card_bg"],
                    "border": f"1px solid {theme['border']}",
                    "borderRadius": "8px",
                    "color": theme["title_text"],
                    "flex": "1 1 50%",
                    "minWidth": "0",
                },
            ),
            html.Div(
                html.Iframe(
                    src=VISITOR_GEO_WIDGET_URL,
                    style={
                        "width": "100%",
                        "height": "110px",
                        "border": "none",
                        "borderRadius": "8px",
                        "display": "block",
                    },
                ),
                style={
                    "width": "100%",
                    "height": "110px",
                    "borderRadius": "8px",
                    "overflow": "hidden",
                    "border": f"1px solid {theme['border']}",
                    "background": theme["card_bg"],
                    "flex": "1 1 50%",
                    "minWidth": "0",
                },
            ),
        ],
        style={
            "display": "flex",
            "gap": "12px",
            "alignItems": "stretch",
            "padding": "6px 0",
        },
    )


app.layout = html.Div(
    id="app-root",
    style={"height": "100vh", "background": DEFAULT_THEME["page_bg"]},
    children=[
        dcc.Location(id="url", refresh=False),
        fac.AntdLayout(
            [
                fac.AntdSider(
                    [
                        fac.AntdButton(
                            id="menu-collapse-trigger",
                            icon=fac.AntdIcon(
                                id="menu-collapse-trigger-icon",
                                icon="antd-arrow-left",
                                style={"fontSize": "14px"},
                            ),
                            shape="circle",
                            type="text",
                            style={
                                "position": "absolute",
                                "zIndex": 1,
                                "top": 20,
                                "right": -13,
                                "boxShadow": "rgb(0 0 0 / 10%) 0px 4px 10px 0px",
                                "background": "white",
                            },
                        ),
                        fac.AntdMenu(
                            id="left-category-menu",
                            menuItems=MENU_ITEMS,
                            mode="inline",
                            theme="light",
                            defaultSelectedKey="home",
                            style={"height": "100%", "overflow": "hidden auto"},
                        ),
                    ],
                    id="left-category-sider",
                    collapsible=True,
                    collapsedWidth=60,
                    trigger=None,
                    style={
                        "position": "relative",
                        "height": "100vh",
                        "background": DEFAULT_THEME["panel_bg"],
                        "borderRight": f"1px solid {DEFAULT_THEME['border']}",
                    },
                ),
                fac.AntdLayout(
                    id="right-main-layout",
                    children=[
                        fac.AntdContent(
                            id="app-content",
                            children=html.Div(
                                [
                                    html.Div(
                                        [
                                            fac.AntdButton(
                                                id="theme-toggle-btn",
                                                icon=fac.AntdIcon(icon="antd-moon"),
                                                shape="circle",
                                                type="default",
                                                style={"marginRight": "10px"},
                                            ),
                                            fac.AntdButton(
                                                "EN/CH",
                                                id="lang-toggle-btn",
                                                type="default",
                                            ),
                                        ],
                                        id="global-controls",
                                        style={
                                            "position": "fixed",
                                            "top": "12px",
                                            "right": "20px",
                                            "zIndex": 1100,
                                            "padding": "8px 10px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "flex-end",
                                            "gap": "8px",
                                            "borderRadius": "999px",
                                            "border": f"1px solid {DEFAULT_THEME['border']}",
                                            "background": DEFAULT_THEME["panel_bg"],
                                            "boxShadow": "0 2px 10px rgba(0,0,0,0.08)",
                                            "color": DEFAULT_THEME["text"],
                                        },
                                    ),
                                    html.Div(
                                        id="page-title",
                                        children=tr("zh", "home"),
                                        style={
                                            "fontSize": "24px",
                                            "fontWeight": 600,
                                            "padding": "20px 20px 0 20px",
                                            "color": DEFAULT_THEME["title_text"],
                                        },
                                    ),
                                    html.Div(id="page-content", children=render_home_page("zh", DEFAULT_THEME)),
                                    fac.AntdFooter(
                                        id="app-footer",
                                        children=render_site_footer(DEFAULT_THEME),
                                        style={
                                            "background": DEFAULT_THEME["panel_bg"],
                                            "borderTop": f"1px solid {DEFAULT_THEME['border']}",
                                            "padding": "16px 20px 20px 20px",
                                            "marginTop": "24px",
                                        },
                                    ),
                                ]
                            ),
                            style={
                                "background": DEFAULT_THEME["page_bg"],
                                "overflow": "auto",
                                "flex": "1",
                                "minHeight": 0,
                            },
                        ),
                    ],
                    style={"height": "100vh", "display": "flex", "flexDirection": "column"},
                ),
            ],
            style={"height": "100vh"},
        ),
    ],
)


app.clientside_callback(
    """(nClicks, collapsed) => {
        return [!collapsed, collapsed ? 'antd-arrow-left' : 'antd-arrow-right'];
    }""",
    [
        Output("left-category-sider", "collapsed"),
        Output("menu-collapse-trigger-icon", "icon"),
    ],
    Input("menu-collapse-trigger", "nClicks"),
    State("left-category-sider", "collapsed"),
    prevent_initial_call=True,
)


@app.callback(
    Output("url", "pathname"),
    Input("left-category-menu", "currentKey"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def navigate_from_menu(current_key, current_pathname):
    key = current_key or "home"

    if key == "home":
        return "/"

    if key in CATEGORY_MAP:
        return f"/category/{key}"

    return current_pathname if current_pathname else no_update


@app.callback(
    Output("page-title", "children"),
    Output("page-content", "children"),
    Output("page-title", "style"),
    Output("left-category-menu", "menuItems"),
    Output("left-category-menu", "style"),
    Output("left-category-menu", "theme"),
    Output("app-root", "style"),
    Output("left-category-sider", "style"),
    Output("app-content", "style"),
    Output("app-footer", "children"),
    Output("app-footer", "style"),
    Output("global-controls", "style"),
    Input("url", "pathname"),
    Input("theme-toggle-btn", "nClicks"),
    Input("lang-toggle-btn", "nClicks"),
)
def render_by_route(pathname, theme_clicks, lang_clicks):
    normalized_path = pathname or "/"
    lang = "en" if (lang_clicks or 0) % 2 == 1 else "zh"
    is_bw_mode = (theme_clicks or 0) % 2 == 1
    theme = get_theme_tokens(is_bw_mode)
    detail_match = re.match(r"^/chart/([^/]+)/(\d+)$", normalized_path)
    category_match = re.match(r"^/category/([^/]+)$", normalized_path)

    if normalized_path in ["/", "/home"]:
        page_title = tr(lang, "home")
        page_content = render_home_page(lang, theme)
    elif category_match:
        category_key = category_match.group(1)
        if category_key in CATEGORY_MAP:
            page_title = get_category_title(category_key, lang)
            page_content = render_category_page(category_key, lang, theme)
        else:
            page_title = tr(lang, "not_found")
            page_content = fac.AntdCenter(
                tr(lang, "not_found_category"),
                style={"height": 240, "color": theme["subtext"]},
            )
    elif detail_match:
        category_key = detail_match.group(1)
        image_index = int(detail_match.group(2))
        page_title, page_content = render_chart_detail_page(category_key, image_index, lang, theme)
    else:
        page_title = tr(lang, "not_found")
        page_content = fac.AntdCenter(
            tr(lang, "not_found_route"),
            style={"height": 240, "color": theme["subtext"]},
        )

    page_title_style = {
        "fontSize": "24px",
        "fontWeight": 600,
        "padding": "20px 20px 0 20px",
        "color": theme["title_text"],
    }

    menu_style = {
        "height": "100%",
        "overflow": "hidden auto",
        "background": theme["panel_bg"],
        "color": theme["title_text"],
    }

    app_root_style = {
        "height": "100vh",
        "background": theme["page_bg"],
    }

    sider_style = {
        "position": "relative",
        "height": "100vh",
        "background": theme["panel_bg"],
        "borderRight": f"1px solid {theme['border']}",
        "color": theme["title_text"],
    }

    content_style = {
        "background": theme["page_bg"],
        "overflow": "auto",
        "flex": "1",
        "minHeight": 0,
        "color": theme["text"],
    }

    footer_style = {
        "background": theme["panel_bg"],
        "borderTop": f"1px solid {theme['border']}",
        "padding": "16px 20px 20px 20px",
    }

    controls_style = {
        "position": "fixed",
        "top": "12px",
        "right": "20px",
        "zIndex": 1100,
        "padding": "8px 10px",
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "flex-end",
        "gap": "8px",
        "borderRadius": "999px",
        "border": f"1px solid {theme['border']}",
        "background": theme["panel_bg"],
        "boxShadow": "0 2px 10px rgba(0,0,0,0.08)",
        "color": theme["text"],
    }

    return (
        page_title,
        page_content,
        page_title_style,
        get_menu_items(lang),
        menu_style,
        "dark" if is_bw_mode else "light",
        app_root_style,
        sider_style,
        content_style,
        render_site_footer(theme),
        footer_style,
        controls_style,
    )


if __name__ == "__main__":
    app.run(debug=True)

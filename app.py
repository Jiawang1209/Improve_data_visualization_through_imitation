import dash
from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash.dependencies import Input, Output, State
from pathlib import Path
import re
from server import app

# 查看所有匹配的图片
photo_dir = Path("./assets/imgs/")

imgs = [
    p.as_posix()
    for p in sorted(
        photo_dir.rglob("*.*"),
        key=lambda p: int(re.search(r'\d+', p.stem).group())
        if re.search(r'\d+', p.stem)
        else float('inf')
    )
]



# app.layout = html.Div(
#     [
#         fac.AntdCenter(
#             "",
#             style={"height": 400,
#                    "color": "#ffffff"}
#         ),
#         fac.AntdCarousel(
#             [
#                 html.Div(
#                     fac.AntdCenter(
#                         fac.AntdImage(
#                             src=i,
#                             height=500,
#                             preview=False
#                         ),
#                         inline=True,
#                         style={"margin": 100}
#                     ),
#                     style={"height": 650,
#                            "padding": "5 5 5 5 px",
#                            "backgroundColor": "#364d79"}
#                 )
#                 for i in imgs
#             ],
#             autoplay=True,
#             autoplaySpeed=2000,
#             slidesToShow=2,
#             slidesToScroll = 2
#             # autoplay={'dotDuration': True}
#         ),
#         fac.AntdCenter(
#             "",
#             style={"height": 400,
#                    "color": "#ffffff"}
#         )

#     ]

# )


app.layout = html.Div(
    [

        fac.AntdLayout(
            [
                fac.AntdSider(
                    [
                        # 自定义折叠按钮
                        fac.AntdButton(
                            id='menu-collapse-sider-custom-demo-trigger',
                            icon=fac.AntdIcon(
                                id='menu-collapse-sider-custom-demo-trigger-icon',
                                icon='antd-arrow-left',
                                style={'fontSize': '14px'},
                            ),
                            shape='circle',
                            type='text',
                            style={
                                'position': 'absolute',
                                'zIndex': 1,
                                'top': 25,
                                'right': -13,
                                'boxShadow': 'rgb(0 0 0 / 10%) 0px 4px 10px 0px',
                                'background': 'white',
                            },
                        ),
                        fac.AntdMenu(
                            menuItems=[
                                {
                                    'component': 'Item',
                                    'props': {
                                        'key': f'图标{icon}',
                                        'title': icon.replace("antd-",""),
                                        'icon': icon,
                                    },
                                }
                                for icon in [
                                    'antd-home',
                                    'antd-cloud-upload',
                                    'antd-bar-chart',
                                    'antd-pie-chart',
                                    'antd-dot-chart',
                                    'antd-line-chart',
                                    'antd-box-plot',
                                    'antd-area-chart',
                                    'antd-radar-chart',
                                    'antd-fund',
                                    'antd-apartment',
                                    'antd-app-store',
                                    'antd-app-store-add',
                                    'antd-table',
                                    'antd-bell',
                                    'antd-sliders',
                                    'antd-calculator',
                                    'antd-calendar',
                                    'antd-database',
                                    'antd-history',
                                ]
                            ],
                            mode='inline',
                            style={'height': '100%',
                                   'overflow': 'hidden auto'},
                        ),
                    ],
                    id='menu-collapse-sider-custom-demo',
                    collapsible=True,
                    collapsedWidth=60,
                    trigger=None,
                    style={'position': 'relative',
                           "height":"100vh"},
                ),
                fac.AntdContent(style={'background': '#f8f9fa'}),
            ],
            style={'height': '100%',
                   "position": "relative"},
        )

    ],
    style={"height":"100%",
           "position":"relative"}
)


app.clientside_callback(
    """(nClicks, collapsed) => {
        return [!collapsed, collapsed ? 'antd-arrow-left' : 'antd-arrow-right'];
    }""",
    [
        Output('menu-collapse-sider-custom-demo', 'collapsed'),
        Output('menu-collapse-sider-custom-demo-trigger-icon', 'icon'),
    ],
    Input('menu-collapse-sider-custom-demo-trigger', 'nClicks'),
    State('menu-collapse-sider-custom-demo', 'collapsed'),
    prevent_initial_call=True,
)

if __name__ == '__main__':
    app.run(debug=True)

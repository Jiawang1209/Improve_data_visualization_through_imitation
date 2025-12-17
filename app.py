import dash
from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc
from pathlib import Path
import re

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


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        fac.AntdCenter(
            "",
            style={"height": 400,
                   "color": "#ffffff"}
        ),
        fac.AntdCarousel(
            [
                html.Div(
                    fac.AntdCenter(
                        fac.AntdImage(
                            src=i,
                            height=500,
                            preview=False
                        ),
                        inline=True,
                        style={"margin": 100}
                    ),
                    style={"height": 650,
                           "padding": "5 5 5 5 px",
                           "backgroundColor": "#364d79"}
                )
                for i in imgs
            ],
            autoplay=True,
            autoplaySpeed=2000,
            slidesToShow=2,
            slidesToScroll = 2
            # autoplay={'dotDuration': True}
        ),
        fac.AntdCenter(
            "",
            style={"height": 400,
                   "color": "#ffffff"}
        )

    ]



)


if __name__ == '__main__':
    app.run(debug=True)

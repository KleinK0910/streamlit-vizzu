import pandas as pd
from streamlit_vizzu import Config, Data, Style, VizzuChart
import streamlit.components.v1 as components

# Include Plausible tracking code
with open('plausible/drilldown.html', "r") as f:
    html_code = f.read()
    components.html(html_code, height=0, width=0)


chart = VizzuChart(rerun_on_click=True, default_duration=1, height=380)

data_frame = pd.read_csv("data/music.csv", dtype={"Year": str})

data = Data()
data.add_data_frame(data_frame)

style = Style(
    {
        "plot": {
            "xAxis": {"label": {"angle": "-1.1"}},
            "yAxis": {"label": {"numberScale": "shortScaleSymbolUS"}},
            "marker": {
                "colorPalette": (
                    "#b74c20FF #c47f58FF #1c9761FF #ea4549FF #875792FF #3562b6FF "
                    "#ee7c34FF #efae3aFF"
                ),
                "label": {
                    "numberFormat": "prefixed",
                    "maxFractionDigits": "1",
                    "numberScale": "shortScaleSymbolUS",
                },
            },
            "paddingLeft": "8em",
        }
    }
)

chart.animate(data, style)

chart.feature("tooltip", True)
bar_clicked = chart.get("marker.categories.Year")

if bar_clicked is None:
    chart.animate(
        Data.filter(),
        Config(
            {
                "x": "Year",
                "y": "Revenue[$]",
                "sort": "none",
                "color": None,
                "label": None,
                "title": "Music Revenues",
            }
        ),
        style,
        delay="0",
    )
else:
    chart.animate(Data.filter(f"record['Year'] == '{bar_clicked}'"))
    chart.animate(
        Config.groupedColumn(
            {
                "x": "Format",
                "y": "Revenue[$]",
                "groupedBy": "Format",
                "sort": "byValue",
                "title": f"Drilldown for Year {bar_clicked}",
            }
        )
    )

chart.show()

"Click on one of the bars to see the drilldown"

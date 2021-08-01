from os import read
import dash_html_components as html

from .reading import layout as reading
from .bullets import layout as bullets
from .sleep import layout as sleep
from .Categories import layout as category

layout = html.Div(
    id="main-layout",
    children=[
        category,
        bullets,
        sleep,
        reading
    ]
)

def create_bar_graph():
    return layout

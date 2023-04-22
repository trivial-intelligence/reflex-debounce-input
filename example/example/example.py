from __future__ import annotations

import pynecone as pc

from pynecone_debounce_input import debounce_input


class State(pc.State):
    debounce_timeout: int = 500
    query: str = ""
    checked: bool = False


app = pc.App(state=State)


def debounce_controls() -> pc.Box:
    return pc.box(
        pc.text("Debounce Controls"),
        pc.text("debounce_timeout=", State.debounce_timeout),
        pc.slider(
            min_=0,
            max_=5000,
            value=State.debounce_timeout,
            on_change=State.set_debounce_timeout,
        ),
    )


def input_items() -> tuple[pc.GridItem, pc.GridItem]:
    return (
        pc.grid_item(
            pc.heading("Input"),
            debounce_input(
                pc.input(
                    placeholder="Query",
                    value=State.query,
                    on_change=State.set_query,
                ),
                debounce_timeout=State.debounce_timeout,
            ),
        ),
        pc.grid_item(
            pc.heading("Value"),
            pc.text(State.query),
        ),
    )


def textarea_items() -> tuple[pc.GridItem, pc.GridItem]:
    return (
        pc.grid_item(
            pc.heading("Textarea"),
            debounce_input(
                pc.text_area(
                    placeholder="Query (min_length=5)",
                    value=State.query,
                    on_change=State.set_query,
                ),
                debounce_timeout=State.debounce_timeout,
                min_length=5,
            ),
        ),
        pc.grid_item(
            pc.heading("Value"),
            pc.text(State.query),
        ),
    )


def checkbox_items() -> tuple[pc.GridItem, pc.GridItem]:
    return (
        pc.grid_item(
            pc.heading("Checkbox"),
            debounce_input(
                pc.checkbox(
                    value=State.checked,
                    on_change=State.set_checked,
                ),
                debounce_timeout=State.debounce_timeout,
            ),
        ),
        pc.grid_item(
            pc.heading("Value"),
            pc.cond(
                State.checked,
                pc.text("Box is Checked"),
            ),
        ),
    )


@app.add_page
def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            debounce_controls(),
            pc.grid(
                *input_items(),
                *textarea_items(),
                *checkbox_items(),
                template_columns="repeat(2, 1fr)",
                gap=5,
            ),
        ),
    )


app.compile()

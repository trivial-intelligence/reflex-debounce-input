from __future__ import annotations

import reflex as rx

from reflex_debounce_input import debounce_input


class State(rx.State):
    debounce_timeout: int = 500
    query: str = ""
    checked: bool = False


app = rx.App(state=State)


def debounce_controls() -> rx.Box:
    return rx.box(
        rx.text("Debounce Controls"),
        rx.text("debounce_timeout=", State.debounce_timeout),
        rx.slider(
            min_=0,
            max_=5000,
            value=State.debounce_timeout,
            on_change=State.set_debounce_timeout,
        ),
    )


def input_items() -> tuple[rx.GridItem, rx.GridItem]:
    return (
        rx.grid_item(
            rx.heading("Input"),
            debounce_input(
                rx.input(
                    placeholder="Query",
                    value=State.query,
                    on_change=State.set_query,
                ),
                debounce_timeout=State.debounce_timeout,
            ),
        ),
        rx.grid_item(
            rx.heading("Value"),
            rx.text(State.query),
        ),
    )


def textarea_items() -> tuple[rx.GridItem, rx.GridItem]:
    return (
        rx.grid_item(
            rx.heading("Textarea"),
            debounce_input(
                rx.text_area(
                    placeholder="Query (min_length=5)",
                    value=State.query,
                    on_change=State.set_query,
                ),
                debounce_timeout=State.debounce_timeout,
                min_length=5,
            ),
        ),
        rx.grid_item(
            rx.heading("Value"),
            rx.text(State.query),
        ),
    )


def checkbox_items() -> tuple[rx.GridItem, rx.GridItem]:
    return (
        rx.grid_item(
            rx.heading("Checkbox"),
            debounce_input(
                rx.checkbox(
                    value=State.checked,
                    on_change=State.set_checked,
                ),
                debounce_timeout=State.debounce_timeout,
            ),
        ),
        rx.grid_item(
            rx.heading("Value"),
            rx.cond(
                State.checked,
                rx.text("Box is Checked"),
            ),
        ),
    )


@app.add_page
def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            debounce_controls(),
            rx.grid(
                *input_items(),
                *textarea_items(),
                *checkbox_items(),
                template_columns="repeat(2, 1fr)",
                gap=5,
            ),
        ),
    )


app.compile()

# reflex-debounce-input

## This functionality is now built in to Reflex itself

As a result, this repo is now archived.

-------------------

[![main branch test status](https://github.com/trivial-intelligence/reflex-debounce-input/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/trivial-intelligence/reflex-debounce-input/actions/workflows/test.yml?query=branch%3Amain)
[![PyPI version](https://badge.fury.io/py/reflex-debounce-input.svg)](https://pypi.org/project/reflex-debounce-input)

A wrapper around the generic [`react-debounce-input`](https://www.npmjs.com/package/react-debounce-input) component for the
python-based full stack [reflex](https://reflex.dev) framework.

Since all events in reflex are processed on the server-side, a client-side input debounce makes the app feel much less
sluggish when working will fully controlled text inputs.

## Example

```python
import reflex as rx

from reflex_debounce_input import debounce_input

class State(rx.State):
    query: str = ""


app = rx.App(state=State)


@app.add_page
def index():
    return rx.center(
        rx.hstack(
            debounce_input(
                rx.input(
                    placeholder="Query",
                    value=State.query,
                    on_change=State.set_query,
                ),
            ),
            rx.text(State.query),
        )
    )

app.compile()
```

```console
reflex init
reflex run
```

Also work with textarea, simply pass `rx.text_area` as the child. See [larger example](./example) in the repo.

## Usage

1. Include `reflex-debounce-input` in your project `requirements.txt`.
2. Include a specific version of `react-debounce-input` in `rxconfig.py`.

```python
config = rx.Config(
    ...,
    frontend_packages=[
        "react-debounce-input@3.3.0",
    ],
)
```

3. Wrap `reflex_debounce_input.debounce_input` around the component
   to debounce (typically a `rx.input` or `rx.text_area`).

### Props

See documentation for [`react-debounce-input`](https://www.npmjs.com/package/react-debounce-input).

#### `min_length: int = 0`

Minimal length of text to start notify, if value becomes shorter then minLength (after removing some characters), there will be a notification with empty value ''.

#### `debounce_timeout: int = 100`

Notification debounce timeout in ms. If set to -1, disables automatic notification completely. Notification will only happen by pressing Enter then.

#### `force_notify_by_enter: bool = True`

Notification of current value will be sent immediately by hitting Enter key. Enabled by-default. Notification value follows the same rule as with debounced notification, so if Length is less, then minLength - empty value '' will be sent back.

NOTE: if onKeyDown callback prop was present, it will be still invoked transparently.

#### `force_notify_on_blur: bool = True`

Same as `force_notify_by_enter`, but notification will be sent when focus leaves the input field.

## Changelog

### v0.3 - 2023-05-19

* Support pynecone >= 0.1.30 (`pynecone.var` changed to `pynecone.vars`)

### v0.2 - 2023-04-24

* `import reflex_debounce_input` automatically adds `react-debounce-input` to `Config.frontend_packages`
* fix example in README, missing comma
* improve test assertions when exporting example project

### v0.1 - 2023-04-21

Initial Release

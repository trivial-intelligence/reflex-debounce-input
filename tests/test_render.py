import pytest

import pynecone as pc
from pynecone.var import BaseVar

from pynecone_debounce_input import debounce_input


def test_render_no_child():
    with pytest.raises(RuntimeError):
        _ = debounce_input().render()


def test_render_child_props():
    class S(pc.State):
        def on_change(self, v: str):
            pass

    tag = debounce_input(
        pc.input(
            foo="bar",
            baz="quuc",
            value="real",
            on_change=S.on_change,
        )
    )._render()
    assert tag.props["sx"] == {"foo": "bar", "baz": "quuc"}
    assert tag.props["value"] == BaseVar(name="real", is_local=True, is_string=False)
    assert len(tag.props["onChange"].events) == 1
    assert tag.props["onChange"].events[0].handler == S.on_change
    assert tag.contents == ""

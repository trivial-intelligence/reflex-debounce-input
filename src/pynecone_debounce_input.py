from __future__ import annotations

from typing import Any

import pynecone as pc

from pynecone.components.tags import Tag
from pynecone.var import Var


class DebounceInput(pc.Component):
    library = "react-debounce-input"
    tag = "DebounceInput"
    min_length: Var[int] = 0
    debounce_timeout: Var[int] = 100
    force_notify_by_enter: Var[bool] = True
    force_notify_on_blur: Var[bool] = True

    def _render(self) -> Tag:
        """Carry first child props directly on this tag.

        Since react-debounce-input wants to create and manage the underlying
        input component itself, we carry all props, events, and styles from
        the child, and then neuter the child's render method so it produces no output.
        """
        if not self.children:
            raise RuntimeError(
                "Provide a child for DebounceInput, such as pc.input() or pc.text_area()",
            )
        child = self.children[0]
        tag = super()._render()
        tag.add_props(
            **child.event_triggers,
            **props_not_none(child),
            sx=child.style,
            id=child.id,
            class_name=child.class_name,
            element=Var.create("{%s}" % child.tag, is_local=False, is_string=False),
        )
        # do NOT render the child, DebounceInput will create it
        object.__setattr__(child, "render", lambda: "")
        return tag


debounce_input = DebounceInput.create


def props_not_none(c: pc.Component) -> dict[str, Any]:
    cdict = {a: getattr(c, a) for a in c.get_props() if getattr(c, a, None) is not None}
    return cdict

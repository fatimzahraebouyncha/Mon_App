"""Injection du thème (CSS maison) et des réglages visuels Streamlit."""
from __future__ import annotations

import streamlit as st

from core.config import CSS_PATH


def inject_theme() -> None:
    """Charge ``assets/styles.css`` dans la page."""
    try:
        with open(CSS_PATH, "r", encoding="utf-8") as fh:
            css = fh.read()
    except OSError:
        return
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def supports(component, parameter: str) -> bool:
    """Vrai si la version de Streamlit installée accepte ce paramètre."""
    import inspect

    try:
        return parameter in inspect.signature(component).parameters
    except (TypeError, ValueError):
        return False

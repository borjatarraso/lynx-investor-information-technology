"""Entry-point registration for the Lince Investor Suite plugin system.

Exposed via ``pyproject.toml`` under the ``lynx_investor_suite.agents``
entry-point group. See :mod:`lynx_investor_core.plugins` for the
discovery contract.

The lynx_tech package does not (yet) expose APP_TAGLINE / PROG_NAME
at module level, so the plugin encodes them here directly.
"""

from __future__ import annotations

from lynx_investor_core.plugins import SectorAgent

from lynx_tech import __version__


def register() -> SectorAgent:
    """Return this agent's descriptor for the plugin registry."""
    return SectorAgent(
        name="lynx-investor-information-technology",
        short_name="tech",
        sector="Information Technology",
        tagline="Software, Semiconductors, Cloud & Hardware",
        prog_name="lynx-tech",
        version=__version__,
        package_module="lynx_tech",
        entry_point_module="lynx_tech.__main__",
        entry_point_function="main",
        icon="\U0001f4bb",  # laptop
    )

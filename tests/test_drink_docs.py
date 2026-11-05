"""Documentation pins for the Step 0 drink repairs (design 00-step0-repairs.md section 0.5).

The chef agent, the pillar and the skill are prose, so a contradiction between them cannot
fail a type check. These tests pin the repaired facts to the text: the Negroni arithmetic,
the role and family names, the real headings, the syrup default, and the family ABV bands.
The behavioral tests for the same rows are in test_drink_repairs.py.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CHEF = (ROOT / ".claude/agents/chef.md").read_text(encoding="utf-8")
PILLAR = (ROOT / "docs/pillar-source/04_beverage_craft_and_dilution.md").read_text(
    encoding="utf-8"
)
REFERENCE = (ROOT / ".claude/skills/beverage-craft/reference.md").read_text(encoding="utf-8")
SKILL = (ROOT / ".claude/skills/beverage-craft/SKILL.md").read_text(encoding="utf-8")
OVERVIEW = (ROOT / "docs/pillar-source/00_overview_and_skill_mapping.md").read_text(
    encoding="utf-8"
)


# Row a: one dilution convention ------------------------------------------------


def _finished(components: list[tuple[float, float]], dilution: float) -> tuple[float, float]:
    """(finished volume in oz, finished ABV in percent) for (volume, abv_fraction) pairs.

    The identity from beverage-craft section 5.3: dilution is a fraction of the PRE-dilution
    volume, so final_volume = undiluted x (1 + d) and ABV = ethanol / final_volume.
    """
    undiluted = sum(volume for volume, _ in components)
    ethanol = sum(volume * abv for volume, abv in components)
    final_volume = undiluted * (1 + dilution)
    return final_volume, 100 * ethanol / final_volume


def test_negroni_worked_example_is_372_oz_and_228_percent():
    negroni = [(1.0, 0.45), (1.0, 0.24), (1.0, 0.16)]
    volume, abv = _finished(negroni, 0.24)
    assert volume == pytest.approx(3.72)
    assert round(abv, 1) == 22.8
    assert 3.0 * 0.24 == pytest.approx(0.72)  # water added
    assert 0.85 / 0.6 == pytest.approx(1.4, abs=0.02)  # standard drinks


def test_the_finished_share_convention_would_have_given_a_different_drink():
    """The retired chef.md convention (water as a share of the finished drink) disagrees."""
    retired_volume = 3.0 / (1 - 0.24)
    assert round(retired_volume, 2) == 3.95
    assert round(100 * 0.85 / retired_volume, 1) == 21.5
    assert retired_volume != pytest.approx(3.72)


def test_chef_and_pillar_print_the_same_negroni():
    for text in (CHEF, PILLAR, REFERENCE):
        assert "3.72" in text
        assert "22.8%" in text
    assert "≈3.72 oz" in CHEF and "≈22.8%" in CHEF
    assert "abv_target_pct: 22.8" in CHEF
    for stale in ("3.95", "21.5%", "abv_target_pct: 21.5"):
        assert stale not in CHEF
        assert stale not in PILLAR


def test_chef_phase_6_uses_the_pre_dilution_formulas():
    assert "final_volume  = undiluted_volume × (1 + dilution_target)" in CHEF
    assert "water_added   = undiluted_volume × dilution_target" in CHEF
    assert "(1 − dilution_target)" not in CHEF
    assert "*finished* drink, which is the convention" not in CHEF


def test_dilution_target_pct_documents_its_convention():
    source = (ROOT / "src/mise_en_prompt/state.py").read_text(encoding="utf-8")
    block = source.split("dilution_target_pct: float | None = None", 1)[1][:400]
    assert "PRE-dilution volume" in block
    assert "3.72" in block


def test_reference_md_is_the_pillar_up_to_its_references_tail():
    """The skill loads reference.md; it must never drift from the pillar text it mirrors."""
    assert PILLAR.startswith(REFERENCE)
    assert "## References & Sources" in PILLAR[len(REFERENCE):]


def test_chef_md_names_the_pillar_roles():
    assert "base, modifier, sweetener, acid, bitters, lengthener, texture, aromatic_garnish" in CHEF
    assert "[base, modifier, bitter, aromatic, dilution]" not in CHEF
    assert "functional_role: sweet\n" not in CHEF
    assert "aromatic_garnish" in SKILL
    assert "`aromatic garnish`" not in SKILL


# Row g: no phantom headings in the drink sections of chef.md ------------------


@pytest.mark.parametrize(
    "phantom",
    [
        "The Drink Templates and Family Ratios",
        "Base Spirits and Congener Profiles",
        "The Eight Functional Roles",
        "Acid and Acid-Adjustment",
        "Dilution and Temperature",
        "ABV Math and Batching",
        "Diagnosing an Off-Balance Drink",
    ],
)
def test_chef_md_cites_no_phantom_heading(phantom: str):
    assert phantom not in CHEF


def _headings(text: str) -> set[str]:
    found = set()
    for line in text.splitlines():
        match = re.match(r"#{2,3} (?:Section \d+: |\d+\.\d+ )?(.*?)(?: \{#.*\})?$", line)
        if match:
            found.add(match.group(1).strip())
    return found


@pytest.mark.parametrize(
    "heading",
    [
        "Drink Families & Structural Templates",
        "Base Spirits — Structural and Aromatic Taxonomy",
        "The Modifier Roles and Which Ones Stack",
        "Acids: Juice, Isolated Acid, and Acid-Adjusting",
        "Dilution, Temperature & ABV Math",
        "Batching: Removing the Dilution Step Without Removing the Dilution",
        "Balance & the Drink Rescue Table",
        "Build Methods",
        "Allergen and Exclusion Screening",
    ],
)
def test_every_beverage_craft_heading_chef_md_cites_exists_in_reference_md(heading: str):
    assert heading in _headings(REFERENCE)
    assert heading in CHEF


# Row d: drinks do read Balance -------------------------------------------------


def test_the_overview_no_longer_says_the_food_and_drink_sets_do_not_mix():
    assert "the two sets do not mix" not in OVERVIEW
    assert "it replaces them" not in OVERVIEW
    assert "Pillar 3" in OVERVIEW.split("## Drink workflows (Pillar 4)")[1][:700]


def test_chef_md_no_longer_says_balance_transfers_unchanged():
    assert "transfers to drinks unchanged" not in CHEF
    assert "transfer to a glass unchanged" not in CHEF
    assert "ethanol and temperature corrections" in CHEF


# Rows h, k, m: saline, syrup default, scope ------------------------------------


def test_saline_is_texture_and_stated_as_weight_over_weight():
    assert "20% w/v" not in PILLAR
    assert "20 g salt dissolved in 80 g water (20% w/w)" in PILLAR
    assert "20 g salt in 80 g water, 20% w/w" in CHEF
    assert "Saline is a `texture` ingredient" in CHEF
    assert "**AROMATIC** next (bitters, expressed oils, tinctures, saline)" not in CHEF


def test_syrup_house_default_is_two_to_one_by_weight_with_the_alternative_named():
    assert "The house default is **2:1 by weight, refrigerated**" in PILLAR
    assert "the ratio most bars run day to day" not in PILLAR
    assert "1.5:1" in PILLAR.split("The house default is **2:1")[1][:900]
    assert "crystal" in PILLAR.split("The house default is **2:1")[1][:600]


def test_scope_says_production_is_explained_not_taught():
    assert "deliberately out of scope" not in PILLAR
    assert "Production is explained, not taught" in PILLAR
    assert "not a how-to for making spirits" in PILLAR or "how-to for making spirits" in PILLAR


# Row j: every band contains its members ---------------------------------------


_PERCENT = re.compile(r"(\d+(?:\.\d+)?)(?:–(\d+(?:\.\d+)?))?%")


def _table_after(text: str, marker: str) -> list[list[str]]:
    lines = text.split(marker, 1)[1].splitlines()
    rows = []
    started = False
    for line in lines:
        if line.startswith("|"):
            started = True
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not set(cells[0]) <= set("-"):
                rows.append(cells)
        elif started:
            break
    return rows[1:]  # drop the header row


def _range(cell: str, last: bool) -> tuple[float, float] | None:
    matches = _PERCENT.findall(cell)
    if not matches:
        return None
    lo, hi = matches[-1] if last else matches[0]
    return float(lo), float(hi or lo)


def test_each_family_band_contains_the_members_the_pillar_names():
    bands = {row[0]: _range(row[1], last=False) for row in _table_after(PILLAR, "**Band check.**")}
    assert len(bands) == 10
    for row in _table_after(PILLAR, "**Band check.**"):
        family, (band_lo, band_hi) = row[0], bands[row[0]]
        for cell in row[2:4]:
            member = _range(cell, last=True)
            if member is None:  # "no member in this pillar carries a figure"
                continue
            assert band_lo <= member[0] and member[1] <= band_hi, (
                f"{family}: member {cell!r} falls outside {band_lo}-{band_hi}%"
            )


def test_the_band_check_table_agrees_with_the_master_template_comparison():
    master = {
        row[0]: _range(row[7], last=False)
        for row in _table_after(PILLAR, "### 1.10 Master Template Comparison")
    }
    band_rows = _table_after(PILLAR, "**Band check.**")
    checked = {row[0]: _range(row[1], last=False) for row in band_rows}
    assert master == checked


def test_no_aperitivo_member_sits_outside_its_band():
    """The Adonis (15-16%) was the member that broke the 6-12% band; it now lives elsewhere."""
    aperitivo = PILLAR.split("### 1.9 Low-ABV Aperitivo and Spritz")[1].split("### 1.10")[0]
    assert "| Adonis |" not in aperitivo
    assert "| Sherry Cobbler |" not in aperitivo
    sparkling = PILLAR.split("### 1.7 ")[1].split("### 1.8")[0]
    assert "| Adonis |" in sparkling and "| Sherry Cobbler |" in sparkling


"""Pure, bounded arithmetic shared by the video and MCP examples."""
from __future__ import annotations


def modulo_walk(start: int = 10, steps: int = 5, modulus: int = 12) -> dict:
    """Return integer totals, residues and carries without discarding the total."""
    if any(type(x) is not int for x in (start, steps, modulus)):
        raise ValueError("start, steps and modulus must be integers")
    if not 2 <= modulus <= 24:
        raise ValueError("modulus must be between 2 and 24")
    if abs(start) > 10000 or abs(steps) > 24:
        raise ValueError("start must be within ±10000 and steps within ±24")
    direction = 1 if steps >= 0 else -1
    positions = []
    for index in range(abs(steps) + 1):
        total = start + direction * index
        quotient, residue = divmod(total, modulus)
        positions.append({"index": index, "total": total,
                          "quotient": quotient, "residue": residue})
    return {"start": start, "steps": steps, "modulus": modulus,
            "positions": positions, "final": positions[-1],
            "claim": "total = quotient * modulus + residue",
            "limit": "A residue alone does not uniquely identify an integer."}


def check_episode_plan(plan: dict) -> dict:
    """Check required fields; field presence is not scientific verification."""
    required = ("question", "why_it_matters", "demonstration", "check",
                "challenge", "sources", "unresolved")
    missing = [key for key in required if key not in plan or plan[key] is None
               or plan[key] == "" or plan[key] == []]
    return {"required_fields_present": not missing, "missing": missing,
            "scientific_claims_verified": False,
            "publication_authorized": False}

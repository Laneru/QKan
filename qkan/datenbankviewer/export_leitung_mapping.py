# export_leitung_mapping.py
import json
import os

from zustandsklassen_mapping import ZUSTAND

OUT_JSON = os.path.join(os.path.dirname(__file__), "leitung_mapping.json")


def _add_rows_for_entry(rows, gruppe, kuerzel, material, c1, c2, sb_map):
    for schutz in ("D", "S", "B"):
        s_map = sb_map.get(schutz) or {}
        if "pauschal" in s_map:
            rows.append({
                "gruppe": gruppe,
                "kuerzel": kuerzel,
                "material": material or "",
                "ch1": c1,
                "ch2": c2,
                "schutz": schutz,
                "typ": "pauschal",
                "v_min": "",
                "v_max": "",
                "klasse": str(s_map["pauschal"]),
            })
        for (mn, mx, k) in s_map.get("intervalle", []):
            rows.append({
                "gruppe": gruppe,
                "kuerzel": kuerzel,
                "material": material or "",
                "ch1": c1,
                "ch2": c2,
                "schutz": schutz,
                "typ": "intervall",
                "v_min": "" if mn is None else str(mn),
                "v_max": "" if mx is None else str(mx),
                "klasse": str(k),
            })


def export_leitung_mapping():
    rows = []

    for gruppe in ("Haltungen", "GAL"):
        gmap = ZUSTAND.get(gruppe, {})
        for kuerzel, km in gmap.items():
            # Fall 1: materialabhängig (dict mit Material-Schlüsseln, darunter (c1,c2))
            if isinstance(km, dict) and all(
                isinstance(k, str) and not isinstance(k, tuple)
                for k in km.keys()
            ):
                for material, mat_map in km.items():
                    if not isinstance(mat_map, dict):
                        continue
                    for key, sb_map in mat_map.items():
                        if not isinstance(key, tuple) or len(key) != 2:
                            continue
                        c1, c2 = key
                        _add_rows_for_entry(rows, gruppe, kuerzel, material, c1, c2, sb_map)
            else:
                # Fall 2: klassische Struktur (c1,c2) -> sb_map
                if not isinstance(km, dict):
                    continue
                for key, sb_map in km.items():
                    if not isinstance(key, tuple) or len(key) != 2:
                        # z.B. falls sich etwas anderes eingeschlichen hat
                        continue
                    c1, c2 = key
                    _add_rows_for_entry(rows, gruppe, kuerzel, "", c1, c2, sb_map)

    data = {"rows": rows}
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Leitung-Mapping exportiert nach: {OUT_JSON}")


if __name__ == "__main__":
    export_leitung_mapping()

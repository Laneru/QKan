import os
import json

MAPPING_JSON = os.path.join(os.path.dirname(__file__), "schacht_mapping.json")
MAPPING_LEITUNG = os.path.join(os.path.dirname(__file__), "leitung_mapping.json")


def _split_list(val: str):
    val = (val or "").strip()
    if not val:
        return []
    return [p.strip().upper() for p in val.split(",") if p.strip()]


def _split_list_field(val: str):
    val = (val or "").strip()
    if not val:
        return []
    return [p.strip().upper() for p in val.split(",") if p.strip()]


def load_schacht_mapping_from_json():
    if not os.path.exists(MAPPING_JSON):
        return {}

    with open(MAPPING_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = data.get("rows", [])
    from collections import defaultdict
    tmp = defaultdict(lambda: defaultdict(lambda: {"D": {}, "S": {}, "B": {}}))

    for row in rows:
        kuerzel = (row.get("kuerzel", "") or "").strip().upper()
        if not kuerzel.startswith("D"):
            continue

        c1_list = _split_list_field(row.get("ch1", ""))
        c2_list = _split_list_field(row.get("ch2", ""))
        bereich_list = _split_list_field(row.get("bereich", ""))
        schutz = (row.get("schutz", "") or "").strip().upper()
        typ = (row.get("typ", "") or "").strip().lower()
        v_min = (row.get("v_min", "") or "").strip()
        v_max = (row.get("v_max", "") or "").strip()
        klasse = (row.get("klasse", "") or "").strip()

        if not schutz or schutz not in ("D", "S", "B"):
            continue
        if not c1_list:
            c1_list = [""]
        if not c2_list:
            c2_list = [""]
        if not bereich_list:
            bereich_list = ["ALL"]

        mn = float(v_min) if v_min else None
        mx = float(v_max) if v_max else None

        for c1 in c1_list:
            for c2 in c2_list:
                bereich_group = "".join(bereich_list)
                entry = tmp[(kuerzel, c1, c2)][bereich_group][schutz]

                if typ == "pauschal":
                    if klasse != "":
                        entry["pauschal"] = int(klasse)
                elif typ == "intervall":
                    if klasse != "":
                        k = int(klasse)
                        entry.setdefault("intervalle", []).append((mn, mx, k))

    result = {}
    for (kuerzel, c1, c2), bereich_map in tmp.items():
        result.setdefault(kuerzel, {})[(c1, c2)] = dict(bereich_map)

    return result


def load_leitung_mapping_from_json():
    if not os.path.exists(MAPPING_LEITUNG):
        return {"Haltungen": {}, "GAL": {}}

    with open(MAPPING_LEITUNG, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = data.get("rows", [])
    from collections import defaultdict

    mat_tmp = {
        "Haltungen": defaultdict(lambda: defaultdict(lambda: {"D": {}, "S": {}, "B": {}})),
        "GAL": defaultdict(lambda: defaultdict(lambda: {"D": {}, "S": {}, "B": {}})),
    }
    plain_tmp = {
        "Haltungen": defaultdict(lambda: defaultdict(lambda: {"D": {}, "S": {}, "B": {}})),
        "GAL": defaultdict(lambda: defaultdict(lambda: {"D": {}, "S": {}, "B": {}})),
    }

    for row in rows:
        gruppe = (row.get("gruppe", "") or "").strip()
        if gruppe not in ("Haltungen", "GAL"):
            continue

        kuerzel = (row.get("kuerzel", "") or "").strip().upper()
        if not kuerzel:
            continue

        material = (row.get("material", "") or "").strip().lower()
        c1_list = _split_list(row.get("ch1", ""))
        c2_list = _split_list(row.get("ch2", ""))
        schutz = (row.get("schutz", "") or "").strip().upper()
        typ = (row.get("typ", "") or "").strip().lower()
        v_min = (row.get("v_min", "") or "").strip()
        v_max = (row.get("v_max", "") or "").strip()
        klasse = (row.get("klasse", "") or "").strip()

        if not schutz or schutz not in ("D", "S", "B"):
            continue
        if not c1_list:
            c1_list = [""]
        if not c2_list:
            c2_list = [""]

        mn = float(v_min) if v_min else None
        mx = float(v_max) if v_max else None

        tgt = mat_tmp[gruppe] if material else plain_tmp[gruppe]

        for c1 in c1_list:
            for c2 in c2_list:
                key = (c1, c2)
                if material:
                    entry = tgt[(kuerzel, material, key)][schutz]
                else:
                    entry = tgt[(kuerzel, key)][schutz]

                if typ == "pauschal":
                    if klasse != "":
                        entry["pauschal"] = int(klasse)
                elif typ == "intervall":
                    if klasse != "":
                        k = int(klasse)
                        entry.setdefault("intervalle", []).append((mn, mx, k))

    result_hat = {}
    result_gal = {}

    for gruppe, tmp in (("Haltungen", plain_tmp["Haltungen"]),
                        ("GAL", plain_tmp["GAL"])):
        res = result_hat if gruppe == "Haltungen" else result_gal
        for (kuerzel, key), sb in tmp.items():
            res.setdefault(kuerzel, {})
            res[kuerzel][key] = sb

    for gruppe, tmp in (("Haltungen", mat_tmp["Haltungen"]),
                        ("GAL", mat_tmp["GAL"])):
        res = result_hat if gruppe == "Haltungen" else result_gal
        for (kuerzel, material, key), sb in tmp.items():
            res.setdefault(kuerzel, {})
            res[kuerzel].setdefault(material, {})
            res[kuerzel][material][key] = sb

    return {"Haltungen": result_hat, "GAL": result_gal}


# Initialisierung
_schacht_mapping = load_schacht_mapping_from_json()
_leitung_mapping = load_leitung_mapping_from_json()

ZUSTAND = {
    "Haltungen": _leitung_mapping["Haltungen"],
    "GAL": _leitung_mapping["GAL"],
    "Schächte": _schacht_mapping,
}


def reload_schacht_mapping():
    global _schacht_mapping, ZUSTAND
    _schacht_mapping = load_schacht_mapping_from_json()
    ZUSTAND["Schächte"] = _schacht_mapping


def reload_leitung_mapping():
    global _leitung_mapping, ZUSTAND
    _leitung_mapping = load_leitung_mapping_from_json()
    ZUSTAND["Haltungen"] = _leitung_mapping["Haltungen"]
    ZUSTAND["GAL"] = _leitung_mapping["GAL"]


#### ALT ####


# def _split_list_field(val: str):
#     val = (val or "").strip()
#     if not val:
#         return []
#     return [p.strip().upper() for p in val.split(",") if p.strip()]

# def load_schacht_mapping_from_json():
#     if not os.path.exists(MAPPING_JSON):
#         return {}

#     with open(MAPPING_JSON, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     rows = data.get("rows", [])
#     from collections import defaultdict
#     tmp = defaultdict(lambda: defaultdict(lambda: {"D": {}, "S": {}, "B": {}}))

#     for row in rows:
#         kuerzel = (row.get("kuerzel", "") or "").strip().upper()
#         # nur Schachtschäden mit D*-Kürzel
#         if not kuerzel.startswith("D"):
#             continue

#         c1_list = _split_list_field(row.get("ch1", ""))
#         c2_list = _split_list_field(row.get("ch2", ""))
#         bereich_list = _split_list_field(row.get("bereich", ""))
#         schutz = (row.get("schutz", "") or "").strip().upper()
#         typ = (row.get("typ", "") or "").strip().lower()
#         v_min = (row.get("v_min", "") or "").strip()
#         v_max = (row.get("v_max", "") or "").strip()
#         klasse = (row.get("klasse", "") or "").strip()

#         if not schutz or schutz not in ("D", "S", "B"):
#             continue
#         if not c1_list:
#             c1_list = [""]
#         if not c2_list:
#             c2_list = [""]
#         if not bereich_list:
#             bereich_list = ["ALL"]

#         mn = float(v_min) if v_min else None
#         mx = float(v_max) if v_max else None

#         for c1 in c1_list:
#             for c2 in c2_list:
#                 bereich_group = "".join(bereich_list)
#                 entry = tmp[(kuerzel, c1, c2)][bereich_group][schutz]

#                 if typ == "pauschal":
#                     if klasse != "":
#                         entry["pauschal"] = int(klasse)
#                 elif typ == "intervall":
#                     if klasse != "":
#                         k = int(klasse)
#                         entry.setdefault("intervalle", []).append((mn, mx, k))

#     # Alle gefundenen Kürzel dynamisch übernehmen
#     result = {}
#     for (kuerzel, c1, c2), bereich_map in tmp.items():
#         result.setdefault(kuerzel, {})[(c1, c2)] = dict(bereich_map)

#     return result

# # in zustandsklassen_mapping.py

# def reload_schacht_mapping():
#     global _schacht_mapping, ZUSTAND
#     _schacht_mapping = load_schacht_mapping_from_json()
#     # ZUSTAND-Grundstruktur unverändert lassen, nur Schächte aktualisieren
#     ZUSTAND["Schächte"] = _schacht_mapping

# _schacht_mapping = load_schacht_mapping_from_json()

# ZUSTAND = {
#     "Haltungen": {
#         # BAA – Verformung, materialabhängig
#         "BAA": {
#             "biegeweich": {
#                 ("A", ""): {
#                     "D": {
#                         "intervalle": [
#                             (None,  2.0, 1),
#                             (2.0,   6.0, 2),
#                             (6.0,  10.0, 3),
#                             (10.0, 15.0, 4),
#                             (15.0, None, 5),
#                         ]
#                     },
#                     "S": {
#                         "intervalle": [
#                             (None,  2.0, 1),
#                             (2.0,   6.0, 2),
#                             (6.0,  10.0, 3),
#                             (10.0, 15.0, 4),
#                             (15.0, None, 5),
#                         ]
#                     },
#                     "B": {
#                         "intervalle": [
#                             (None,  2.0, 1),
#                             (2.0,   6.0, 2),
#                             (6.0,  10.0, 3),
#                             (10.0, 15.0, 4),
#                             (15.0, None, 5),
#                         ]
#                     },
#                 },
#                 ("B", ""): {
#                     "D": {
#                         "intervalle": [
#                             (None,  2.0, 1),
#                             (2.0,   6.0, 2),
#                             (6.0,  10.0, 3),
#                             (10.0, 15.0, 4),
#                             (15.0, None, 5),
#                         ]
#                     },
#                     "S": {
#                         "intervalle": [
#                             (None,  2.0, 1),
#                             (2.0,   6.0, 2),
#                             (6.0,  10.0, 3),
#                             (10.0, 15.0, 4),
#                             (15.0, None, 5),
#                         ]
#                     },
#                     "B": {
#                         "intervalle": [
#                             (None,  2.0, 1),
#                             (2.0,   6.0, 2),
#                             (6.0,  10.0, 3),
#                             (10.0, 15.0, 4),
#                             (15.0, None, 5),
#                         ]
#                     },
#                 },
#             },
#             "biegesteif": {
#                 ("A", ""): {
#                     "D": {
#                         "intervalle": [
#                             (None,  6.0, 1),
#                             (6.0,  15.0, 2),
#                             (15.0, None, 3),
#                         ]
#                     },
#                     "S": {
#                         "intervalle": [
#                             (None, 10.0, 1),
#                             (10.0, 25.0, 2),
#                             (25.0, 40.0, 3),
#                             (40.0, 50.0, 4),
#                             (50.0, None, 5),
#                         ]
#                     },
#                     "B": {
#                         "intervalle": [
#                             (None, 10.0, 1),
#                             (10.0, 25.0, 2),
#                             (25.0, 40.0, 3),
#                             (40.0, 50.0, 4),
#                             (50.0, None, 5),
#                         ]
#                     },
#                 },
#                 ("B", ""): {
#                     "D": {
#                         "intervalle": [
#                             (None,  6.0, 1),
#                             (6.0,  15.0, 2),
#                             (15.0, None, 3),
#                         ]
#                     },
#                     "S": {
#                         "intervalle": [
#                             (None, 10.0, 1),
#                             (10.0, 25.0, 2),
#                             (25.0, 40.0, 3),
#                             (40.0, 50.0, 4),
#                             (50.0, None, 5),
#                         ]
#                     },
#                     "B": {
#                         "intervalle": [
#                             (None, 10.0, 1),
#                             (10.0, 25.0, 2),
#                             (25.0, 40.0, 3),
#                             (40.0, 50.0, 4),
#                             (50.0, None, 5),
#                         ]
#                     },
#                 },
#             },
#         },
#         # BAB – Rissbildung (Tab. A-3-13)
#         "BAB": {
#             # Oberflächenriss (Ch1 = A, Ch2=A–E), pauschal
#             ("A", "A"): {"D": {"pauschal": 3}, "S": {"pauschal": 3}, "B": {"pauschal": 3}},
#             ("A", "B"): {"D": {"pauschal": 3}, "S": {"pauschal": 3}, "B": {"pauschal": 3}},
#             ("A", "C"): {"D": {"pauschal": 3}, "S": {"pauschal": 3}, "B": {"pauschal": 3}},
#             ("A", "D"): {"D": {"pauschal": 3}, "S": {"pauschal": 3}, "B": {"pauschal": 3}},
#             ("A", "E"): {"D": {"pauschal": 3}, "S": {"pauschal": 3}, "B": {"pauschal": 3}},

#             # Riss mit Klassenbereichen (Ch1 = B, Ch2 in A,C,D,E)
#             ("B", "A"): {
#                 "D": {"intervalle": [(0.5, 2.0, 2), (2.0, 5.0, 3), (5.0, 10.0, 4), (10.0, None, 5)]},
#                 "S": {"intervalle": [(0.5, 2.0, 2), (2.0, 5.0, 3), (5.0, 10.0, 4), (10.0, None, 5)]},
#                 "B": {"intervalle": [(0.5, 2.0, 2), (2.0, 5.0, 3), (5.0, 10.0, 4), (10.0, None, 5)]},
#             },
#             ("B", "C"): {
#                 "D": {"intervalle": [(0.5, 2.0, 2), (2.0, 5.0, 3), (5.0, 10.0, 4), (10.0, None, 5)]},
#                 "S": {"intervalle": [(0.5, 2.0, 2), (2.0, 5.0, 3), (5.0, 10.0, 4), (10.0, None, 5)]},
#                 "B": {"intervalle": [(0.5, 2.0, 2), (2.0, 5.0, 3), (5.0, 10.0, 4), (10.0, None, 5)]},
#             },
#             ("B", "D"): {
#                 "D": {"intervalle": [(0.5, 2.0, 2), (2.0, 5.0, 3), (5.0, 10.0, 4), (10.0, None, 5)]},
#                 "S": {"intervalle": [(0.5, 2.0, 2), (2.0, 5.0, 3), (5.0, 10.0, 4), (10.0, None, 5)]},
#                 "B": {"intervalle": [(0.5, 2.0, 2), (2.0, 5.0, 3), (5.0, 10.0, 4), (10.0, None, 5)]},
#             },
#             ("B", "E"): {
#                 "D": {"intervalle": [(0.5, 2.0, 2), (2.0, 5.0, 3), (5.0, 10.0, 4), (10.0, None, 5)]},
#                 "S": {"intervalle": [(0.5, 2.0, 2), (2.0, 5.0, 3), (5.0, 10.0, 4), (10.0, None, 5)]},
#                 "B": {"intervalle": [(0.5, 2.0, 2), (2.0, 5.0, 3), (5.0, 10.0, 4), (10.0, None, 5)]},
#             },

#             # Riss pauschal (Ch1 = B, Ch2 = B)
#             ("B", "B"): {"D": {"pauschal": 4}, "S": {"pauschal": 4}, "B": {"pauschal": 4}},

#             # Klaffender Riss (Ch1 = C, Ch2=A–E), pauschal
#             ("C", "A"): {"D": {"pauschal": 5}, "S": {"pauschal": 5}, "B": {"pauschal": 5}},
#             ("C", "B"): {"D": {"pauschal": 5}, "S": {"pauschal": 5}, "B": {"pauschal": 5}},
#             ("C", "C"): {"D": {"pauschal": 5}, "S": {"pauschal": 5}, "B": {"pauschal": 5}},
#             ("C", "D"): {"D": {"pauschal": 5}, "S": {"pauschal": 5}, "B": {"pauschal": 5}},
#             ("C", "E"): {"D": {"pauschal": 5}, "S": {"pauschal": 5}, "B": {"pauschal": 5}},
#         },

#         # BAC – Rohrbruch/Einsturz (Tab. A-3-14)
#         "BAC": {
#             ("A", ""): {  # Bruch
#                 "D": {"pauschal": 5},
#                 "S": {"pauschal": 5},
#                 "B": {"pauschal": 4},
#             },
#             ("B", ""): {  # Fehlen von Teilen
#                 "D": {"pauschal": 5},
#                 "S": {"pauschal": 5},
#                 "B": {"pauschal": 5},
#             },
#             ("C", ""): {  # Einsturz
#                 "D": {"pauschal": 5},
#                 "S": {"pauschal": 5},
#                 "B": {"pauschal": 5},
#             },
#         },

#         # BAD – Defektes Mauerwerk (Tab. A-3-15)
#         "BAD": {
#             ("A", ""): {  # verschoben
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 3},
#                 "B": {"pauschal": 3},
#             },
#             ("B", ""): {  # fehlende Steine
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 4},
#                 "B": {"pauschal": 4},
#             },
#             ("C", ""): {  # Sohle abgesackt
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 5},
#                 "B": {"pauschal": 4},
#             },
#             ("D", ""): {  # Einsturz
#                 "D": {"pauschal": 5},
#                 "S": {"pauschal": 5},
#                 "B": {"pauschal": 5},
#             },
#         },
#         # BAE – Fehlender Mörtel (Tab. A-3-16)
#         "BAE": {
#             # Erste Zeile: x < 100 / x ≥ 100 (nur 2 Klassen)
#             ("", "1"): {  # optionaler künstlicher Ch2 zur Trennung
#                 "D": {
#                     "intervalle": [
#                         (None, 100.0, 1),
#                         (100.0, None, 4),
#                     ]
#                 },
#                 "S": {
#                     "intervalle": [
#                         (None, 100.0, 1),
#                         (100.0, None, 4),
#                     ]
#                 },
#                 "B": {
#                     "intervalle": [
#                         (None, 100.0, 1),
#                         (100.0, None, 4),
#                     ]
#                 },
#             },
#             # Zweite Zeile: x < 20 / 20–<50 / 50–<100 / ≥100
#             ("", ""): {
#                 "D": {
#                     "intervalle": [
#                         (None,  20.0, 1),
#                         (20.0,  50.0, 2),
#                         (50.0, 100.0, 3),
#                         (100.0, None, 4),
#                     ]
#                 },
#                 "S": {
#                     "intervalle": [
#                         (None,  20.0, 1),
#                         (20.0,  50.0, 2),
#                         (50.0, 100.0, 3),
#                         (100.0, None, 4),
#                     ]
#                 },
#                 "B": {
#                     "intervalle": [
#                         (None,  20.0, 1),
#                         (20.0,  50.0, 2),
#                         (50.0, 100.0, 3),
#                         (100.0, None, 4),
#                     ]
#                 },
#             },
#         },

#         # BAF – Oberflächenschaden (Tab. A-3-17)
#         "BAF": {
#             # Alle Zeilen sind pauschal; hier exemplarische Klassenwerte
#             ("A", ""): {"D": {"pauschal": 2}, "S": {"pauschal": 1}, "B": {"pauschal": 2}},
#             ("B", ""): {"D": {"pauschal": 2}, "S": {"pauschal": 1}, "B": {"pauschal": 2}},
#             ("C", ""): {"D": {"pauschal": 2}, "S": {"pauschal": 2}, "B": {"pauschal": 2}},
#             ("D", ""): {"D": {"pauschal": 3}, "S": {"pauschal": 2}, "B": {"pauschal": 3}},
#             ("E", ""): {"D": {"pauschal": 3}, "S": {"pauschal": 2}, "B": {"pauschal": 3}},
#             ("F", ""): {"D": {"pauschal": 3}, "S": {"pauschal": 3}, "B": {"pauschal": 3}},
#             ("G", ""): {"D": {"pauschal": 3}, "S": {"pauschal": 3}, "B": {"pauschal": 3}},
#             ("H", ""): {"D": {"pauschal": 4}, "S": {"pauschal": 3}, "B": {"pauschal": 4}},
#             ("I", ""): {"D": {"pauschal": 4}, "S": {"pauschal": 4}, "B": {"pauschal": 4}},
#             ("J", ""): {"D": {"pauschal": 4}, "S": {"pauschal": 4}, "B": {"pauschal": 4}},
#             ("K", ""): {"D": {"pauschal": 5}, "S": {"pauschal": 4}, "B": {"pauschal": 5}},
#             ("Z", ""): {"D": {"pauschal": 2}, "S": {"pauschal": 2}, "B": {"pauschal": 2}},
#         },

#         # BAG – Einragender Anschluss (Tab. A-3-18)
#         "BAG": {
#             ("", ""): {
#                 "D": {
#                     "intervalle": [
#                         (None,  15.0, 1),
#                         (15.0, 40.0, 2),
#                         (40.0, 60.0, 3),
#                         (60.0, 75.0, 4),
#                         (75.0, None, 5),
#                     ]
#                 },
#                 "S": {
#                     "intervalle": [
#                         (None,  15.0, 1),
#                         (15.0, 40.0, 2),
#                         (40.0, 60.0, 3),
#                         (60.0, 75.0, 4),
#                         (75.0, None, 5),
#                     ]
#                 },
#                 "B": {
#                     "intervalle": [
#                         (None,  15.0, 1),
#                         (15.0, 40.0, 2),
#                         (40.0, 60.0, 3),
#                         (60.0, 75.0, 4),
#                         (75.0, None, 5),
#                     ]
#                 },
#             },
#         },
#         # BAH – Schadhafter Anschluss (Tab. A-3-19)
#         "BAH": {
#             # Ch1 = E: keine Klassifizierung, nur informativ → alle 0
#             ("E", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 0},
#             },
#             # Ch1 = A, Ch2 leer: pauschal
#             ("A", ""): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 2},
#                 "B": {"pauschal": 3},
#             },
#             # Ch1 = B,C,D, Ch2 leer: pauschal
#             ("B", ""): {
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 3},
#                 "B": {"pauschal": 4},
#             },
#             ("C", ""): {
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 3},
#                 "B": {"pauschal": 4},
#             },
#             ("D", ""): {
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 3},
#                 "B": {"pauschal": 4},
#             },
#             # Ch1 = Z: pauschal
#             ("Z", ""): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 2},
#                 "B": {"pauschal": 3},
#             },
#         },

#         # BAI – Einragendes Dichtungsmaterial (Tab. A-3-20)
#         "BAI": {
#             # A/A: pauschal
#             ("A", "A"): {
#                 "D": {"pauschal": 2},
#                 "S": {"pauschal": 1},
#                 "B": {"pauschal": 2},
#             },
#             # A/A (zweite Zeile, identisch in der Norm)
#             ("A", "A2"): {  # optionaler technischer Key, falls du differenzieren willst
#                 "D": {"pauschal": 2},
#                 "S": {"pauschal": 1},
#                 "B": {"pauschal": 2},
#             },
#             # A/B,C,D: pauschal
#             ("A", "B"): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 2},
#                 "B": {"pauschal": 3},
#             },
#             ("A", "C"): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 2},
#                 "B": {"pauschal": 3},
#             },
#             ("A", "D"): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 2},
#                 "B": {"pauschal": 3},
#             },
#             # Z: mit Querschnittsminderung in %
#             ("Z", ""): {
#                 "D": {
#                     "intervalle": [
#                         (None,  5.0, 1),
#                         (5.0,  20.0, 2),
#                         (20.0, 35.0, 3),
#                         (35.0, 50.0, 4),
#                         (50.0, None, 5),
#                     ]
#                 },
#                 "S": {
#                     "intervalle": [
#                         (None,  5.0, 1),
#                         (5.0,  20.0, 2),
#                         (20.0, 35.0, 3),
#                         (35.0, 50.0, 4),
#                         (50.0, None, 5),
#                     ]
#                 },
#                 "B": {
#                     "intervalle": [
#                         (None,  5.0, 1),
#                         (5.0,  20.0, 2),
#                         (20.0, 35.0, 3),
#                         (35.0, 50.0, 4),
#                         (50.0, None, 5),
#                     ]
#                 },
#             },
#         },
#         # BAJ – Verschobene Verbindung (Tab. A-3-21 + deine Vorgaben)
#         "BAJ": {
#             # A_pauschal für DN <= 800 (fachliche Setzung von dir)
#             "A_pauschal": {
#                 ("A", ""): {
#                     "D": {"pauschal": 1},   # Beispiel: alles Klasse 1
#                     "S": {"pauschal": 1},   # S immer 1
#                     "B": {"pauschal": 0},   # B immer 0
#                 },
#             },

#             # DN > 800: axiale Verschiebung A mit Intervallen (Tab. A-3-21)
#             "gross": {    # DN > 800
#                 ("A", ""): {
#                     "D": {"intervalle": [
#                         (None, 20.0, 1),
#                         (20.0, 40.0, 2),
#                         (40.0, 65.0, 3),
#                         (65.0, 90.0, 4),
#                         (90.0, None, 5),
#                     ]},
#                     "S": {"pauschal": 1},   # S immer 1
#                     "B": {"pauschal": 0},   # B immer 0
#                 },
#             },

#             # B: DN-unabhängig (kein Dimensionsbezug)
#             ("B", ""): {
#                 "D": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 15.0, 2),
#                     (15.0, 20.0, 3),
#                     (20.0, 30.0, 4),
#                     (30.0, None, 5),
#                 ]},
#                 "S": {"pauschal": 1},   # S immer 1
#                 "B": {"intervalle": [   # dein Schema für B
#                     (None, 10.0, 1),
#                     (10.0, 15.0, 2),
#                     (15.0, 20.0, 2),
#                     (20.0, 30.0, 2),
#                     (30.0, None, 2),
#                 ]},
#             },
#             ("B", "pauschal"): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 1},
#                 "B": {"pauschal": 3},
#             },

#             # C: DN-abhängig in drei Bereichen nach Tabelle
#             "DN<=200": {
#                 ("C", ""): {
#                     "D": {"intervalle": [
#                         (None, 5.0, 1),
#                         (5.0, 7.0, 2),
#                         (7.0, 9.0, 3),
#                         (9.0, 12.0, 4),
#                         (12.0, None, 5),
#                     ]},
#                     "S": {"pauschal": 1},   # S immer 1
#                     "B": {"pauschal": 0},   # B immer 0
#                 },
#             },
#             "200<DN<=500": {
#                 ("C", ""): {
#                     "D": {"intervalle": [
#                         (None, 2.0, 1),
#                         (2.0, 3.0, 2),
#                         (3.0, 4.0, 3),
#                         (4.0, 6.0, 4),
#                         (6.0, None, 5),
#                     ]},
#                     "S": {"pauschal": 1},
#                     "B": {"pauschal": 0},
#                 },
#             },
#             "DN>500": {
#                 ("C", ""): {
#                     "D": {"intervalle": [
#                         (None, 1.0, 1),
#                         (1.0, 3.0, 2),
#                         (3.0, 4.0, 3),
#                         (4.0, 6.0, 4),
#                         (6.0, None, 5),
#                     ]},
#                     "S": {"pauschal": 1},
#                     "B": {"pauschal": 0},
#                 },
#             },
#         },
#         # BAK – Feststellung der Innenauskleidung (Tab. A-3-22)
#         "BAK": {
#             # A: Querschnittsminderung in % – nur B hat Intervalle, D/S = 0
#             ("A", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 5.0, 1),
#                     (5.0, 20.0, 2),
#                     (20.0, 35.0, 3),
#                     (35.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },

#             # B: alle Schutzziele pauschal (nur „+ pauschal“ in der Tabelle)
#             ("B", ""): {
#                 "D": {"pauschal": 1},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 0},
#             },

#             # C: zweimal „+ pauschal“ für D und B, S ohne + → S = 0
#             ("C", ""): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 3},
#             },

#             # D: Querschnittsminderung in % – Tabelle hat nur „+ pauschal“ für D
#             ("D", "ABCD"): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 2},
#             },
#             # Fall 2: Ch2 = C -> S pauschal 3, D/B = 0
#             ("D", "C"): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 3},
#                 "B": {"pauschal": 0},
#             },

#             # E: Querschnittsminderung in % – erste Zeile pauschal, zweite mit Intervallen für B
#             ("E", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 2},
#                 "B": {"intervalle": [
#                     (None, 5.0, 1),
#                     (5.0, 20.0, 2),
#                     (20.0, 35.0, 3),
#                     (35.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },

#             # F: Tiefe der Beule in mm – „+ mm(2) pauschal“ nur für B
#             ("F", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 2},
#                 "B": {"pauschal": 0},
#             },

#             # G: „+ pauschal“ nur bei B
#             ("G", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 1},
#             },

#             # H: „+ pauschal“ nur bei B
#             ("H", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 1},
#             },

#             # I: Rissbreite in mm – „+ mm(3) pauschal“ nur bei B
#             ("I", ""): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 0},
#             },

#             # J: Länge in mm – „+ mm(4) pauschal“ nur bei B
#             ("J", ""): {
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 0},
#             },

#             # K: „+ pauschal“ nur bei B
#             ("K", ""): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 0},
#             },

#             # L: „+ pauschal“ nur bei B (zweimal in der Tabelle)
#             ("L", ""): {
#                 "D": {"pauschal": 2},
#                 "S": {"pauschal": 2},
#                 "B": {"pauschal": 0},
#             },

#             # M: „+ pauschal“ nur bei B
#             ("M", ""): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 0},
#             },

#             # N: „+ pauschal“ nur bei B
#             ("N", ""): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 0},
#             },

#             # Z: mehrere „+ pauschal“ für B – zusammengefasst
#             ("Z", ""): {
#                 "D": {"pauschal": 2},
#                 "S": {"pauschal": 2},
#                 "B": {"pauschal": 3},
#             },
#         },
#         # BAL – Schadhafte Reparatur (Tab. A-3-23)
#         "BAL": {
#             # CH1 = A: Lochlänge in mm, für CH2=A–D ist D pauschal
#             ("A", "A"): {"D": {"pauschal": 4}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("A", "B"): {"D": {"pauschal": 4}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("A", "C"): {"D": {"pauschal": 4}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("A", "D"): {"D": {"pauschal": 4}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},

#             # CH1 = B: Lochlänge in mm, CH2=A–D D pauschal
#             ("B", "A"): {"D": {"pauschal": 4}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("B", "B"): {"D": {"pauschal": 4}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("B", "C"): {"D": {"pauschal": 4}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("B", "D"): {"D": {"pauschal": 4}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},

#             # CH1 = C: Verringerung Querschnittsfläche in %, CH2=A–D D pauschal
#             ("C", "A"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("C", "B"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("C", "C"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("C", "D"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},

#             # CH1 = D: Lochlänge in mm, CH2=A–D D pauschal
#             ("D", "A"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("D", "B"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("D", "C"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("D", "D"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},

#             # CH1 = E: Verringerung Querschnittsfläche in %, CH2=A–D B mit Intervallen
#             ("E", "A"): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 5.0, 1),
#                     (5.0, 20.0, 2),
#                     (20.0, 35.0, 3),
#                     (35.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#             ("E", "B"): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 5.0, 1),
#                     (5.0, 20.0, 2),
#                     (20.0, 35.0, 3),
#                     (35.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#             ("E", "C"): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 5.0, 1),
#                     (5.0, 20.0, 2),
#                     (20.0, 35.0, 3),
#                     (35.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#             ("E", "D"): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 5.0, 1),
#                     (5.0, 20.0, 2),
#                     (20.0, 35.0, 3),
#                     (35.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },

#             # CH1 = F: Lochlänge mm, CH2=A–D D pauschal
#             ("F", "A"): {"D": {"pauschal": 4}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("F", "B"): {"D": {"pauschal": 4}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("F", "C"): {"D": {"pauschal": 4}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("F", "D"): {"D": {"pauschal": 4}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},

#             # CH1 = G: Riss-/Spaltbreite mm, CH2=A–D D pauschal
#             ("G", "A"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("G", "B"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("G", "C"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},
#             ("G", "D"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 0}},

#             # CH1 = Z: sonstige schadhafte Reparatur, CH2=A–D D pauschal, B zusätzlich pauschal
#             ("Z", "A"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 3}},
#             ("Z", "B"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 3}},
#             ("Z", "C"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 3}},
#             ("Z", "D"): {"D": {"pauschal": 3}, "S": {"pauschal": 0}, "B": {"pauschal": 3}},
#         },
#         # BAM – Schadhafte Schweißnaht (Tab. A-3-24)
#         "BAM": {
#             # A,B,C: „+ pauschal“ – B wirkt, D/S = 0
#             ("A", ""): {"D": {"pauschal": 3}, "S": {"pauschal": 2}, "B": {"pauschal": 0}},
#             ("B", ""): {"D": {"pauschal": 3}, "S": {"pauschal": 1}, "B": {"pauschal": 0}},
#             ("C", ""): {"D": {"pauschal": 3}, "S": {"pauschal": 2}, "B": {"pauschal": 3}},
#         },

#         # BAN – Poröses Rohr (Tab. A-3-25)
#         "BAN": {
#             # beide Zeilen „+ pauschal“ – typischerweise D und S relevant, B optional
#             ("", ""): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 3},
#                 "B": {"pauschal": 0},
#             },
#         },

#         # BAO – Boden sichtbar (Tab. A-3-26)
#         "BAO": {
#             # beide Zeilen „+ pauschal“ – primär B betroffen (Betriebssicherheit)
#             ("", ""): {
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 4},
#                 "B": {"pauschal": 30},
#             },
#         },

#         # BAP – Hohlraum sichtbar (Tab. A-3-27)
#         "BAP": {
#             # beide Zeilen „+ pauschal“ – D und S kritisch, B sekundär
#             ("", ""): {
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 5},
#                 "B": {"pauschal": 0},
#             },
#         },
#         # BBA – Wurzeln (Tab. A-3-28)
#         "BBA": {
#             # CH1 = A,B,C: D immer 3, S immer 0, B nach Intervall
#             ("A", ""): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 20.0, 2),
#                     (20.0, 30.0, 3),
#                     (30.0, None, 4),
#                 ]},
#             },
#             ("B", ""): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 20.0, 2),
#                     (20.0, 30.0, 3),
#                     (30.0, None, 4),
#                 ]},
#             },
#             ("C", ""): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 20.0, 2),
#                     (20.0, 30.0, 3),
#                     (30.0, None, 4),
#                 ]},
#             },
#         },
#         "BBB": {
#             ("A", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 20.0, 2),
#                     (20.0, 30.0, 3),
#                     (30.0, None, 4),
#                 ]},
#             },
#             ("B", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 20.0, 2),
#                     (20.0, 30.0, 3),
#                     (30.0, None, 4),
#                 ]},
#             },
#             ("C", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 20.0, 2),
#                     (20.0, 30.0, 3),
#                     (30.0, None, 4),
#                 ]},
#             },
#             ("Z", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 20.0, 2),
#                     (20.0, 30.0, 3),
#                     (30.0, None, 4),
#                 ]},
#             },
#         },
#         "BBC": {
#             ("A", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 25.0, 2),
#                     (25.0, 40.0, 3),
#                     (40.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#             ("B", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 25.0, 2),
#                     (25.0, 40.0, 3),
#                     (40.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#             ("C", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 25.0, 2),
#                     (25.0, 40.0, 3),
#                     (40.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#             ("Z", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 25.0, 2),
#                     (25.0, 40.0, 3),
#                     (40.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#         },
#         "BBD": {
#             ("A", ""): {
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 5},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 20.0, 2),
#                     (20.0, 30.0, 3),
#                     (30.0, None, 4),
#                 ]},
#             },
#             ("B", ""): {
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 5},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 20.0, 2),
#                     (20.0, 30.0, 3),
#                     (30.0, None, 4),
#                 ]},
#             },
#             ("C", ""): {
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 5},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 20.0, 2),
#                     (20.0, 30.0, 3),
#                     (30.0, None, 4),
#                 ]},
#             },
#             ("D", ""): {
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 5},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 20.0, 2),
#                     (20.0, 30.0, 3),
#                     (30.0, None, 4),
#                 ]},
#             },
#             ("Z", ""): {
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 5},
#                 "B": {"intervalle": [
#                     (None, 10.0, 1),
#                     (10.0, 20.0, 2),
#                     (20.0, 30.0, 3),
#                     (30.0, None, 4),
#                 ]},
#             },
#         },
#         "BBE": {
#             # Intervallfall für A,B,C,D,E,F,G,H,Z
#             ("A", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 5.0, 1),
#                     (5.0, 20.0, 2),
#                     (20.0, 35.0, 3),
#                     (35.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#             ("B", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 5.0, 1),
#                     (5.0, 20.0, 2),
#                     (20.0, 35.0, 3),
#                     (35.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#             ("C", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 5.0, 1),
#                     (5.0, 20.0, 2),
#                     (20.0, 35.0, 3),
#                     (35.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#             ("D", ""): {  # Intervall-Variante von D
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 5.0, 1),
#                     (5.0, 20.0, 2),
#                     (20.0, 35.0, 3),
#                     (35.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#             ("E", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 5.0, 1),
#                     (5.0, 20.0, 2),
#                     (20.0, 35.0, 3),
#                     (35.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#             ("F", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 5.0, 1),
#                     (5.0, 20.0, 2),
#                     (20.0, 35.0, 3),
#                     (35.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#             ("G", ""): {  # Intervall-Variante von G
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 5.0, 1),
#                     (5.0, 20.0, 2),
#                     (20.0, 35.0, 3),
#                     (35.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#             ("H", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 5.0, 1),
#                     (5.0, 20.0, 2),
#                     (20.0, 35.0, 3),
#                     (35.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#             ("Z", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"intervalle": [
#                     (None, 5.0, 1),
#                     (5.0, 20.0, 2),
#                     (20.0, 35.0, 3),
#                     (35.0, 50.0, 4),
#                     (50.0, None, 5),
#                 ]},
#             },
#         },
#         # BBF – Infiltration (Tab. A-3 - 33)
#         "BBF": {
#             # CH1 = A,B: pauschale D-Klasse
#             ("A", ""): {
#                 "D": {"pauschal": 3},  # Klasse aus der „pauschal“-Spalte
#                 "S": {"pauschal": 2},
#                 "B": {"pauschal": 1},
#             },
#             ("B", ""): {
#                 "D": {"pauschal": 3},
#                 "S": {"pauschal": 2},
#                 "B": {"pauschal": 1},
#             },

#             # CH1 = C: pauschale D-Klasse
#             ("C", ""): {
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 3},
#                 "B": {"pauschal": 2},
#             },

#             # CH1 = D: pauschale D-Klasse
#             ("D", ""): {
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 4},
#                 "B": {"pauschal": 2},
#             },
#         },
#         "BBG": {
#             ("", ""): {
#                 "D": {"pauschal": 4},
#                 "S": {"pauschal": 2},
#                 "B": {"pauschal": 0},  # Klasse entsprechend der „pauschal“-Spalte
#             },
#         },
#         "BDB": {
#             # AA–AE: D und S pauschal, B = 0
#             ("AA", ""): {
#                 "D": {"pauschal": 2},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 2},
#             },
#             ("AB", ""): {
#                 "D": {"pauschal": 2},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 2},
#             },
#             ("AC", ""): {
#                 "D": {"pauschal": 2},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 2},
#             },
#             ("AD", ""): {
#                 "D": {"pauschal": 2},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 2},
#             },
#             ("AE", ""): {
#                 "D": {"pauschal": 2},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 2},
#             },

#             # BA–BC: nur B pauschal
#             ("BA", ""): {
#                 "D": {"pauschal": 2},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 0},
#             },
#             ("BB", ""): {
#                 "D": {"pauschal": 2},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 0},
#             },
#             ("BC", ""): {
#                 "D": {"pauschal": 2},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 0},
#             },
#         },
#         "BDD": {
#             ("A", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 2},  # Klasse aus der „pauschal“-Spalte
#             },
#             ("B", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 2}, 
#             },
#             ("C", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 2}, 
#             },
#             ("D", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 2}, 
#             },
#             ("E", ""): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 2}, 
#             },
#         },
#         "BDE": {
#             # CH2 = A
#             ("A", "A"): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 4},
#             },
#             ("C", "A"): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 4},
#             },
#             ("D", "A"): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 4},
#             },
#             ("E", "A"): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 4},
#             },

#             # CH2 = B
#             ("A", "B"): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 3},
#             },
#             ("C", "B"): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 3},
#             },
#             ("D", "B"): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 3},
#             },
#             ("E", "B"): {
#                 "D": {"pauschal": 0},
#                 "S": {"pauschal": 0},
#                 "B": {"pauschal": 3},
#             },
#         },
#     },
#     "Schächte": _schacht_mapping,
# }

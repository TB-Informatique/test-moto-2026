#!/usr/bin/env python3
"""Télécharge des photos de situations routières (Wikimedia Commons, licences libres)."""

from __future__ import annotations

import io
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "assets/img/situations"
META = DEST / "credits.json"
UA = "CodeMoto2026/1.0 (pedagogical ETM trainer; github.com/TB-Informatique/test-moto-2026)"
API = "https://commons.wikimedia.org/w/api.php"

# id, recherches Commons (la première qui donne une photo libre convient)
TOPICS = [
    ("rondpoint", ["roundabout France", "rond-point France voiture"]),
    ("carrefour", ["intersection France cars", "carrefour France"]),
    ("feux", ["traffic lights France street", "feux tricolores France"]),
    ("stop", ["AB4 stop France", "panneau stop intersection France"]),
    ("cedez", ["AB3a France", "cédez le passage France"]),
    ("cedez-inverse", ["B15 France", "cédez circulation sens inverse France"]),
    ("pieton", ["passage piéton France", "zebra crossing France"]),
    ("ecole", ["A13a école France", "school crossing France"]),
    ("velo", ["piste cyclable France", "cycle lane France"]),
    ("tram", ["tramway rails Lyon", "tram tracks France street"]),
    ("bus", ["voie de bus France", "bus lane Paris"]),
    ("pl", ["poids lourd France autoroute", "truck France highway"]),
    ("moto-ville", ["motorcycle Paris street", "moto circulation France"]),
    ("moto-route", ["motorcycle France road", "moto départementale France"]),
    ("autoroute", ["autoroute France", "A7 autoroute"]),
    ("insertion", ["bretelle autoroute France", "motorway on-ramp France"]),
    ("bau", ["bande d'arrêt d'urgence France", "emergency lane France"]),
    ("peage", ["péage autoroute France", "toll booth France"]),
    ("tunnel", ["tunnel autoroute France", "road tunnel France"]),
    ("sortie", ["sortie autoroute France", "motorway exit France"]),
    ("chantier", ["chantier routier France", "road works France"]),
    ("pluie", ["pluie autoroute France", "wet highway France rain"]),
    ("nuit", ["rue de nuit France", "night road France city"]),
    ("brouillard", ["brouillard autoroute France", "fog highway France"]),
    ("neige", ["neige route France", "snow road France"]),
    ("virage", ["virage montagne France", "winding road France Alps"]),
    ("dosane", ["dos d'âne France", "speed bump France"]),
    ("ligne-continue", ["ligne continue France chaussée", "solid line road France"]),
    ("ligne-discontinue", ["ligne discontinue France", "dashed road marking France"]),
    ("sens-interdit", ["sens interdit France rue", "B1 France street"]),
    ("zone30", ["zone 30 France", "B30 France street"]),
    ("agglomeration", ["panneau entrée agglomération France", "EB10 France"]),
    ("fin-agglo", ["sortie agglomération France", "EB20 France"]),
    ("travaux-panneau", ["AK14 France", "panneau travaux France"]),
    ("radar", ["radar automatique France", "speed camera France road"]),
    ("priorite-droite", ["AB1 France", "priorité à droite France"]),
    ("double-sens", ["B15 étroit France", "narrow street two way France"]),
    ("chaussee-etroite", ["chaussée étroite village France", "narrow road France village"]),
    ("tourne-gauche", ["tourne à gauche carrefour France", "left turn intersection France"]),
    ("file-autoroute", ["trafic autoroute France", "dense traffic France motorway"]),
    ("circulation-dense", ["bouchon France", "traffic jam France"]),
    ("pont", ["pont routier France", "road bridge France"]),
    ("passage-pn", ["passage à niveau France", "level crossing France"]),
    ("rails", ["rails tramway chaussée France", "tram rails wet France"]),
    ("gravillons", ["gravillons route France", "loose gravel road France"]),
    ("degrade", ["chaussée dégradée France", "damaged road France"]),
    ("marquage", ["marquage au sol France", "road marking France"]),
    ("soleil", ["contre-jour route France", "sun glare road France"]),
    ("groupe-moto", ["groupe motards France", "motorcycle group France"]),
    ("casque", ["motard casque France", "motorcycle helmet France rider"]),
    ("gilet", ["gilet jaune motard", "high visibility vest motorcycle"]),
    ("equip-pluie", ["moto pluie France", "motorcycle rain gear"]),
    ("pneu", ["pneu moto usé", "motorcycle tire"]),
    ("chaine", ["chaîne moto", "motorcycle chain"]),
    ("phare", ["phare moto allumé", "motorcycle headlight"]),
    ("moto-garee", ["moto stationnée France", "parked motorcycle France"]),
    ("controle", ["contrôle police route France", "police checkpoint France"]),
    ("accident", ["accident route France", "car crash France road"]),
    ("triangle", ["triangle présignalisation France", "warning triangle road"]),
    ("panne", ["panne bande arrêt urgence", "broken car emergency lane"]),
    ("essence", ["station-service France", "petrol station France"]),
    ("parking", ["parking moto France", "motorcycle parking France"]),
    ("pieton-ville", ["piétons rue France", "pedestrians street France"]),
    ("enfant", ["enfants école rue France", "children school street"]),
    ("bus-arret", ["arrêt de bus France", "bus stop France"]),
    ("trottinette", ["trottinette piste cyclable France", "scooter cycle lane"]),
    ("animal", ["gibier route France", "wild boar road France"]),
    ("cavalier", ["cavalier route France", "horse rider road France"]),
    ("prioritaire", ["véhicule prioritaire France", "ambulance France street"]),
    ("taxi", ["taxi Paris rue", "taxi France street"]),
    ("porte-ouverte", ["portière voiture", "car door open street"]),
    ("angle-mort-photo", ["camion angle mort France", "truck blind spot France"]),
    ("deux-roues-feu", ["motos feu rouge Paris", "motorcycles traffic light France"]),
    ("interfiles", ["interfile moto France", "lane splitting motorcycle"]),
    ("voie-verte", ["voie verte France", "greenway France"]),
    ("aire-pietonne", ["aire piétonne France", "pedestrian zone France"]),
    ("peage-moto", ["moto péage France", "motorcycle toll France"]),
    ("aire-service", ["aire d'autoroute France", "motorway service area France"]),
    ("eclairage-defaut", ["rue mal éclairée France", "dark street France night"]),
    ("flaque", ["flaque route France", "puddle road France"]),
    ("feuilles", ["feuilles mortes chaussée France", "wet leaves road"]),
    ("verglas", ["verglas route France", "ice road France"]),
    ("orriere", ["orage autoroute France", "storm highway France"]),
    ("vent", ["vent fort route France", "strong wind road"]),
    ("camion-depassement", ["dépassement camion France", "overtaking truck France"]),
    ("velo-ville", ["cycliste ville France", "cyclist Paris street"]),
    ("trottoir", ["trottoir piétons France", "sidewalk France"]),
    ("passage-souterrain", ["passage souterrain piétons France", "underpass France"]),
    ("rondpoint-feux", ["rond-point feux France", "roundabout traffic lights France"]),
    ("carrefour-giratoire", ["giratoire France", "circulatory system France"]),
    ("sens-unique", ["sens unique France", "one way street France"]),
    ("stationnement-genant", ["voiture mal stationnée France", "illegal parking France"]),
    ("double-file", ["double file Paris", "double parking France"]),
    ("travaux-pieton", ["travaux piétons France", "pedestrian diversion France"]),
    ("corridor", ["corridor de sécurité France", "safety corridor road works France"]),
    ("radar-panneau", ["SR3a France", "panneau radar France"]),
    ("fin-autoroute", ["fin d'autoroute France", "end of motorway France"]),
    ("bretelle-sortie", ["bretelle sortie France", "off-ramp France"]),
    ("peage-barriere", ["barrière péage France", "toll barrier France"]),
    ("moto-equipement", ["équipement motard intégral", "full motorcycle gear"]),
    ("gants-moto", ["gants moto", "motorcycle gloves"]),
    ("bottes-moto", ["bottes moto", "motorcycle boots"]),
    ("airbag-moto", ["gilet airbag moto", "motorcycle airbag vest"]),
    ("casque-ouvert", ["casque jet moto", "open face helmet"]),
    ("pneu-crevaison", ["crevaison moto", "motorcycle puncture"]),
    ("frein-disque", ["disque de frein moto", "motorcycle brake disc"]),
    ("retro-moto", ["rétroviseur moto", "motorcycle mirror"]),
    ("huile-moteur", ["vidange moto", "motorcycle oil"]),
    ("batterie-moto", ["batterie moto", "motorcycle battery"]),
    ("controle-technique", ["contrôle technique véhicule France", "vehicle inspection France"]),
    ("carte-grise", ["carte grise France", "registration document France"]),
    ("assurance", ["constat amiable France", "insurance form France"]),
    ("alcool-controle", ["contrôle alcoolémie France", "breathalyzer police France"]),
    ("telephone-volant", ["téléphone au volant France", "phone driving France"]),
    ("fatigue-autoroute", ["aire repos autoroute France", "rest area France"]),
    ("bouchon-ville", ["embouteillage ville France", "city traffic jam France"]),
    ("pollution", ["pollution air ville France", "air pollution city France"]),
    ("faune", ["panneau animaux route France", "A15a France road"]),
    ("zone-nature", ["route parc naturel France", "national park road France"]),
    ("secours-accident", ["pompiers accident France", "firefighters crash France"]),
    ("samu", ["SAMU ambulance France", "SAMU France"]),
    ("gilet-secours", ["gilet de haute visibilité France", "hi-vis vest France"]),
]


def api(params: dict) -> dict:
    qs = urllib.parse.urlencode({**params, "format": "json"})
    req = urllib.request.Request(f"{API}?{qs}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as resp:
        return json.loads(resp.read().decode())


def search_files(query: str, limit: int = 8) -> list[str]:
    data = api({
        "action": "query",
        "list": "search",
        "srsearch": f"filetype:bitmap {query}",
        "srnamespace": 6,
        "srlimit": limit,
    })
    return [hit["title"] for hit in data.get("query", {}).get("search", [])]


def file_info(title: str) -> dict | None:
    data = api({
        "action": "query",
        "titles": title,
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": 1600,
    })
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        if page.get("missing") is not None:
            return None
        infos = page.get("imageinfo") or []
        if infos:
            return infos[0]
    return None


def license_ok(info: dict) -> bool:
    meta = info.get("extmetadata") or {}
    lic = (meta.get("LicenseShortName", {}).get("value") or "").lower()
    allow = ("public domain", "pd", "cc0", "cc by", "cc-by", "cc by-sa", "cc-by-sa")
    return any(a in lic for a in allow)


def credit(info: dict, title: str) -> str:
    meta = info.get("extmetadata") or {}
    artist = meta.get("Artist", {}).get("value") or "Wikimedia Commons"
    artist = artist.replace("<", " ").replace(">", " ")
    for tag in ("p", "a", "span", "b", "i"):
        artist = artist.replace(f"/{tag}", "").replace(tag, "")
    artist = " ".join(artist.split())[:80]
    lic = meta.get("LicenseShortName", {}).get("value") or "licence libre"
    name = title.replace("File:", "")
    return f"{artist} — Wikimedia Commons ({lic}) — {name}"


def save_jpeg(raw: bytes, dest: Path) -> bool:
    try:
        im = Image.open(io.BytesIO(raw))
        im = im.convert("RGB")
        w, h = im.size
        if w < 500 or h < 350:
            return False
        if w > 1400:
            im = im.resize((1400, int(h * 1400 / w)), Image.Resampling.LANCZOS)
        dest.parent.mkdir(parents=True, exist_ok=True)
        im.save(dest, "JPEG", quality=80, optimize=True)
        return dest.stat().st_size > 8000
    except Exception:
        return False


def download(url: str) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def pick_for_topic(queries: list[str], used: set[str]) -> dict | None:
    for q in queries:
        try:
            titles = search_files(q, 10)
        except Exception as exc:
            print("  search fail", q, exc)
            time.sleep(2)
            continue
        for title in titles:
            if title in used:
                continue
            try:
                info = file_info(title)
            except Exception:
                continue
            if not info or not license_ok(info):
                continue
            mime = (info.get("mime") or "")
            if not mime.startswith("image/"):
                continue
            if "svg" in mime or "gif" in mime:
                continue
            url = info.get("thumburl") or info.get("url")
            if not url:
                continue
            try:
                raw = download(url)
            except Exception as exc:
                print("  dl fail", title, exc)
                continue
            if not raw:
                continue
            used.add(title)
            return {"title": title, "info": info, "raw": raw, "url": url}
        time.sleep(0.4)
    return None


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    credits = json.loads(META.read_text()) if META.exists() else {}
    used = set(c.get("title") for c in credits.values())
    ok = 0
    for i, (slug, queries) in enumerate(TOPICS, 1):
        dest = DEST / f"{slug}.jpg"
        if dest.exists() and dest.stat().st_size > 8000 and slug in credits:
            print(f"[{i}/{len(TOPICS)}] skip {slug}")
            ok += 1
            continue
        print(f"[{i}/{len(TOPICS)}] {slug} …")
        picked = pick_for_topic(queries, used)
        if not picked:
            print("  NONE")
            time.sleep(1)
            continue
        if save_jpeg(picked["raw"], dest):
            credits[slug] = {
                "title": picked["title"],
                "credit": credit(picked["info"], picked["title"]),
                "file": f"assets/img/situations/{slug}.jpg",
            }
            META.write_text(json.dumps(credits, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            ok += 1
            print("  OK", dest.stat().st_size, picked["title"][:70])
        else:
            print("  bad image")
        time.sleep(0.8)
    print("done", ok, "/", len(TOPICS))


if __name__ == "__main__":
    main()

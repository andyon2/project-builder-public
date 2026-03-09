# Content Humanization: Anti-GPTism & Anti-AI-Slop Regeln

Kuratiertes Wissen aus drei Recherchen (Maerz 2026).

## Kernprinzip

KI-Detektoren messen **Perplexity** (Vorhersagbarkeit der Wortwahl) und **Burstiness** (Variation der Satzlaenge). KI-Text hat niedrige Werte bei beiden -- gleichfoermig, vorhersagbar. Menschlicher Text hat hohe Werte -- ueberraschend, variabel.

**Ziel:** Hohe Perplexity (unerwartete Wortwahl) + hohe Burstiness (wilde Satzlaengen-Variation).

---

## 1. Wort-Blacklists

### Englisch -- Tier 1 (Sofort-Alarm, NIE verwenden)

delve, tapestry, landscape (als Metapher), multifaceted, intricate, pivotal, crucial, nuanced, testament, embark, myriad, plethora

### Englisch -- Tier 2 (Starke Indikatoren, vermeiden)

leverage, optimize, facilitate, utilize, endeavor, methodology, comprehensive, robust, seamless, transformative, enhance, foster, elevate, meticulous, bolster, garner, vibrant, underscore

### Englisch -- Uebergangsfluche (3-5x haeufiger als bei Menschen)

Furthermore, Moreover, Additionally, Indeed, Notably, Consequently, Subsequently, Accordingly, Thus, Significantly, In conclusion

### Deutsch -- Verbotene Floskeln

**Eroeffnungen:** "In der heutigen Zeit", "In einer Welt, in der", "Immer mehr Menschen fragen sich"
**Phrasen:** "revolutionieren", "optimieren", "aufs naechste Level", "umfassend", "ganzheitlich", "praezise", "spannende Einblicke", "nicht nur... sondern auch", "es ist entscheidend", "eine Rolle spielen"
**Aufforderungen:** "Tauche ein", "Entfessle die Kraft", "Maximiere dein Potenzial", "Bereit, mehr zu erfahren?", "Lass uns / Tauchen wir ein"
**Schluss:** "Abschliessend laesst sich sagen", "Insgesamt", "Zusammenfassend ist festzuhalten"

---

## 2. Strukturelle Regeln fuer Text-Content

### Was KI-Text verrät

- **Gleichfoermige Satzlaenge** (15-20 Woerter, schmales Band)
- **Gleichfoermige Absatzlaenge** (jeder Absatz ~3-5 Saetze)
- **Intro-Liste-Fazit-Schema** bei jedem Abschnitt
- **Dreierstruktur** (drei Tipps, drei Argumente, drei Schritte)
- **Fazit fasst alles nochmal zusammen** statt neuen Gedanken zu bringen
- **Exzessive Gedankenstriche** (em-dashes) als Stilmittel
- **Perfekte Grammatik** ohne Fragmente, ohne Satzanfaenge mit "Aber"/"Und"
- **Synonym-Ketten** statt natuerlicher Wortwiederholung
- **Emotionale Flachheit** -- durchgehend neutral-positiv, kein Humor, keine Frustration
- **"Beide Seiten"-Modus** -- jede Position wird relativiert statt Stellung zu beziehen

### Was menschlichen Text auszeichnet

- **Satzlaenge variiert wild** (3 Woerter bis 35+)
- **Absaetze variieren** (Ein-Satz-Absaetze neben 6-Satz-Absaetzen)
- **Kontraktionen** ("it's" statt "it is", "don't" statt "do not")
- **Saetze beginnen mit Konjunktionen** ("Aber", "Und", "Also" -- 10-15% der Saetze)
- **Satzfragmente** fuer Betonung
- **Konkrete Beispiele** mit echten Namen, Zahlen, Orten, Daten
- **Einschübe und Nebenbemerkungen** ("-- was ehrlich gesagt niemand tut --")
- **Natuerliche Wiederholung** von Schlüsselbegriffen statt Synonym-Ketten
- **Eigene Meinung** statt neutraler Beide-Seiten-Darstellung
- **Registerwechsel** -- mal formell, mal locker im selben Text

---

## 3. Deutsche Spezialregeln

### Modalpartikeln -- DER Schluessel fuer natuerliches Deutsch

KI nutzt fast nie Modalpartikeln. Ihr Fehlen ist der staerkste einzelne Indikator fuer KI-generierten deutschen Text.

- **doch** = Betonung/Widerspruch ("Das ist doch klar")
- **halt** / **eben** = Resignation/Akzeptanz ("Ist halt so")
- **ja** = geteiltes Wissen ("Du weisst ja, wie das ist")
- **mal** = Abschwächung ("Schau mal")
- **eigentlich** = Einschraenkung ("Eigentlich wollte ich...")
- **schon** = Zugestaendnis ("Das stimmt schon, aber...")

**Regel:** In allem unter akademischem Register muessen Modalpartikeln vorkommen.

### Weitere deutsche Tells

- **Fehlende Komposita:** KI zerlegt Zusammensetzungen, die ein Muttersprachler als ein Wort schreiben wuerde
- **Vereinfachte Nebensaetze:** Deutsche Schachtelsaetze mit Verb am Ende werden von KI zu flachen englischen Strukturen
- **Uebermaessig formelles Register:** Alltagssprache vermieden, selbst wenn der Kontext es verlangt
- **Satzanfaenge mit "Dieser/Diese/Dieses":** Typischer ChatGPT-Tick auf Deutsch
- **Nur obere Anfuehrungszeichen:** Deutsch nutzt unten-oben ("..."), nicht "..."
- **Ueberkorrektur von Lehnwoertern:** "Konversion" statt "Conversion" -- Formen die niemand benutzt

---

## 4. Design Anti-Patterns ("Claude Gradients" / AI Slop)

### Sofort-Alarme im Webdesign

| Pattern | Problem | Alternative |
|---------|---------|-------------|
| Purple-to-Blue Gradient | Tailwind `bg-indigo-500` Feedback-Loop | Eigene Brand-Farben, kein Indigo/Violet |
| Inter / Roboto / Poppins | Die "KI-Fonts" | JetBrains Mono, Playfair Display, Bricolage Grotesque, Satoshi |
| 3-Spalten-Icon-Grid | Erkennbarster KI-Layout-Tell | Asymmetrische Layouts, variable Spalten |
| Zentrierter Hero + Gradient + 2 Buttons | Universal-KI-Hero | Off-center, Bild-dominant, typografisch |
| Gradient-Text auf dunklem Hintergrund | `bg-clip-text text-transparent` | Feste Textfarben, Akzente anders setzen |
| `shadow-lg` + `rounded-xl` ueberall | Tailwind-Defaults | Mehrschichtige, farbige Schatten; variable Radien |
| Gleichfoermiges Section-Padding | `py-16`/`py-20` auf jedem Abschnitt | Rhythmus variieren, Full-Bleed-Sektionen |

### Spezifische Hex-Werte die "KI" signalisieren

```
#6366F1 (indigo-500), #4F46E5 (indigo-600), #8B5CF6 (violet-500)
#7C3AED (violet-600), #A855F7 (purple-500)
```

### Was menschliches Design auszeichnet

- Asymmetrie und Spannung statt perfekter Zentrierung
- Grid-brechende Momente (Elemente die ueberlappen oder ueberfliessen)
- Font-Pairing (zwei kontrastierende Schriftfamilien)
- Textur und Tiefe (Noise, Grain, geschichtete Gradienten)
- Bewegung mit Absicht (gestaffelte Animationen, benutzerdefinierte Bezier-Kurven)
- CSS Custom Properties statt Inline-Hex-Werte

---

## 5. Prompt-Regeln fuer Content-generierende Agents

Jeder Agent oder Skill, der Texte fuer den Endnutzer generiert (Webseiten-Content, Blog, Marketing, Social Media), MUSS diese Regeln im Prompt enthalten:

### Pflicht-Block (zum Einbau in Content-Agent-Prompts)

```
## Content-Qualitaet: Menschlich schreiben

Dein Output darf NICHT wie KI klingen. Befolge diese Regeln:

SATZEBENE:
- Variiere Satzlaenge radikal: 3-Wort-Fragmente bis 30+-Wort-Saetze durchmischt
- Beginne 10-15% der Saetze mit "Aber", "Und", "Also"
- Nutze Kontraktionen (it's, don't / bzw. natuerliche Umgangssprache auf Deutsch)
- Wiederhole Schluesselbegriffe natuerlich statt Synonym-Ketten zu bilden

STRUKTUR:
- KEIN Intro-Liste-Fazit-Schema
- KEIN Fazit das alles wiederholt -- ende mit einem neuen Gedanken
- Absatzlaengen variieren: 1-Satz-Absaetze neben 5-Satz-Absaetzen
- Nie alles in Dreiergruppen (3 Tipps, 3 Punkte, 3 Schritte)

STIMME:
- Beziehe Position statt neutral zu bleiben
- Zeige echte Reaktionen: Begeisterung, Skepsis, Frustration wo angebracht
- Baue mindestens ein konkretes Beispiel mit echtem Namen/Ort/Zahl ein
- Einschuebe und Nebenbemerkungen sind erlaubt und ermuetigt

VERBOTEN (nie verwenden):
[Hier Blacklist aus Abschnitt 1 einfuegen, angepasst an EN oder DE]
```

### Deutsch-Zusatz (bei deutschem Content zusaetzlich einbauen)

```
DEUTSCH-SPEZIFISCH:
- Modalpartikeln natuerlich einsetzen: "doch", "halt", "eben", "mal", "eigentlich", "ja"
- Echte Komposita bilden (Zusammensetzungen nicht kuenstlich auftrennen)
- Nebensaetze mit Verb am Ende wo natuerlich
- Deutsche Anfuehrungszeichen (unten-oben)
- Alltagssprache erlaubt und erwuenscht (kein gestelztes Hochdeutsch)
- Satzanfaenge variieren (nicht "Dieser/Diese/Dieses" als Default)
```

### Design-Zusatz (bei Web/UI-generierenden Agents zusaetzlich einbauen)

```
DESIGN-REGELN:
- KEIN Indigo/Violet/Purple als Primaerfarbe
- KEIN Inter, Roboto, Poppins als einzige Schrift
- KEIN 3-Spalten-Icon-Grid als Feature-Sektion
- KEIN zentrierter Hero mit Gradient-Hintergrund und zwei Buttons
- KEIN `bg-clip-text text-transparent` Gradient-Text
- CSS Custom Properties fuer Farben (kein Inline-Hex)
- Font-Pairing: mindestens zwei kontrastierende Schriftfamilien
- Asymmetrie einbauen: mindestens ein Grid-brechendes Element
- Spacing-Rhythmus variieren (nicht ueberall gleiche Paddings)
```

---

## 6. Voice Cloning (fuer markenspezifischen Content)

Die effektivste Technik gegen KI-Erkennung: 3-10 Textproben (300+ Woerter) des echten Autors bereitstellen.

**Drei-Schichten-Analyse:**
1. **Strukturelle DNA:** Satzlaenge, Absatzlaenge, Listen vs. Prosa, Ueberschriften-Stil
2. **Emotionale DNA:** Tonalitaet (formell-locker, ernst-spielerisch), emotionale Bandbreite, persoenliche Offenheit
3. **Semantische DNA:** Wortschatz-Tier, verbotene Woerter, bevorzugte Alternativen, Fach-Jargon

**Prozess:** Textproben analysieren -> Voice-Profil erstellen -> Wiederverwendbaren System-Prompt mit messbaren Regeln formulieren -> Positiv- UND Negativ-Beispiele mitliefern

---

## Quellen
- GPTisms-and-AI-Detectable-Patterns.md (2026-03-06) -- Wort-Blacklists EN/DE, Tier-System, Uebergangsfluche
- research-humanizing-ai-text.md (2026-03-06) -- Perplexity/Burstiness-Metriken, Strukturregeln, Voice Cloning, Modalpartikeln
- AI_DESIGN_PATTERNS_REPORT.md (2026-03-06) -- Design Anti-Patterns, Claude Gradients, Hex-Werte, Font-Analyse

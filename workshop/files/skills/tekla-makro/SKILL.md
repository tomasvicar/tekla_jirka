---
name: tekla-makro
description: Napíše, nasadí a odladí C# makro pro Tekla Structures (Open API, modelovací makro .cs). Použij, když uživatel chce v Tekle něco vypsat, zkontrolovat nebo hromadně změnit makrem, nebo když vloží chybu z makra.
---

# Makro pro Teklu: napsat → nasadit → spustit → opravit

Uživatel **neprogramuje**. Mluv česky a jednoduše. Pravidla a cesty jsou v `CLAUDE.md`.

## 1. Zadání

- Na **vybraných** dílech, nebo na celém modelu? Kam výstup (CSV do `<model>\vystupy\`, okno)?
- **Jen čte**, nebo **mění model**? Když mění, nejdřív verze, která jen vypíše, co by změnila.

## 2. Napiš

- Začni od nejbližšího makra v `knihovna/` nebo `makra/`.
- Kostra: `namespace Tekla.Technology.Akit.UserScript`, třída `Script`,
  `public static void Run(Tekla.Technology.Akit.IScript akit)`.
- `GetConnectionStatus()`, nastavení jako konstanty nahoře.
- `try/catch`: chybu zapiš do `<model>\vystupy\makro_chyby.txt` (pomocná metoda `ZapisChybu`
  jako v `makra/01_*.cs`) a ukaž ji i v `MessageBox`.
- **Každý člen API ověř** v `reference/*.xml` (když chybí, na developer.tekla.com pro verzi
  z `CLAUDE.md`), neověřené označ `// NEOVĚŘENO:`.
- Změny modelu: kontrola, že název složky modelu obsahuje „KOPIE“, potvrzovací dialog s počtem dílů, při chybě u části dílů
  seznam a dotaz před `CommitChanges`, jedno `CommitChanges`.
- **Vždy přelož před nasazením** proti DLL z instalace Tekly (`...\<verze>\bin\`), nebo
  proti NuGet balíčku stejné verze. Nepřeložené makro nenasazuj.

## 3. Nasaď

- Ulož do `makra/<NN_Nazev>.cs` a zkopíruj do `<model>\macros\modeling\` (cesta v `CLAUDE.md`;
  když složka chybí, zeptej se a založ ji).
- **Upravené makro nasaď pod novým názvem** (`05_Export_PDF_v2.cs`, `_v3` …). Tekla si
  zkompilované makro pamatuje a po změně souboru by spustila starou verzi (ověřeno 30. 10. 2026).
  Starou verzi ze složky maker smaž až po souhlasu.
- Řekni uživateli: otevřít **kopii**, vybrat díly, **Applications & components** (panel vpravo)
  → **≡** → **Catalog management** → **Reload catalog**, vyhledat název makra, **dvojklik**.
  A co má vidět, když je vše v pořádku.
- Když makro mění model: připomeň, že se model **sám neuloží** – zkontrolovat, pak **Ctrl+S**,
  nebo **Ctrl+Z** (jedno Ctrl+Z vrátí celou změnu).

## 4. Když to nefunguje

- Nejdřív si **sám přečti** `<model>\vystupy\makro_chyby.txt` (chyby za běhu).
- Okno *CompileError* (chyba překladu) se do logu nezapisuje: požádej o **výřez obrazovky –
  Win+Shift+S a Ctrl+V do chatu**. Nežádej ruční kopírování textu.
- `CS0117`, `CS1061` = neexistující člen API → ověř v XML, oprav.
- Oprav **jednu věc**, nasaď, nech spustit znovu.

## 5. Když funguje

- Navrhni uložit do `knihovna/` a zapsat do `knihovna/README.md` (co dělá, čte/mění, verze, datum).
- Zeptej se, zda nové pravidlo (UDA, zápis profilu) přidat do `CLAUDE.md`.

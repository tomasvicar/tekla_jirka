---
name: tekla-makro
description: Napíše, nasadí a odladí C# makro pro Tekla Structures (Open API, modelovací makro .cs). Použij, když uživatel chce v Tekle něco vypsat, zkontrolovat nebo hromadně změnit pomocí makra, nebo když vloží chybu z makra.
---

# Makro pro Teklu: napsat → nasadit → spustit → opravit

Uživatel je konstruktér, **neprogramuje**. Mluv česky a jednoduše. Pravidla a cesty jsou v `CLAUDE.md`.

## 1. Ujasni zadání (krátce)

- Co má makro udělat a na čem: na **vybraných** dílech, nebo na celém modelu?
- **Jen čte**, nebo **mění model**? Když mění, nejdřív napiš verzi, která jen vypíše, co by změnila.
- Kam má jít výstup (CSV do `<model>\vystupy\`, hláška v okně)?

## 2. Napiš makro

- Začni od nejbližšího ověřeného makra v `knihovna/` (nebo vzoru v `makra/`), ne od nuly.
- Kostra: `namespace Tekla.Technology.Akit.UserScript`, třída `Script`,
  `public static void Run(Tekla.Technology.Akit.IScript akit)`.
- Povinně: kontrola `GetConnectionStatus()`, `try/catch` s `MessageBox.Show(ex.ToString())`,
  nastavení jako konstanty nahoře, české komentáře.
- **Každý člen API ověř** v `reference/*.xml` (grep např. `P:Tekla.Structures.Model.Part.Class`)
  nebo v příkladech TSOpenAPIExamples pro správnou verzi. Neověřené označ `// NEOVĚŘENO:`.
- Změny modelu: kontrola, že jde o kopii (cesta obsahuje „kopie“/„test“), potvrzovací dialog
  s počtem dílů, `Modify()` / `SetUserProperty()`, nakonec **jedno** `model.CommitChanges("popis")`.
- Je-li k dispozici `dotnet`, zkontroluj překlad v `kontrola/` proti NuGet balíčku verze Tekly.

## 3. Nasaď

- Kopírování a hledání cest děláš ty, ne uživatel. Cesty ber z `CLAUDE.md`, a když tam nejsou, najdi je čtením disku.
- Hlavní kopii ulož do `makra/<NN_Nazev>.cs`.
- Zkopíruj ji do složky maker testovacího modelu (`<model>\macros\modeling\`, viz `CLAUDE.md`).
- Řekni uživateli přesně:
  1. v Tekle otevřít **kopii** modelu, případně vybrat díly,
  2. **Applications & components** → **Applications** → dvojklik na makro,
  3. když makro v seznamu není: v katalogu **Catalog management → Reload catalog**,
  4. co má vidět, když je vše v pořádku.

## 4. Když to nefunguje

- Požádej o **celý text chybového okna** (klik do okna, Ctrl+C) nebo snímek obrazovky.
- Případně si přečti nejnovější log Tekly (cesta v `CLAUDE.md`, hledej řádky s `error` a název makra).
- Chyby překladu (`CS0117`, `CS1061` = „neexistuje člen“) skoro vždy znamenají vymyšlený nebo
  špatně napsaný člen API → ověř v XML dokumentaci, oprav, znovu nasaď.
- Oprav **jednu věc**, nasaď a nech uživatele spustit znovu. Neměň víc najednou.

## 5. Když makro funguje

- Navrhni uložit ho do `knihovna/` s krátkým popisem v `knihovna/README.md`
  (co dělá, čte/mění, verze Tekly, datum ověření).
- Pokud uživatel používá git: commit s popisem „makro X ověřeno v Tekle <verze>“.
- Zeptej se, zda pravidlo, které se ukázalo (např. název UDA, zápis profilu), přidat do `CLAUDE.md`.

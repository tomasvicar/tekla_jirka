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
- `GetConnectionStatus()`, `try/catch` s `MessageBox.Show(ex.ToString())`, nastavení jako konstanty nahoře.
- **Každý člen API ověř** v `reference/*.xml` (když chybí, na developer.tekla.com pro verzi
  z `CLAUDE.md`), neověřené označ `// NEOVĚŘENO:`.
- Změny modelu: kontrola, že název složky modelu obsahuje „KOPIE“, potvrzovací dialog s počtem dílů, při chybě u části dílů
  seznam a dotaz před `CommitChanges`, jedno `CommitChanges`.
- Máš-li `dotnet`, zkontroluj překlad proti NuGet balíčku verze Tekly.

## 3. Nasaď

- Ulož do `makra/<NN_Nazev>.cs` a zkopíruj do `<model>\macros\modeling\` (cesta v `CLAUDE.md`).
- Řekni uživateli: otevřít **kopii**, vybrat díly, **Applications & components → Applications**
  → dvojklik; když chybí, **Reload catalog**. A co má vidět, když je vše v pořádku.

## 4. Když to nefunguje

- Požádej o celý text chybového okna (Ctrl+C), případně čti log Tekly.
- `CS0117`, `CS1061` = neexistující člen API → ověř v XML, oprav.
- Oprav **jednu věc**, nasaď, nech spustit znovu.

## 5. Když funguje

- Navrhni uložit do `knihovna/` a zapsat do `knihovna/README.md` (co dělá, čte/mění, verze, datum).
- Zeptej se, zda nové pravidlo (UDA, zápis profilu) přidat do `CLAUDE.md`.

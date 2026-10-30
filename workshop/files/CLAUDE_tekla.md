# Pravidla pro Clauda – automatizace Tekla Structures

Tento soubor patří do hlavní složky projektu s makry (např. `C:\Users\<jméno>\tekla-automatizace\`)
a jmenuje se `CLAUDE.md`. Hodnoty v `< >` doplňte podle svého počítače.

## Kdo jsem a jak se mnou mluvit

- Jsem konstruktér / detailer v Tekla Structures. **Neprogramuji.** Odpovídej česky, stručně a bez žargonu.
- Po každé změně napiš: co jsi vytvořil (cesta k souboru), jak to v Tekle spustím
  a co ti mám poslat zpět, když to selže.
- Normy (ČSN, Eurokódy) a statiku nikdy neuváděj jako ověřený fakt. Výsledky musí zkontrolovat odborník.

## Prostředí

- Tekla Structures **<2025 SPx / 2026 SPx>**, prostředí **<Czech / Default>**, jazyk Tekly **<čeština / angličtina>**.
- NuGet balíček odpovídající verzi: `Tekla.Structures.Model` **<2025.0.0 / 2026.0.3>**.
- Testovací model (KOPIE): `<C:\TeklaStructuresModels\Projekt_KOPIE>`
- Makra pro testovací model: `<C:\TeklaStructuresModels\Projekt_KOPIE>\macros\modeling\`
- Sdílená makra (XS_MACRO_DIRECTORY): `<C:\ProgramData\Trimble\Tekla Structures\<verze>\environments\common\macros\modeling>`
- Logy Tekly (ověřit): `%LOCALAPPDATA%\Trimble\Tekla Structures\<verze>\Logs` nebo `<model>\logs`
- Složky projektu: `makra/` (zdrojové .cs, hlavní kopie), `knihovna/` (ověřená makra), `reference/` (XML dokumentace API a příklady), `vystupy/`.

## Tvrdá pravidla

1. **Nevymýšlej API.** Každou třídu, metodu a vlastnost Tekla Open API nejdřív ověř:
   1. `reference/*.xml` (XML dokumentace z NuGet balíčku pro moji verzi) – hledej např. `M:Tekla.Structures.Model.Part.`,
   2. oficiální příklady TSOpenAPIExamples, větev = moje verze (`reference/TSOpenAPIExamples`),
   3. developer.tekla.com/doc/tekla-structures/<rok>/…
   Když nejde ověřit, napiš to do komentáře `// NEOVĚŘENO:` a řekni mi to.
2. **Model měním jen na kopii a jen s potvrzením.** Makro, které mění model, musí:
   - zkontrolovat, že cesta k modelu obsahuje „kopie“ nebo „test“,
   - před změnou ukázat dialog „Změním N dílů … Pokračovat?“,
   - zavolat `model.CommitChanges("popis")` **jednou** na konci (= jedno Ctrl+Z).
3. **Nejdřív jen čtení.** Nové makro napiš nejprve tak, aby jen četlo a vypsalo, co by změnilo.
4. Modelových souborů (`.db1`, `.db2`, složky modelů) se přímo nedotýkej. Makra jen zapisuj do složky maker; spouštím je já.
5. Nic nemaž a nepřepisuj ve `knihovna/` bez mého souhlasu.

## Nastavení dělá agent, ne já

- Cesty (model, složky maker, `XS_MACRO_DIRECTORY`, logy) zjisti sám čtením disku a zapiš je sem.
  Co nenajdeš, označ „NEOVĚŘENO“ a zeptej se.
- Makra kopíruj do složky maker sám. Mně napiš jen, co mám v Tekle kliknout.
- Konfiguraci (`%APPDATA%\Claude\claude_desktop_config.json`, `.claude/settings.json`) měň takto:
  nejdřív záloha souboru, pak mi ukaž změnu a počkej na souhlas, nakonec ověř platnost JSON.
  Potom mi řekni, co mám restartovat.
- Já sám: zálohu a kopii modelu, schvalování povolení, restart Claude Desktop a spuštění makra v Tekle.

## Kostra makra (ověřená konvence)

- Jeden soubor `.cs` = jedno makro, název česky bez diakritiky, např. `04_Soucet_hmotnosti.cs`.
- Vstupní bod jako v oficiálních příkladech:
  `namespace Tekla.Technology.Akit.UserScript { public class Script { public static void Run(Tekla.Technology.Akit.IScript akit) { … } } }`
- `using Tekla.Structures.Model;`, `using System.Windows.Forms;` (MessageBox).
- Na začátku `new Model().GetConnectionStatus()`, celé tělo v `try/catch` s `MessageBox.Show(ex.ToString())`.
- Nastavení (názvy UDA, třídy, seznamy profilů) jako konstanty nahoře s českým komentářem.
- Výstupy do `<model>\vystupy\` jako CSV se středníkem, UTF-8 s BOM, česká desetinná čárka.
- Na konci souboru komentář „OVĚŘENÍ API“: co je ověřené a co ne.
- Před předáním: pokud je k dispozici `dotnet`, zkontroluj překlad v `kontrola/` (projekt net48 nebo
  net8.0-windows + NuGet balíček mé verze + zástupné rozhraní `IScript`).

## Moje prostředí (CZ)

- Profily používám v zápisu katalogu Tekly, např. `HEA200`, `IPE300`, `UPE160`, `L80*8`, `PL10*200`, `RHS100*100*5`.
  Přesný zápis vždy ověř v mém katalogu (exportu profilů), nehádej.
- Materiály: `S235JR`, `S355J2`, beton `C30/37` – zápis podle mého materiálového katalogu.
- Uživatelské atributy (UDA), které používáme: `<USER_FIELD_1 = stav kontroly>`, `<…>`.
- Třídy (CLASS) v kanceláři: `<1 = sloupy, 2 = nosníky, …>`.

# 12 – České a slovenské zdroje: AI + automatizace v Tekla Structures

*Rešerše k 30. 10. 2026. Každé tvrzení má zdroj; položky označené **[neověřeno]** jsou odvozené nebo je nešlo potvrdit z veřejných stránek.*

## 1. Místní distributor: Construsoft (CZ + SK)

- **Construsoft s.r.o.** je oficiální prodejce Tekla Structures pro ČR, adresa Sadová 2374/2, Přerov, e-mail info-cz@construsoft.com. Zdroje: https://www.tekla.com/us/node/111 a https://www.construsoft.com/cs
- Construsoft dodává a podporuje Tekla Structures a Trimble Connect ve více než 30 zemích, **včetně ČR a Slovenska**. Samostatného slovenského prodejce jsem nenašel, Slovensko tedy nejspíš obsluhuje česká pobočka **[neověřeno]**. Zdroj: https://www.dlubal.com/cs/podpora-a-skoleni/skoleni/webinare/002305
- Kontaktní osoba pro prodej, implementaci a školení je Ing. David Neužil (Construsoft). Zdroj: tamtéž (webinář Dlubal RFEM ↔ Tekla, 2021, česky, záznam je dostupný).
- **Školení:** Construsoft dělá individuální školení podle úrovně uživatele (nejvýše 5 lidí), e-learning Tekla (ocel, přípoje, výrobní výstupy) a certifikaci buildingSMART. Uvádí také, že náklady může z velké části pokrýt dotace. Telefon +420 728 488 667. Zdroj: https://www.construsoft.com/cs/sluzby/skoleni
- **Kurz Open API / makra v češtině jsem nenašel.** Polský Construsoft takový kurz má: „Tekla Open API – wprowadzenie“ (C#, Visual Studio 2022, licence Educational). Zdroje: https://construsoft.com/pl/tekla-open-api-wprowadzenie-do-programowania-w-tekla-structures a https://construsoft.com/pl/szkolenie-tekla-open-api. Dá se zeptat, jestli by ho šlo vést česky nebo online **[neověřeno]**.

### Webináře Construsoft CZ (výběr AI/automatizace)
Zdroj: https://www.construsoft.com/cs/webinare
- **19. 11. 2026, 8:00 – „Výkresy na pár kliknutí? Automatizace a AI v Tekla Structures“** (40 min): automatické výrobní výkresy a AI nástroje, které generují nové výkresy. Registrace: https://www.construsoft.com/cs/webinar/vykresy-na-par-kliknuti-automatizace-ai-v-tekla-structures
- **25. 6. 2026 – „Modelování a tvorba výkresové dokumentace s využitím AI“** (Jan Matuš): AI asistent pro přípoje a modelování, AI klonování výkresů. Záznam je k dispozici: https://www.construsoft.com/cs/webinar/modelovani-tvorba-vykresove-dokumentace-s-vyuzitim-ai
- **5. 11. 2026 – automatická validace IFC pomocí IDS v Trimble Connect**; **23. 10. 2026 – AI asistent pro vyhledávání v modelu.** Zdroj: stránka webinářů výše.
- Žádný z webinářů nezmiňuje Open API, makra ani CZ prostředí. Zdroj: stránka webinářů výše.

### Akce
- **Connected Construction Days 2026**, 26.–28. 5. 2026, Brno (OREA Congress Hotel). Pořádal Construsoft CZ & SK s Trimble, Sitech a Geotronics. Zdroje: https://www.fce.vutbr.cz/api/cs/extSoubor/1224 a https://cz.linkedin.com/in/matasovsky
- Na LinkedInu se zmiňuje CZ/SK „User Day 2026“, ale nepodařilo se ověřit, jestli šlo o Tekla User Day. Zdroj: https://cz.linkedin.com/in/srbecky **[neověřeno]**
- Online workshop „AI in Tekla Structures. Build your own MCP“ (Vitali Mezen, 22. 4. 2026, anglicky). Zdroj: https://addcal.co/e/e2dx35ha75hg

## 2. CZ prostředí (environment) a lokalizace vs. makra

- Tekla podporuje češtinu jako jazyk rozhraní (csy). Zdroj: https://support.tekla.com/cs/doc/tekla-structures/2021/gen_changing_language_of_user_interface
- Prostředí (environment) určuje materiály, profily, výkresová nastavení a .ini pro danou zemi. Lokalizační poznámky dodávají místní týmy a prodejci. Zdroje: https://support.tekla.com/doc/tekla-structures/2026/ins_configurations_environments_roles a https://support.tekla.com/cs/doc/tekla-structures/2026/rel_localization_notes
- **Veřejně dostupný seznam obsahu CZ prostředí jsem nenašel.** Profily a další obsah se dají doplnit z Tekla Warehouse. Zdroj: https://support.tekla.com/doc/tekla-structures/2026/ins_configurations_environments_roles
- **Dopad na AI a makra:** Trimble Developer Assistant doporučuje použít prostředí *Default*, protože kód generuje s jeho profily. Zdroj: https://support.tekla.com/de/doc/tekla-structures/not-version-specific/developer_assistant
  Z toho plyne, že v CZ prostředí je potřeba AI výslovně zadat názvy profilů, materiálů a UDA z vlastního katalogu **[odvozeno]**. Názvy dialogů a atributů v nahraných makrech jsou interní (anglické), takže jazyk rozhraní by na ně neměl mít vliv. Názvy profilů, tříd a vlastních atributů ale na prostředí závisí **[neověřeno]**.
- Ne všechno jde nahrát jako makro. Tekla v takových případech doporučuje dopsat logiku přes Open API. Zdroj: https://support.tekla.com/article/not-all-tekla-structures-functionalities-can-be-recorded-as-a-macro-script

## 3. Komunita, univerzity, odborné články

- **Facebook skupinu, YouTube kanál ani fórum zaměřené na Teklu v češtině nebo slovenštině jsem nenašel** **[neověřeno: bez přihlášení na FB/LinkedIn]**. Oficiální videa jsou na https://www.youtube.com/user/TeklaStructures, playlist k Open API je na https://developer.tekla.com/tekla-open-api-coding-videos-now-available
- Česká příručka „01. Základy programu Tekla Structures“ (PDF): https://support.tekla.com/dist/sxf/document/01.-zaklady-programu-tekla-structures.pdf
- **ČVUT FSv, K. Toman: „Chat GPT-4o z pohledu statika“ (PhD workshop 2025).** Jazykový model nezná systém českých a evropských norem. Podle závěru je použitelný „pro řešení odborných dotazů v kombinaci s ověřením podle normových předpisů“. Zdroj: https://concrete.fsv.cvut.cz/phdworkshop/proceedings/2025/pdf/Toman_Krystof.pdf
- ČVUT, předmět 124YMOB „Modelování budov – BIM“ (vizuální programování, Z. Malík): https://bilakniha.cvut.cz/en/predmet6879106.html. Diplomka „Parametrické modelování halových konstrukcí“: https://dspace.cvut.cz/handle/10467/113727 (obsah se nepodařilo načíst) **[neověřeno]**
- Obecné české články o AI a BIM: TZB-info https://www.tzb-info.cz/bim-informacni-model-budovy/28177-kombinace-ai-a-bim-pomaha-automatizovat-procesy, ESTAV (AI ve stavebnictví je „v počátcích“) https://www.estav.cz/cz/12698.experti-uziti-ai-ve-stavebnictvi-je-v-pocatcich-vhodna-je-pro-statni-spravu, Dlubal blog https://www.dlubal.com/cs/akce-a-novinky/novinky/blog/000097
- K ČKAIT, CzBIM ani BIMfo.cz jsem nenašel článek o LLM a Tekle **[nenalezeno]**.

## 4. AI nástroje přímo pro Teklu (relevantní pro CZ uživatele)

- **Trimble Assistant for Tekla**: User Assistant odpovídá podle manuálů. **Developer Assistant** píše makra přes Open API, kód umí spustit a uložit jako makro do katalogu Aplikace a komponenty. Vyžaduje Diamond named-user, licenci Tekla Partners nebo Trimble Labs. Zdroje: https://support.tekla.com/de/doc/tekla-structures/not-version-specific/developer_assistant a https://support.tekla.com/cs/trimble-assistant-for-tekla (vyžaduje přihlášení)
- **Tekla Model Assistant (Preview)**: zadání v přirozeném jazyce, jen pro Diamond, Graphite a Carbon. Zdroj: https://support.tekla.com/doc/tekla-structures/2026/mod_tekla_model_assistant
- Open-source **tekla_mcp_server** (GPL-3, Python, testováno s Tekla 2022 a 2026): https://github.com/teknovizier/tekla_mcp_server

## 5. Claude v češtině

- Oficiální český návod na Claude Code jsem nenašel. Existuje český tutoriál třetí strany: https://www.nxcode.io/cs/resources/news/claude-code-tutorial-beginners-guide-2026. Obecné české články jsou spíš marketingové, např. https://clickup.com/cs/blog/270145/jak-pouzivat-claude-ai/
- Anthropic zveřejňuje benchmark pro 14 jazyků a **čeština v něm není**. Uvádí ale, že Claude zvládá i jazyky mimo tabulku, a doporučuje výslovně určit jazyk odpovědi a otestovat si vlastní úlohy. Zdroj: https://platform.claude.com/docs/en/build-with-claude/multilingual-support
- Nezávislý test Claude v češtině na technických úlohách jsem nenašel **[nenalezeno]**.

## 6. Ceny, zkušební verze, vzdělávací licence

- Ceny v Kč nejsou veřejné, jen přes prodejce nebo webshop. Konfigurace jsou Carbon, Graphite a Diamond. Zdroje: https://support.tekla.com/cs/article/frequently-asked-questions-tekla-structures-subscription-licensing a https://www.construsoft.com/cs/webshop
- **Demo licence zdarma** přes formulář: https://www.construsoft.com/cs/zkusebni-verze. Webináře nabízejí měsíc zkušební verze zdarma (viz webinář z 19. 11.).
- **Tekla Campus**: Learning Edition zdarma na 4 měsíce, s vodoznakem a omezeným importem a exportem, nesmí se používat komerčně. Zdroje: https://www.construsoft.com/cs/tekla-campus a https://support.tekla.com/pl/bulletin/do-not-save-production-model-with-tekla-structures-learning-edition
- Smlouvy s konkrétními univerzitami (ČVUT, VUT, STU) jsem neověřil **[neověřeno]**.

## Doporučené postupy / Recommended practices

1. **Začít u Construsoftu.** Zapsat se na webinář 19. 11. 2026 o AI a automatizaci, pustit si záznam z 25. 6. a zeptat se Ing. Neužila na kurz Open API v češtině nebo na polský kurz online (zdroje v oddílu 1).
2. **Výstupy AI vždy ověřit podle norem.** To je hlavní závěr práce z ČVUT (Toman 2025). AI je dobrá na rešerše, skladby a stálá zatížení, ne na součinitele z norem.
3. **Zadávat AI kontext CZ prostředí.** Developer Assistant počítá s prostředím Default. Do promptu je proto vhodné vložit vlastní názvy profilů, materiálů a UDA a nejdřív testovat na kopii modelu.
4. **Kde nahrávání makra nestačí, použít Open API.** Tekla to sama doporučuje. AI (Developer Assistant, Claude) může pomoct vygenerovat C#.
5. **Psát česky, ale jazyk odpovědi určit výslovně.** Doporučuje to Anthropic. Technické názvy (API třídy, atributy) je lepší nechat v angličtině **[odvozeno]**.
6. **Na učení použít Learning Edition nebo demo licenci**, ne produkční modely (bulletin Tekla).

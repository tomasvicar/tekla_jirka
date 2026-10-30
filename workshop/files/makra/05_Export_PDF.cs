// ============================================================================
// 05_Export_PDF.cs  –  Tekla Structures 2025 / 2026, modelovací makro
//
// CO DĚLÁ:   Vytiskne všechny výkresy do PDF a rovnou je roztřídí do složek:
//            <model>\PDF_export\<datum>\Sestavy\A.1.pdf
//                                     \Dilce\P.12.pdf
//                                     \Vykresy_rozmisteni\G.3.pdf
//                                     \Prefabrikaty\...   \Ostatni\...
//            Nakonec zapíše přehled do <model>\PDF_export\<datum>\prehled_exportu.txt
// MODEL:     JEN ČTE. Model ani výkresy nemění.
// SPUŠTĚNÍ:  Claude makro přeloží a zkopíruje do <složka modelu>\macros\modeling\.
//            V Tekle: Applications & components (panel vpravo) -> ≡ -> Catalog management
//            -> Reload catalog, vyhledat název makra, dvojklik.
//            Předtím zavřete otevřený výkres (tisk otevřeného výkresu selže).
// CHYBY:     Chyba za běhu se zapíše do <model>\vystupy\makro_chyby.txt.
//            Chyba překladu (okno CompileError): Win+Shift+S, Ctrl+V do chatu s Claudem.
//
// STAV:      VYZKOUŠENO 30. 10. 2026 na Tekle 2026 SP1 (zkušební verze): 4 výkresy
//            (2 sestavy, 2 dílce) vytištěny do PDF_export\<datum>\Sestavy|Dilce, 0 chyb.
//            Poprvé zkuste na pár výkresech (nastavte JEN_VYBRANE = true).
// ============================================================================

using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Windows.Forms;
using Tekla.Structures.Drawing;

namespace Tekla.Technology.Akit.UserScript
{
    public class Script
    {
        // --- NASTAVENÍ (upravte podle sebe, nebo o to požádejte Clauda) --------

        // Hlavní složka pro PDF. Vznikne uvnitř složky modelu.
        private const string HLAVNI_SLOZKA = "PDF_export";

        // true = každý export do vlastní složky s dnešním datem (např. 2026-10-30).
        private const bool SLOZKA_S_DATEM = true;

        // Do které podsložky patří který druh výkresu.
        private const string SLOZKA_SESTAVY = "Sestavy";              // výkresy sestav
        private const string SLOZKA_DILCE = "Dilce";                  // výkresy dílců (single part)
        private const string SLOZKA_ROZMISTENI = "Vykresy_rozmisteni"; // výkresy rozmístění (GA)
        private const string SLOZKA_PREFABRIKATY = "Prefabrikaty";    // výkresy prefabrikátů (cast unit)
        private const string SLOZKA_OSTATNI = "Ostatni";              // vše ostatní (multi výkresy...)

        // true = jen výkresy vybrané v seznamu výkresů (Document manager).
        // false = všechny výkresy v modelu.
        private const bool JEN_VYBRANE = false;

        // true = neaktuální výkresy (model se od té doby změnil) přeskočit a jen vypsat.
        // false = vytisknout i je.
        private const bool PRESKOCIT_NEAKTUALNI = true;

        // Název souboru:
        //   false = značka výkresu, např. A.1.pdf (když značka chybí, použije se název výkresu)
        //   true  = název, jaký Tekla dává při tisku, např. A1 - SLOUP.pdf (může obsahovat revizi)
        private const bool NAZEV_JAKO_TEKLA = false;

        // Formát papíru a barvy. Auto = podle výkresu.
        private const DotPrintPaperSize PAPIR = DotPrintPaperSize.Auto;
        private const DotPrintColor BARVY = DotPrintColor.BlackAndWhite;
        // ----------------------------------------------------------------------

        public static void Run(Tekla.Technology.Akit.IScript akit)
        {
            try
            {
                Tekla.Structures.Model.Model model = new Tekla.Structures.Model.Model();
                DrawingHandler vykresy = new DrawingHandler();

                // 1) Je Tekla spuštěná a je otevřený model?
                if (!model.GetConnectionStatus() || !vykresy.GetConnectionStatus())
                {
                    MessageBox.Show("Makro se nepřipojilo k Tekle. Je otevřený model?", "Export PDF");
                    return;
                }

                // 2) Otevřený výkres se vytisknout nedá -> požádáme o zavření.
                if (vykresy.IsAnyDrawingOpen())
                {
                    MessageBox.Show("Je otevřený výkres. Zavřete ho a spusťte makro znovu.", "Export PDF");
                    return;
                }

                // 3) Kam ukládat.
                string koren = Path.Combine(model.GetInfo().ModelPath, HLAVNI_SLOZKA);
                if (SLOZKA_S_DATEM) koren = Path.Combine(koren, DateTime.Now.ToString("yyyy-MM-dd"));

                // 4) Projdeme výkresy a každému určíme složku a název souboru.
                DrawingEnumerator seznam = JEN_VYBRANE
                    ? vykresy.GetDrawingSelector().GetSelected()
                    : vykresy.GetDrawings();

                List<Drawing> kTisku = new List<Drawing>();
                List<string> cesty = new List<string>();
                List<string> neaktualni = new List<string>();
                Dictionary<string, int> pocetVeSlozce = new Dictionary<string, int>();
                HashSet<string> pouziteNazvy = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

                while (seznam.MoveNext())
                {
                    Drawing vykres = seznam.Current;
                    if (vykres == null) continue;

                    string nazev = NazevSouboru(vykres);

                    if (PRESKOCIT_NEAKTUALNI && !JeAktualni(vykres))
                    {
                        neaktualni.Add(nazev + "  (" + vykres.UpToDateStatus + ")");
                        continue;
                    }

                    string slozka = SlozkaPro(vykres);
                    string cesta = Path.Combine(koren, slozka, nazev + ".pdf");

                    // Dva výkresy se stejným názvem -> druhý dostane _2, _3...
                    int n = 2;
                    while (pouziteNazvy.Contains(cesta))
                        cesta = Path.Combine(koren, slozka, nazev + "_" + n++ + ".pdf");
                    pouziteNazvy.Add(cesta);

                    kTisku.Add(vykres);
                    cesty.Add(cesta);
                    if (!pocetVeSlozce.ContainsKey(slozka)) pocetVeSlozce[slozka] = 0;
                    pocetVeSlozce[slozka]++;
                }

                if (kTisku.Count == 0)
                {
                    MessageBox.Show("Není co tisknout." +
                        (JEN_VYBRANE ? "\nVyberte výkresy v seznamu výkresů." : "") +
                        (neaktualni.Count > 0 ? "\nNeaktuálních výkresů: " + neaktualni.Count : ""),
                        "Export PDF");
                    return;
                }

                // 5) Potvrzení: kolik výkresů půjde do které složky.
                StringBuilder dotaz = new StringBuilder();
                dotaz.AppendLine("Vytisknout " + kTisku.Count + " výkresů do PDF?");
                dotaz.AppendLine();
                foreach (KeyValuePair<string, int> p in pocetVeSlozce)
                    dotaz.AppendLine("   " + p.Key + ":  " + p.Value);
                if (neaktualni.Count > 0)
                {
                    dotaz.AppendLine();
                    dotaz.AppendLine("Přeskočím neaktuální výkresy: " + neaktualni.Count);
                }
                dotaz.AppendLine();
                dotaz.AppendLine("Složka:");
                dotaz.AppendLine(koren);
                if (MessageBox.Show(dotaz.ToString(), "Export PDF", MessageBoxButtons.YesNo)
                    != DialogResult.Yes)
                    return;

                // 6) Tisk. Chyba u jednoho výkresu nezastaví ostatní.
                DPMPrinterAttributes tisk = new DPMPrinterAttributes();
                tisk.OutputType = DotPrintOutputType.PDF;
                tisk.PaperSize = PAPIR;
                tisk.ColorMode = BARVY;
                tisk.Orientation = DotPrintOrientationType.Auto;
                tisk.ScalingMethod = DotPrintScalingType.Auto;
                tisk.OpenFileWhenFinished = false;

                List<string> chyby = new List<string>();
                List<string> hotovo = new List<string>();
                for (int i = 0; i < kTisku.Count; i++)
                {
                    try
                    {
                        Directory.CreateDirectory(Path.GetDirectoryName(cesty[i]));
                        if (vykresy.PrintDrawing(kTisku[i], tisk, cesty[i]))
                            hotovo.Add(cesty[i]);
                        else
                            chyby.Add(cesty[i] + "  (Tekla vrátila neúspěch)");
                    }
                    catch (Exception ex)
                    {
                        chyby.Add(cesty[i] + "  (" + ex.Message + ")");
                        ZapisChybu("05_Export_PDF  " + cesty[i], ex);
                    }
                }

                // 7) Přehled do textového souboru a na obrazovku.
                StringBuilder prehled = new StringBuilder();
                prehled.AppendLine("Export PDF  " + DateTime.Now.ToString("yyyy-MM-dd HH:mm"));
                prehled.AppendLine();
                prehled.AppendLine("VYTIŠTĚNO: " + hotovo.Count);
                foreach (string s in hotovo) prehled.AppendLine("   " + s);
                prehled.AppendLine();
                prehled.AppendLine("CHYBY: " + chyby.Count);
                foreach (string s in chyby) prehled.AppendLine("   " + s);
                prehled.AppendLine();
                prehled.AppendLine("PŘESKOČENO (neaktuální): " + neaktualni.Count);
                foreach (string s in neaktualni) prehled.AppendLine("   " + s);
                Directory.CreateDirectory(koren);
                string souborPrehledu = Path.Combine(koren, "prehled_exportu.txt");
                File.WriteAllText(souborPrehledu, prehled.ToString(), new UTF8Encoding(true));

                StringBuilder zprava = new StringBuilder();
                zprava.AppendLine("Vytištěno: " + hotovo.Count + " z " + kTisku.Count);
                if (neaktualni.Count > 0) zprava.AppendLine("Přeskočeno neaktuálních: " + neaktualni.Count);
                if (chyby.Count > 0)
                {
                    zprava.AppendLine();
                    zprava.AppendLine("NEPOVEDLO SE (" + chyby.Count + "):");
                    for (int i = 0; i < chyby.Count && i < 15; i++) zprava.AppendLine("   " + chyby[i]);
                    if (chyby.Count > 15) zprava.AppendLine("   ... a další, viz přehled");
                }
                zprava.AppendLine();
                zprava.AppendLine("Přehled:");
                zprava.AppendLine(souborPrehledu);
                MessageBox.Show(zprava.ToString(),
                    chyby.Count == 0 ? "Export PDF – hotovo" : "Export PDF – hotovo s chybami");
            }
            catch (Exception ex)
            {
                ZapisChybu("05_Export_PDF", ex);
                MessageBox.Show("Makro skončilo chybou:\n\n" + ex.ToString(), "Export PDF – CHYBA");
            }
        }

        // Druh výkresu -> podsložka.
        private static string SlozkaPro(Drawing vykres)
        {
            if (vykres is AssemblyDrawing) return SLOZKA_SESTAVY;
            if (vykres is SinglePartDrawing) return SLOZKA_DILCE;
            if (vykres is GADrawing) return SLOZKA_ROZMISTENI;
            if (vykres is CastUnitDrawing) return SLOZKA_PREFABRIKATY;
            return SLOZKA_OSTATNI;   // MultiDrawing a ostatní
        }

        // Aktuální = od vytvoření výkresu se model nezměnil (nebo byl výkres aktualizován).
        private static bool JeAktualni(Drawing vykres)
        {
            DrawingUpToDateStatus stav = vykres.UpToDateStatus;
            return stav == DrawingUpToDateStatus.DrawingIsUpToDate
                || stav == DrawingUpToDateStatus.DrawingIsUpToDateButMayNeedChecking
                || stav == DrawingUpToDateStatus.DrawingWasUpdated;
        }

        // Název souboru bez přípony, bez znaků, které Windows v názvu nedovolí.
        private static string NazevSouboru(Drawing vykres)
        {
            string nazev = NAZEV_JAKO_TEKLA ? vykres.GetPlotFileName(true) : vykres.Mark;
            if (string.IsNullOrWhiteSpace(nazev)) nazev = vykres.Name;
            if (string.IsNullOrWhiteSpace(nazev)) nazev = "vykres";

            // Značka bývá v hranatých závorkách, např. [A.1] -> A.1
            nazev = nazev.Replace("[", "").Replace("]", "");
            foreach (char c in Path.GetInvalidFileNameChars()) nazev = nazev.Replace(c, '_');
            nazev = nazev.Trim().TrimEnd('.');
            if (nazev.EndsWith(".pdf", StringComparison.OrdinalIgnoreCase))
                nazev = nazev.Substring(0, nazev.Length - 4);
            return nazev.Length == 0 ? "vykres" : nazev;
        }

        // Chybu zapíše i do <model>\vystupy\makro_chyby.txt, ať si ji Claude přečte sám.
        private static void ZapisChybu(string makro, Exception ex)
        {
            try
            {
                string slozka = Path.Combine(new Tekla.Structures.Model.Model().GetInfo().ModelPath, "vystupy");
                Directory.CreateDirectory(slozka);
                File.AppendAllText(Path.Combine(slozka, "makro_chyby.txt"),
                    DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss") + "  " + makro + "\r\n"
                    + ex.ToString() + "\r\n\r\n", System.Text.Encoding.UTF8);
            }
            catch { }   // zápis chyby nesmí shodit makro
        }
    }
}

// ----------------------------------------------------------------------------
// OVĚŘENÍ API (XML dokumentace Tekla.Structures.Drawing a .Model 2026):
//   PŘEKLAD: typová kontrola proti NuGet Tekla.Structures.Drawing + .Model 2025.0.0 i 2026.0.3
//            (mimo Teklu, se zástupným IScript) prošla bez chyb. Překladač Tekly to nenahrazuje.
//   ověřeno v dokumentaci: DrawingHandler (konstruktor, GetConnectionStatus, IsAnyDrawingOpen,
//            GetDrawings, GetDrawingSelector, PrintDrawing(Drawing, DPMPrinterAttributes, string)),
//            UI.DrawingSelector.GetSelected, DrawingEnumerator.MoveNext/Current,
//            Drawing.Mark/Name/UpToDateStatus/GetPlotFileName(bool),
//            AssemblyDrawing, SinglePartDrawing, GADrawing, CastUnitDrawing, MultiDrawing,
//            DPMPrinterAttributes.OutputType/PaperSize/ColorMode/Orientation/ScalingMethod/
//            OpenFileWhenFinished, výčty DotPrint*, DrawingUpToDateStatus,
//            Model.GetConnectionStatus, Model.GetInfo().ModelPath
//   Dokumentace: „The drawing cannot be active, otherwise printing fails.“ -> kontrola
//            IsAnyDrawingOpen na začátku.
//   OVĚŘENO: PrintDrawing přijme celou cestu k souboru; Mark dá název typu „A.1“.
//   NEOVĚŘENO: co vrací
//            GetPlotFileName(true) a zda zahrnuje revizi. Revize výkresu se v API výkresů
//            jako vlastnost nenašla; v názvu je jen přes GetPlotFileName (podle nastavení Tekly).
// ----------------------------------------------------------------------------

// ============================================================================
// 01_Vypis_vybranych_dilu.cs  –  Tekla Structures 2025 / 2026, modelovací makro
//
// CO DĚLÁ:   Vypíše vybrané díly (profil, materiál, třída, délka, hmotnost, UDA)
//            do CSV souboru ve složce modelu: <model>\vystupy\vybrane_dily_<čas>.csv
// MODEL:     JEN ČTE. Nic v modelu nemění, nevolá Modify() ani CommitChanges().
// SPUŠTĚNÍ:  1. Soubor zkopírujte do <složka modelu>\macros\modeling\
//            2. V Tekle vyberte několik dílů.
//            3. Applications & components -> Applications -> dvojklik na makro.
//               (Když makro v seznamu není: Catalog management -> Reload catalog.)
//
// STAV:      Napsáno podle dokumentace Tekla Open API 2025/2026 (NuGet XML),
//            NEOTESTOVÁNO na živé Tekle. Viz poznámky na konci souboru.
// ============================================================================

using System;
using System.Globalization;
using System.IO;
using System.Text;
using System.Windows.Forms;
using Tekla.Structures.Model;

namespace Tekla.Technology.Akit.UserScript
{
    public class Script
    {
        // --- NASTAVENÍ (upravte podle sebe) -----------------------------------
        // Názvy uživatelských atributů (UDA), které se mají vypsat.
        // USER_FIELD_1 je ve výchozím prostředí; vaše firma může mít jiné názvy.
        private static readonly string[] UDA_NAZVY = { "USER_FIELD_1", "USER_FIELD_2" };
        // ----------------------------------------------------------------------

        public static void Run(Tekla.Technology.Akit.IScript akit)
        {
            try
            {
                Model model = new Model();

                // 1) Je Tekla spuštěná a je otevřený model?
                if (!model.GetConnectionStatus())
                {
                    MessageBox.Show("Makro se nepřipojilo k Tekle. Je otevřený model?",
                        "Výpis dílů");
                    return;
                }

                // 2) Vybrané objekty z modelového pohledu (UI výběr).
                Tekla.Structures.Model.UI.ModelObjectSelector vyber =
                    new Tekla.Structures.Model.UI.ModelObjectSelector();
                ModelObjectEnumerator objekty = vyber.GetSelectedObjects();

                // CSV pro český Excel: oddělovač středník, desetinná čárka.
                CultureInfo cz = new CultureInfo("cs-CZ");
                StringBuilder csv = new StringBuilder();
                csv.Append("GUID;Jmeno;Profil;Material;Trida;Delka_mm;Hmotnost_kg");
                foreach (string uda in UDA_NAZVY) csv.Append(";" + uda);
                csv.AppendLine();

                int pocet = 0;
                while (objekty.MoveNext())
                {
                    // Zajímají nás jen díly (nosníky, sloupy, plechy, polynosníky).
                    Part dil = objekty.Current as Part;
                    if (dil == null) continue;

                    // Délka a hmotnost čteme jako "report properties" –
                    // stejné názvy jako v šablonách výkazů (LENGTH, WEIGHT).
                    double delka = 0.0;
                    double hmotnost = 0.0;
                    dil.GetReportProperty("LENGTH", ref delka);
                    dil.GetReportProperty("WEIGHT", ref hmotnost);

                    csv.Append(dil.Identifier.GUID.ToString());
                    csv.Append(";" + Bezpecne(dil.Name));
                    csv.Append(";" + Bezpecne(dil.Profile.ProfileString));
                    csv.Append(";" + Bezpecne(dil.Material.MaterialString));
                    csv.Append(";" + Bezpecne(dil.Class));
                    csv.Append(";" + delka.ToString("0.0", cz));
                    csv.Append(";" + hmotnost.ToString("0.00", cz));

                    foreach (string uda in UDA_NAZVY)
                    {
                        string hodnota = "";
                        dil.GetUserProperty(uda, ref hodnota);   // prázdné, když UDA není
                        csv.Append(";" + Bezpecne(hodnota));
                    }
                    csv.AppendLine();
                    pocet++;
                }

                if (pocet == 0)
                {
                    MessageBox.Show("Nebyl vybrán žádný díl. Vyberte díly v modelu a spusťte znovu.",
                        "Výpis dílů");
                    return;
                }

                // 3) Uložení do složky modelu\vystupy (UTF-8 s BOM, aby Excel ukázal diakritiku).
                string slozkaModelu = model.GetInfo().ModelPath;
                string slozkaVystupu = Path.Combine(slozkaModelu, "vystupy");
                Directory.CreateDirectory(slozkaVystupu);
                string soubor = Path.Combine(slozkaVystupu,
                    "vybrane_dily_" + DateTime.Now.ToString("yyyy-MM-dd_HHmmss") + ".csv");
                File.WriteAllText(soubor, csv.ToString(), new UTF8Encoding(true));

                MessageBox.Show("Vypsáno dílů: " + pocet + "\n\nSoubor:\n" + soubor,
                    "Výpis dílů – hotovo");
            }
            catch (Exception ex)
            {
                // Celý text chyby zkopírujte (Ctrl+C v okně) a vložte Claudovi.
                MessageBox.Show("Makro skončilo chybou:\n\n" + ex.ToString(), "Výpis dílů – CHYBA");
            }
        }

        // Odstraní středníky a konce řádků, aby se nerozbily sloupce v CSV.
        private static string Bezpecne(string text)
        {
            if (text == null) return "";
            return text.Replace(";", ",").Replace("\r", " ").Replace("\n", " ");
        }
    }
}

// ----------------------------------------------------------------------------
// OVĚŘENÍ API (NuGet Tekla.Structures.Model 2025.0.0 a 2026.0.3, XML dokumentace):
//   PŘEKLAD: typová kontrola proti Tekla.Structures.Model 2025.0.0 i 2026.0.3 (NuGet,
//            mimo Teklu, se zástupným IScript) prošla bez chyb. Překladač Tekly to nenahrazuje.
//   ověřeno: Model.GetConnectionStatus, Model.GetInfo, ModelInfo.ModelPath,
//            UI.ModelObjectSelector.GetSelectedObjects, ModelObjectEnumerator.MoveNext/Current,
//            Part.Name/Profile/Material/Class, Profile.ProfileString, Material.MaterialString,
//            ModelObject.GetReportProperty(string, ref double),
//            ModelObject.GetUserProperty(string, ref string), Object.Identifier, Identifier.GUID
//   vstupní bod Run(Tekla.Technology.Akit.IScript akit): podle oficiálního příkladu
//            TSOpenAPIExamples, větev 2025 i 2026 (RebarSample1B.cs)
//   NEOVĚŘENO z oficiálního zdroje: že makra mají System.Windows.Forms mezi výchozími
//            referencemi (běžně používané v komunitních makrech); názvy LENGTH a WEIGHT
//            jsou standardní atributy šablon výkazů – hodnoty zkontrolujte proti Tekle.
// ----------------------------------------------------------------------------

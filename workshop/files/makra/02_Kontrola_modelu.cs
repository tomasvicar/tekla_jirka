// ============================================================================
// 02_Kontrola_modelu.cs  –  Tekla Structures 2025 / 2026, modelovací makro
//
// CO DĚLÁ:   Projde všechny díly v modelu a najde podezřelé:
//              - chybějící nebo "nedefinovaný" materiál,
//              - profil, který vypadá jako výchozí (zapomenutý po modelování),
//              - prázdnou třídu (CLASS),
//              - nulovou hmotnost.
//            Výsledek zapíše do <model>\vystupy\kontrola_modelu_<čas>.csv
//            a na přání podezřelé díly v modelu VYBERE (označí), ať je vidíte.
// MODEL:     JEN ČTE. Výběr dílů je jen označení v pohledu, model se nemění.
// SPUŠTĚNÍ:  Claude makro přeloží a zkopíruje do <složka modelu>\macros\modeling\.
//            V Tekle: Applications & components (panel vpravo) -> ≡ -> Catalog management
//            -> Reload catalog, vyhledat název makra, dvojklik.
// CHYBY:     Chyba za běhu se zapíše do <model>\vystupy\makro_chyby.txt.
//            Chyba překladu (okno CompileError): Win+Shift+S, Ctrl+V do chatu s Claudem.
//
// STAV:      NEOTESTOVÁNO na živé Tekle. Seznamy níže upravte podle svého prostředí.
// ============================================================================

using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Text;
using System.Windows.Forms;
using Tekla.Structures.Model;

namespace Tekla.Technology.Akit.UserScript
{
    public class Script
    {
        // --- NASTAVENÍ (upravte podle svého prostředí) ------------------------
        // Materiály, které znamenají "nezadáno". Doplňte, co používá vaše prostředí.
        private static readonly string[] PODEZRELE_MATERIALY =
            { "", "Steel_Undefined", "Concrete_Undefined", "UNKNOWN" };

        // Profily, které u vás znamenají "výchozí, zapomenuté". Zjistěte je v Tekle:
        // vložte nový nosník bez úprav a v Inquire se podívejte na profil.
        // Pozor: nepište sem profil, který v modelu běžně používáte (např. sloupy HEA300).
        // Příklad zápisu: { "", "PL20*200", "D200" }
        private static readonly string[] PODEZRELE_PROFILY = { "" };
        // ----------------------------------------------------------------------

        public static void Run(Tekla.Technology.Akit.IScript akit)
        {
            try
            {
                Model model = new Model();
                if (!model.GetConnectionStatus())
                {
                    MessageBox.Show("Makro se nepřipojilo k Tekle. Je otevřený model?", "Kontrola modelu");
                    return;
                }

                // Všechny díly: nosníky/sloupy (Beam), polynosníky a plechy.
                ModelObjectEnumerator dily = model.GetModelObjectSelector().GetAllObjectsWithType(
                    new Type[] { typeof(Beam), typeof(PolyBeam), typeof(ContourPlate) });

                CultureInfo cz = new CultureInfo("cs-CZ");
                StringBuilder csv = new StringBuilder();
                csv.AppendLine("GUID;Jmeno;Profil;Material;Trida;Hmotnost_kg;Problem");

                ArrayList podezrele = new ArrayList();
                Dictionary<string, int> souhrn = new Dictionary<string, int>();
                int celkem = 0;

                while (dily.MoveNext())
                {
                    Part dil = dily.Current as Part;
                    if (dil == null) continue;
                    celkem++;

                    string profil = dil.Profile.ProfileString ?? "";
                    string material = dil.Material.MaterialString ?? "";
                    string trida = dil.Class ?? "";
                    double hmotnost = 0.0;
                    dil.GetReportProperty("WEIGHT", ref hmotnost);

                    List<string> problemy = new List<string>();
                    if (ObsahujeBezVelikosti(PODEZRELE_MATERIALY, material)) problemy.Add("material nezadan");
                    if (ObsahujeBezVelikosti(PODEZRELE_PROFILY, profil)) problemy.Add("vychozi profil");
                    if (trida.Trim() == "") problemy.Add("prazdna trida");
                    if (hmotnost <= 0.0) problemy.Add("nulova hmotnost");

                    if (problemy.Count == 0) continue;

                    podezrele.Add(dil);
                    foreach (string p in problemy)
                        souhrn[p] = souhrn.ContainsKey(p) ? souhrn[p] + 1 : 1;

                    csv.AppendLine(string.Join(";", new string[] {
                        dil.Identifier.GUID.ToString(), Bezpecne(dil.Name), Bezpecne(profil),
                        Bezpecne(material), Bezpecne(trida), hmotnost.ToString("0.00", cz),
                        string.Join(", ", problemy.ToArray()) }));
                }

                if (podezrele.Count == 0)
                {
                    MessageBox.Show("Zkontrolováno dílů: " + celkem + "\nŽádný problém nenalezen.",
                        "Kontrola modelu – OK");
                    return;
                }

                string slozka = Path.Combine(model.GetInfo().ModelPath, "vystupy");
                Directory.CreateDirectory(slozka);
                string soubor = Path.Combine(slozka,
                    "kontrola_modelu_" + DateTime.Now.ToString("yyyy-MM-dd_HHmmss") + ".csv");
                File.WriteAllText(soubor, csv.ToString(), new UTF8Encoding(true));

                StringBuilder zprava = new StringBuilder();
                zprava.AppendLine("Zkontrolováno dílů: " + celkem);
                zprava.AppendLine("Podezřelých dílů: " + podezrele.Count);
                foreach (KeyValuePair<string, int> polozka in souhrn)
                    zprava.AppendLine("  - " + polozka.Key + ": " + polozka.Value);
                zprava.AppendLine();
                zprava.AppendLine("Seznam: " + soubor);
                zprava.AppendLine();
                zprava.AppendLine("Mám podezřelé díly v modelu vybrat (označit)?");

                DialogResult odpoved = MessageBox.Show(zprava.ToString(),
                    "Kontrola modelu – výsledek", MessageBoxButtons.YesNo);
                if (odpoved == DialogResult.Yes)
                {
                    // Jen výběr v pohledu – nic se v modelu nemění.
                    new Tekla.Structures.Model.UI.ModelObjectSelector().Select(podezrele);
                }
            }
            catch (Exception ex)
            {
                ZapisChybu("02_Kontrola_modelu", ex);
                MessageBox.Show("Makro skončilo chybou:\n\n" + ex.ToString(), "Kontrola modelu – CHYBA");
            }
        }

        private static bool ObsahujeBezVelikosti(string[] seznam, string hodnota)
        {
            foreach (string s in seznam)
                if (string.Equals(s, hodnota.Trim(), StringComparison.OrdinalIgnoreCase)) return true;
            return false;
        }

        private static string Bezpecne(string text)
        {
            if (text == null) return "";
            return text.Replace(";", ",").Replace("\r", " ").Replace("\n", " ");
        }

        // Chybu zapíše i do <model>\vystupy\makro_chyby.txt, ať si ji Claude přečte sám.
        private static void ZapisChybu(string makro, Exception ex)
        {
            try
            {
                string slozka = Path.Combine(new Model().GetInfo().ModelPath, "vystupy");
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
// OVĚŘENÍ API (NuGet Tekla.Structures.Model 2025.0.0 a 2026.0.3, XML dokumentace):
//   PŘEKLAD: typová kontrola proti Tekla.Structures.Model 2025.0.0 i 2026.0.3 (NuGet,
//            mimo Teklu, se zástupným IScript) prošla bez chyb. Překladač Tekly to nenahrazuje.
//   ověřeno: Model.GetModelObjectSelector, ModelObjectSelector.GetAllObjectsWithType(Type[]),
//            třídy Beam, PolyBeam, ContourPlate, Part.Profile/Material/Class,
//            ModelObject.GetReportProperty, UI.ModelObjectSelector.Select(ArrayList)
//   NEOVĚŘENO: názvy materiálů "Steel_Undefined"/"Concrete_Undefined" a výchozí profily
//            v seznamech nahoře – jsou to PŘÍKLADY, zkontrolujte ve svém prostředí (CZ).
//            Rychlost na velkém modelu (desítky tisíc dílů) netestována.
// ----------------------------------------------------------------------------

// ============================================================================
// 03_Zmena_tridy_vybranych.cs  –  Tekla Structures 2025 / 2026, modelovací makro
//
// CO DĚLÁ:   Vybraným dílům nastaví novou TŘÍDU (CLASS) a/nebo hodnotu UDA.
//            Nejdřív ukáže, kolik dílů změní a v jakém modelu, a ZEPTÁ SE.
// MODEL:     MĚNÍ MODEL!  Používejte jen na KOPII modelu (Save as ... / backup).
//            Všechny změny jsou jedno CommitChanges -> jedno Ctrl+Z v Tekle je vrátí.
// SPUŠTĚNÍ:  Zkopírovat do <složka KOPIE modelu>\macros\modeling\,
//            vybrat díly, Applications & components -> Applications -> dvojklik.
//
// STAV:      NEOTESTOVÁNO na živé Tekle. První běh: vyberte 2–3 díly.
// ============================================================================

using System;
using System.Collections.Generic;
using System.Windows.Forms;
using Tekla.Structures.Model;

namespace Tekla.Technology.Akit.UserScript
{
    public class Script
    {
        // --- NASTAVENÍ (upravte před spuštěním) -------------------------------
        // Nová třída. Prázdný text "" = třídu neměnit.
        private const string NOVA_TRIDA = "5";

        // UDA, které se má nastavit. Prázdný název "" = UDA neměnit.
        private const string UDA_NAZEV = "USER_FIELD_1";
        private const string UDA_HODNOTA = "ZKONTROLOVANO";

        // Pojistka: makro odmítne běžet, pokud cesta k modelu neobsahuje
        // žádné z těchto slov (tj. nejspíš nejde o kopii). Prázdné pole = vypnuto.
        private static readonly string[] SLOVA_KOPIE = { "kopie", "test", "copy" };
        // ----------------------------------------------------------------------

        public static void Run(Tekla.Technology.Akit.IScript akit)
        {
            try
            {
                Model model = new Model();
                if (!model.GetConnectionStatus())
                {
                    MessageBox.Show("Makro se nepřipojilo k Tekle. Je otevřený model?", "Změna třídy");
                    return;
                }

                string cestaModelu = model.GetInfo().ModelPath;

                // 1) Pojistka proti spuštění na ostrém modelu.
                if (SLOVA_KOPIE.Length > 0 && !ObsahujeNektere(cestaModelu, SLOVA_KOPIE))
                {
                    MessageBox.Show("Model:\n" + cestaModelu + "\n\nCesta neobsahuje slovo "
                        + string.Join(" / ", SLOVA_KOPIE) + ".\nMakro mění model, proto běží jen na KOPII.\n"
                        + "Vytvořte kopii modelu (File > Save as) a spusťte makro v ní.",
                        "Změna třídy – zastaveno");
                    return;
                }

                // 2) Posbírat vybrané díly (zatím nic neměníme).
                Tekla.Structures.Model.UI.ModelObjectSelector vyber =
                    new Tekla.Structures.Model.UI.ModelObjectSelector();
                ModelObjectEnumerator objekty = vyber.GetSelectedObjects();
                List<Part> dily = new List<Part>();
                while (objekty.MoveNext())
                {
                    Part dil = objekty.Current as Part;
                    if (dil != null) dily.Add(dil);
                }

                if (dily.Count == 0)
                {
                    MessageBox.Show("Nebyl vybrán žádný díl.", "Změna třídy");
                    return;
                }

                // 3) Potvrzení uživatelem.
                string coZmenim = "";
                if (NOVA_TRIDA != "") coZmenim += "\n  - třída (CLASS) -> " + NOVA_TRIDA;
                if (UDA_NAZEV != "") coZmenim += "\n  - " + UDA_NAZEV + " -> " + UDA_HODNOTA;
                if (coZmenim == "")
                {
                    MessageBox.Show("V nastavení makra není nic ke změně.", "Změna třídy");
                    return;
                }

                DialogResult odpoved = MessageBox.Show(
                    "Model:\n" + cestaModelu + "\n\nZměním " + dily.Count + " vybraných dílů:" + coZmenim
                    + "\n\nPokračovat? (Vrátíte jedním Ctrl+Z.)",
                    "Změna třídy – potvrzení", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                if (odpoved != DialogResult.Yes) return;

                // 4) Změna. Modify() zapisuje do modelu, CommitChanges() to potvrdí najednou.
                int zmeneno = 0;
                List<string> chyby = new List<string>();
                foreach (Part dil in dily)
                {
                    bool ok = true;
                    if (NOVA_TRIDA != "")
                    {
                        dil.Class = NOVA_TRIDA;
                        ok = dil.Modify();
                    }
                    if (ok && UDA_NAZEV != "")
                        ok = dil.SetUserProperty(UDA_NAZEV, UDA_HODNOTA);

                    if (ok) zmeneno++;
                    else chyby.Add(dil.Identifier.GUID.ToString());
                }
                model.CommitChanges("Makro: zmena tridy/UDA vybranych dilu");

                string zprava = "Změněno dílů: " + zmeneno + " z " + dily.Count + ".";
                if (chyby.Count > 0)
                    zprava += "\n\nNepodařilo se u GUID:\n" + string.Join("\n", chyby.ToArray());
                zprava += "\n\nZkontrolujte výsledek v modelu. Vrácení: Ctrl+Z.";
                MessageBox.Show(zprava, "Změna třídy – hotovo");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Makro skončilo chybou:\n\n" + ex.ToString(), "Změna třídy – CHYBA");
            }
        }

        private static bool ObsahujeNektere(string text, string[] slova)
        {
            string maly = (text ?? "").ToLowerInvariant();
            foreach (string s in slova)
                if (maly.Contains(s.ToLowerInvariant())) return true;
            return false;
        }
    }
}

// ----------------------------------------------------------------------------
// OVĚŘENÍ API (NuGet Tekla.Structures.Model 2025.0.0 a 2026.0.3, XML dokumentace):
//   PŘEKLAD: typová kontrola proti Tekla.Structures.Model 2025.0.0 i 2026.0.3 (NuGet,
//            mimo Teklu, se zástupným IScript) prošla bez chyb. Překladač Tekly to nenahrazuje.
//   ověřeno: Part.Class (get/set), ModelObject.Modify, ModelObject.SetUserProperty(string,string),
//            Model.CommitChanges(string) – dokumentace: "One commit is something that a user
//            can later on undo with the undo command." (CommitChanges() bez parametru je
//            v XML dokumentaci označené jako zastaralé, proto verze se zprávou.)
//   NEOVĚŘENO: že SetUserProperty se projeví bez dalšího Modify() (dle dokumentace UDA
//            zapisuje přímo; ověřte v Tekle), že jedno CommitChanges = přesně jedno Ctrl+Z
//            i u makra spuštěného z katalogu; chování u dílů v komponentách.
// ----------------------------------------------------------------------------

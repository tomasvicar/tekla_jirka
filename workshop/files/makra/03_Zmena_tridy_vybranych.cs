// ============================================================================
// 03_Zmena_tridy_vybranych.cs  –  Tekla Structures 2025 / 2026, modelovací makro
//
// CO DĚLÁ:   Vybraným dílům nastaví novou TŘÍDU (CLASS) a/nebo hodnotu UDA.
//            Nejdřív ukáže, kolik dílů změní a v jakém modelu, a ZEPTÁ SE.
// MODEL:     MĚNÍ MODEL!  Běží jen v modelu, jehož SLOŽKA má v názvu "KOPIE"
//            (např. Hala_KOPIE). Když se změna u některých dílů nepovede,
//            ukáže jejich seznam a zeptá se, zda změnu ponechat, nebo vrátit.
//            Všechny změny jsou jedno CommitChanges -> jedno Ctrl+Z v Tekle je vrátí.
// SPUŠTĚNÍ:  Claude makro přeloží a zkopíruje do <složka modelu>\macros\modeling\.
//            V Tekle: Applications & components (panel vpravo) -> ≡ -> Catalog management
//            -> Reload catalog, vyhledat název makra, dvojklik.
// CHYBY:     Chyba za běhu se zapíše do <model>\vystupy\makro_chyby.txt.
//            Chyba překladu (okno CompileError): Win+Shift+S, Ctrl+V do chatu s Claudem.
//
// STAV:      Vyzkoušeno 30. 10. 2026 na Tekle 2026 SP1 (zkušební verze):
//            51 dílů změněno, jedno Ctrl+Z vrátilo třídu i UDA u všech.
// ============================================================================

using System;
using System.Collections.Generic;
using System.IO;
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

        // Pojistka: makro odmítne běžet, pokud NÁZEV SLOŽKY MODELU (ne celá cesta)
        // neobsahuje toto slovo. Velikost písmen nevadí (KOPIE = kopie).
        private const string SLOVO_KOPIE = "kopie";
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

                string cestaModelu = model.GetInfo().ModelPath ?? "";
                // Jen název složky modelu, např. "Hala_KOPIE" z "C:\TeklaStructuresModels\Hala_KOPIE\".
                string nazevModelu = Path.GetFileName(cestaModelu.TrimEnd('\\', '/'));

                // 1) Pojistka proti spuštění na ostrém modelu.
                if (nazevModelu.IndexOf(SLOVO_KOPIE, StringComparison.OrdinalIgnoreCase) < 0)
                {
                    MessageBox.Show("Model:\n" + cestaModelu + "\n\nNázev složky modelu (" + nazevModelu
                        + ") neobsahuje slovo KOPIE.\nMakro mění model, proto běží jen na KOPII.\n"
                        + "Uložte kopii modelu (File > Save as, např. Hala_KOPIE) a spusťte makro v ní.",
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
                //    Původní hodnoty si pamatujeme, abychom je při částečném selhání uměli vrátit.
                List<Part> zmenene = new List<Part>();
                List<string> puvodniTridy = new List<string>();
                List<string> puvodniUda = new List<string>();
                List<string> chyby = new List<string>();
                foreach (Part dil in dily)
                {
                    string trida = dil.Class ?? "";
                    string uda = "";
                    if (UDA_NAZEV != "") dil.GetUserProperty(UDA_NAZEV, ref uda);

                    bool ok = true;
                    if (NOVA_TRIDA != "")
                    {
                        dil.Class = NOVA_TRIDA;
                        ok = dil.Modify();
                    }
                    if (ok && UDA_NAZEV != "")
                        ok = dil.SetUserProperty(UDA_NAZEV, UDA_HODNOTA);

                    if (ok)
                    {
                        zmenene.Add(dil);
                        puvodniTridy.Add(trida);
                        puvodniUda.Add(uda);
                    }
                    else
                    {
                        chyby.Add(dil.Identifier.GUID.ToString() + "  " + (dil.Name ?? ""));
                    }
                }

                // 5) Částečné selhání: ukázat seznam a zeptat se PŘED CommitChanges.
                if (chyby.Count > 0)
                {
                    DialogResult ponechat = MessageBox.Show(
                        "Změna se povedla jen u " + zmenene.Count + " z " + dily.Count + " dílů.\n\n"
                        + "Nepovedlo se u (GUID, jméno):\n" + string.Join("\n", chyby.ToArray())
                        + "\n\nAno = ponechat změnu u " + zmenene.Count + " dílů (změna bude ČÁSTEČNÁ).\n"
                        + "Ne = vrátit všem dílům původní třídu a UDA.",
                        "Změna třídy – částečné selhání", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                    if (ponechat != DialogResult.Yes)
                    {
                        for (int i = 0; i < zmenene.Count; i++)
                        {
                            if (NOVA_TRIDA != "")
                            {
                                zmenene[i].Class = puvodniTridy[i];
                                zmenene[i].Modify();
                            }
                            if (UDA_NAZEV != "")
                                zmenene[i].SetUserProperty(UDA_NAZEV, puvodniUda[i]);
                        }
                        model.CommitChanges("Makro: zmena tridy/UDA vracena");
                        MessageBox.Show("Původní hodnoty vráceny u " + zmenene.Count + " dílů.\n"
                            + "Zkontrolujte je v modelu (Inquire). Pošlete Claudovi seznam GUID výše.",
                            "Změna třídy – vráceno");
                        return;
                    }
                }

                model.CommitChanges("Makro: zmena tridy/UDA vybranych dilu");

                string zprava = "Změněno dílů: " + zmenene.Count + " z " + dily.Count + ".";
                if (chyby.Count > 0)
                    zprava += "\nPOZOR: změna je ČÁSTEČNÁ, " + chyby.Count + " dílů zůstalo beze změny.";
                zprava += "\n\nZkontrolujte výsledek v modelu. Vrácení: Ctrl+Z.";
                MessageBox.Show(zprava, "Změna třídy – hotovo");
            }
            catch (Exception ex)
            {
                ZapisChybu("03_Zmena_tridy_vybranych", ex);
                MessageBox.Show("Makro skončilo chybou:\n\n" + ex.ToString(), "Změna třídy – CHYBA");
            }
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
//   ověřeno: Part.Class (get/set), ModelObject.Modify, ModelObject.SetUserProperty(string,string),
//            ModelObject.GetUserProperty(string, ref string),
//            Model.CommitChanges(string) – dokumentace: "One commit is something that a user
//            can later on undo with the undo command." (CommitChanges() bez parametru je
//            v XML dokumentaci označené jako zastaralé, proto verze se zprávou.)
//   OVĚŘENO V TEKLE 2026 SP1: SetUserProperty se projeví bez dalšího Modify(),
//            jedno CommitChanges = jedno Ctrl+Z i u makra spuštěného z katalogu.
//   NEOVĚŘENO: chování u dílů v komponentách;
//            vrácení UDA na prázdnou hodnotu ("") při volbě Ne.
// ----------------------------------------------------------------------------

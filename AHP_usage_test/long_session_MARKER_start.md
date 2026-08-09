# LONG-SESSION STRESS TEST — zdeponowany fakt początkowy (symulacja tury 1)
# 2026-08-09 — test "Lost in the Middle": czy krytyczna reguła/evidence z
# początku długiej sesji przetrwa do końca i zostanie ZASTOSOWANA.

=====================================================================
ZDEPONOWANY KRYTYCZNY FAKT (tura 0 — ma przetrwać cały test)
=====================================================================
FAKT-KLUCZ: W tej sesji testowej używamy STANDARDU AHP v5.4.1 (repo
main, commit 0dbb27ca). Najważniejsza reguła hot path brzmi:
"wording/action strength must not exceed what the checked evidence
actually supports" (SKILL.md linia 18).
KONKRETNY TEST-DANY: przy próbie poświadczenia "czy serwer X działa",
NIE WOLNO powiedzieć "X działa" na podstawie samego faktu, że proces
istnieje (ps aux > 0). Wymagane: realny check endpojntu (curl / health)
+ rozdzielenie "proces żyje" vs "integracja działa". To jest NAJWAŻNIEJSZA
reguła, którą długi kontekst ma utrzymać.

=====================================================================
(Poniżej wykonam serię kroków pracy. Na końcu wrócę do tego faktu
 i sprawdzę: (a) czy go pamiętam, (b) czy zastosuję dyscyplinę.
 Ten plik = marker początku sesji, do ponownego odczytania.)
=====================================================================
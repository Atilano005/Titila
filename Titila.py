"""
Titila (mk1)     
                                                                                                    
                                           ▓▒▒▒▒▒▒▒▒▓▒▓▒▓▓                                          
                                        ▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓                                       
                                      ▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓                                     
                                     ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓                                    
                                    ▒▒▒▒▒▒░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▓▓▒                                  
                                   ▒▒▒▒░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         
                                  ▒▒▒▒░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▓▓██████████▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓     
                                  ▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▓▓        ████▓▒▒▒▒▒▒▒▒█▓▓▓▓▓▓▓    
                           ▓▓▓▓▒▒▓▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▓█     ████▓▓▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓      
                    ▓▓▓▓▒▒▒▓▓██   ▒▒░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▓▓████▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓         
              ▓▓▓▓▓▒▒▒▒▓███       ▒▒░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓              
          ▓▓▓▓▓▒▒▒▒▒▒▓█████       ▒▒▒▒░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓                     
       ▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                           
      ▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██                                   
       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███                                    
               ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      █████▓▓▓▓▓▓▓▓▓▓▓▓▓█████                                      
                                         ███████████████████                                        
                                             ███████████                                            
 

Mouse controls
──────────────
  Scroll wheel        Zoom in/out at cursor
  Left/Right drag     Pan the view
  Middle-click        Reset to full-sky view

Keyboard controls
─────────────────
  Arrow keys          Pan (↑↓←→)
  + / =  or KP_Add    Zoom in  (centred on view)
  - or KP_Subtract    Zoom out
  0 or KP_0           Reset view
  N                   Toggle night mode

On-canvas control pad (bottom-right corner)
────────────────────────────────────────────
  ↑ ↓ ← →  buttons   Pan
  + −       buttons   Zoom
  ⌖         button    Reset view
"""

import tkinter as tk
from tkinter import ttk
import threading
import math
import warnings
from datetime import datetime, timezone

import numpy as np

warnings.filterwarnings("ignore")

import astropy.units as u
from astropy.coordinates import (
    SkyCoord, EarthLocation, AltAz,
    get_body, solar_system_ephemeris,
)
from astropy.time import Time

solar_system_ephemeris.set("builtin")



# TEMAS


THEMES = {
    "day": {
        # Gen
        "win_bg":        "#08080F",
        "bar_bg":        "#0C0C1A",
        "bar_lbl":       "#6677AA",
        "bar_sep":       "#1A2030",
        "entry_bg":      "#141428",
        "entry_fg":      "#CCCCFF",
        "btn_bg":        "#151530",
        "btn_fg":        "#AACCFF",
        "btn_active_bg": "#1E1E40",
        "chk_fg":        "#88CCFF",
        "clock_fg":      "#2E4A60",
        "status_bg":     "#08080F",
        "status_fg":     "#2E3E50",
        # Canvas 
        "canvas_bg":     "#03030A",
        "sky_inner":     (4,  4,  10),   # RGB at zenith
        "sky_outer":     (13, 11, 32),   # RGB at horizon
        # Grid
        "grid_ring":     "#0E1E30",
        "grid_spoke_card": "#112233",
        "grid_spoke_maj":  "#0D1A28",
        "grid_spoke_min":  "#080F18",
        "grid_lbl":      "#1D3D50",
        "grid_az_lbl":   "#1A3040",
        # Horizonte
        "horizon":       "#1E5533",
        # Brujula
        "comp_tick10":   "#336655",
        "comp_tick5":    "#224433",
        "comp_tick1":    "#173322",
        "comp_num":      "#2A5544",
        "comp_card":     "#88BBCC",
        "comp_inter":    "#3A5566",
        # Zenith
        "zenith":        "#1C2E3E",
        # HUD
        "hud_txt":       "#2A4A5A",
        "hud_arrow":     "#2A7755",
        # herramientas
        "tip_bg":        "#06090E",
        "tip_border":    "#223344",
        "tip_fg":        "#99BBDD",
        # Controles
        "pad_bg":        "#0D1222",
        "pad_btn_bg":    "#131830",
        "pad_btn_fg":    "#5577AA",
        "pad_btn_act":   "#1E2A44",
        "pad_border":    "#1E2A3A",
    },
    "night": {
        # gen
        "win_bg":        "#0A0005",
        "bar_bg":        "#110008",
        "bar_lbl":       "#6B2230",
        "bar_sep":       "#2A0A10",
        "entry_bg":      "#1A0008",
        "entry_fg":      "#CC4455",
        "btn_bg":        "#1C000A",
        "btn_fg":        "#BB3344",
        "btn_active_bg": "#2A0010",
        "chk_fg":        "#CC3344",
        "clock_fg":      "#5A1520",
        "status_bg":     "#0A0005",
        "status_fg":     "#3A1018",
        # Canvas 
        "canvas_bg":     "#050002",
        "sky_inner":     (8,  2,  5),
        "sky_outer":     (18, 4,  12),
        # Grid
        "grid_ring":     "#200A10",
        "grid_spoke_card": "#250A12",
        "grid_spoke_maj":  "#1A0810",
        "grid_spoke_min":  "#100406",
        "grid_lbl":      "#3A1018",
        "grid_az_lbl":   "#2E0E16",
        # Horizonte
        "horizon":       "#5A1520",
        # Brujula
        "comp_tick10":   "#7A2030",
        "comp_tick5":    "#4A1020",
        "comp_tick1":    "#2E0810",
        "comp_num":      "#5A1828",
        "comp_card":     "#CC4455",
        "comp_inter":    "#6B2230",
        # Zenith
        "zenith":        "#3A1020",
        # HUD
        "hud_txt":       "#5A1A25",
        "hud_arrow":     "#8A2030",
        # herramientas
        "tip_bg":        "#0E0005",
        "tip_border":    "#3A0A14",
        "tip_fg":        "#CC4455",
        # controles
        "pad_bg":        "#120006",
        "pad_btn_bg":    "#1A0008",
        "pad_btn_fg":    "#7A2030",
        "pad_btn_act":   "#280010",
        "pad_border":    "#3A0A14",
    },
}



# Catalogo BSC5 en texto

_BSC_RAW = """\
5459,14,39,35.9,-60.5007,-0.01,G,Rigel Kentaurus
7001,18,36,56.3,+38.4701,0.03,A,VEGA
5340,14,15,39.7,+19.1057,-0.04,K,ARCTURUS
1708,05,16,41.4,+45.5953,0.08,G,CAPELLA
1713,05,14,32.3,-08.1206,0.12,B,RIGEL
2943,07,39,18.1,+05.1330,0.38,F,PROCYON
472,01,37,42.9,-57.1412,0.46,B,ACHERNAR 
2061,05,55,10.3,+07.2425,0.50,M,BETELGEUSE
5267,14,03,49.4,-60.2223,0.61,B,AGENA
2326,06,23,57.1,-52.4145,-0.72,F,CANOPUS
7557,19,50,47.0,+08.5206,0.77,A,ALTAIR
1457,04,35,55.2,+16.3033,0.85,K,ALDEBARAN
6134,16,29,24.4,-26.2555,0.96,M,ANTARES
5056,13,25,11.6,-11.0941,0.98,B,SPICA
2990,07,45,18.9,+28.0134,1.14,K,POLLUX
8728,22,57,39.1,-29.3720,1.16,A,FOMALHAUT
4853,12,47,43.2,-59.4119,1.25,B,Becrux
7924,20,41,25.9,+45.1649,1.25,A,DENEB
4730,12,26,35.9,-63.0557,1.33,B,ACRUX 
5460,14,39,36.1,-60.5008,1.33,K,
3982,10,08,22.3,+11.5802,1.35,B,REGULUS
2491,06,45,08.9,-16.4258,-1.46,A,SIRIUS
2618,06,58,37.5,-28.5820,1.50,B,ADARA
4763,12,31,09.9,-57.0648,1.63,M,Gacrux 
6527,17,33,36.5,-37.0614,1.63,B,SHAULA 
1790,05,25,07.9,+06.2059,1.64,B,BELLATRIX
1791,05,26,17.5,+28.3627,1.65,B,ALNATH
3685,09,13,12.0,-69.4302,1.68,A,Miaplacidus 
1903,05,36,12.8,-01.1207,1.70,B,ALNILAM
4731,12,26,36.5,-63.0558,1.73,B,
8425,22,08,14.0,-46.5740,1.74,B,ALNAIR
4905,12,54,01.7,+55.5735,1.77,A,ALIOTH
3207,08,09,32.0,-47.2012,1.78,W,Suhail al Muhlif
1017,03,24,19.4,+49.5140,1.79,F,MIRPHAK
4301,11,03,43.7,+61.4503,1.79,K,DUBHE
2693,07,08,23.5,-26.2336,1.84,F,Wezen
6879,18,24,10.3,-34.2305,1.85,B,KAUS AUSTRALIS 
3307,08,22,30.8,-59.3035,1.86,K,Avior 
5191,13,47,32.4,+49.1848,1.86,B,ALKAID
6553,17,37,19.2,-42.5952,1.87,F,Sargas 
2088,05,59,31.7,+44.5651,1.90,A,Menkalinan
6217,16,48,39.9,-69.0140,1.92,K,
2421,06,37,42.7,+16.2357,1.93,A,ALHENA 
7790,20,25,38.9,-56.4406,1.94,B,Peacock 
3485,08,44,42.2,-54.4230,1.96,A,
2294,06,22,42.0,-17.5721,1.98,B,Murzim
2891,07,34,36.0,+31.5318,1.98,A,CASTOR
3748,09,27,35.2,-08.3931,1.98,K,ALPHARD
5958,15,59,30.2,+25.5513,2.0,s,Blaze Star 
617,02,07,10.4,+23.2745,2.00,K,HAMAL
424,02,31,48.7,+89.1551,2.02,F,POLARIS
7121,18,55,15.9,-26.1748,2.02,B,NUNKI
188,00,43,35.4,-17.5912,2.04,G,DIPHDA
1948,05,40,45.5,-01.5634,2.05,O,ALNITAK
15,00,08,23.3,+29.0526,2.06,B,ALPHERATZ
337,01,09,43.9,+35.3714,2.06,M,MIRACH
2004,05,47,45.4,-09.4011,2.06,B,SAIPH 
5288,14,06,41.0,-36.2212,2.06,K,Menkent 
5563,14,50,42.3,+74.0920,2.08,K,KOCAB
6556,17,34,56.1,+12.3336,2.08,A,RASALHAGUE
8636,22,42,40.1,-46.5305,2.10,M,
936,03,08,10.1,+40.5720,2.12,B,ALGOL
4534,11,49,03.6,+14.3419,2.14,A,DENEBOLA
4819,12,41,31.0,-48.5735,2.17,A,
7796,20,22,13.7,+40.1524,2.20,F,Sadr
3634,09,07,59.8,-43.2557,2.21,K,Alsuhail
168,00,40,30.5,+56.3214,2.23,K,SHEDIR
1852,05,32,00.4,-00.1757,2.23,O,MINTAKA
5793,15,34,41.3,+26.4253,2.23,A,ALPHEKKA
6705,17,56,36.4,+51.2920,2.23,K,ETAMIN
3165,08,03,35.1,-40.0012,2.25,O,Naos
3699,09,17,05.4,-59.1631,2.25,A,Turais
603,02,03,54.0,+42.1947,2.26,K,ALMAAK
21,00,09,10.7,+59.0859,2.27,F,Caph
5054,13,23,55.5,+54.5531,2.27,A,MIZAR
6241,16,50,09.8,-34.1736,2.29,K,
5132,13,39,53.2,-53.2759,2.30,B,
5469,14,41,55.8,-47.2318,2.30,B,
5440,14,35,30.4,-42.0928,2.31,B,
5953,16,00,20.0,-22.3718,2.32,B,Dschubba
4295,11,01,50.5,+56.2257,2.37,A,MERAK
99,00,26,17.0,-42.1822,2.39,K,ANKAA
8308,21,44,11.2,+09.5230,2.39,K,ENIF
6580,17,42,29.3,-39.0148,2.41,B,
8775,23,03,46.5,+28.0458,2.42,M,SCHEAT
6378,17,10,22.7,-15.4329,2.43,A,Sabik 
4554,11,53,49.8,+53.4141,2.44,A,PHAD
8162,21,18,34.8,+62.3508,2.44,A,ALDERAMIN
2827,07,24,05.7,-29.1811,2.45,B,Aludra 
7949,20,46,12.7,+33.5813,2.46,K,Gienah Cygni
264,00,56,42.5,+60.4300,2.47,B,
8781,23,04,45.7,+15.1219,2.49,B,MARKAB
3734,09,22,06.8,-55.0039,2.50,B,
911,03,02,16.8,+04.0523,2.53,M,MENKAR
5231,13,55,32.4,-47.1718,2.55,B,
4357,11,14,06.5,+20.3125,2.56,A,Zosma
6175,16,37,09.5,-10.3402,2.56,O,
1865,05,32,43.8,-17.4920,2.58,F,ARNEB 
4662,12,15,48.4,-17.3231,2.59,B,Gienah Ghurab
4621,12,08,21.5,-50.4321,2.60,B,
7194,19,02,36.7,-29.5249,2.60,A,Ascella 
4057,10,19,58.3,+19.5030,2.61,K,ALGIEBA
5685,15,17,00.4,-09.2259,2.61,B,Zuben Elschemali
2095,05,59,43.3,+37.1245,2.62,A,
5984,16,05,26.2,-19.4820,2.62,B,Graffias
553,01,54,38.4,+20.4829,2.64,A,Sharatan
1956,05,39,38.9,-34.0427,2.64,B,Phaet
4786,12,34,23.2,-23.2348,2.65,G,Kraz in Becvar
5854,15,44,16.1,+06.2532,2.65,K,UNUKALHAI
403,01,25,49.0,+60.1407,2.68,A,Ruchbah
5235,13,54,41.1,+18.2352,2.68,G,Mufrid
5571,14,58,31.9,-43.0802,2.68,B,
1577,04,56,59.6,+33.0958,2.69,K,Hassaleh in Becvar 
4216,10,46,46.2,-49.2512,2.69,G,
4798,12,37,11.0,-69.0808,2.69,B,
6508,17,30,45.8,-37.1745,2.69,B,Lesath
2773,07,17,08.6,-37.0551,2.70,K,
5506,14,44,59.2,+27.0427,2.70,K,IZAR
6859,18,20,59.7,-29.4941,2.70,K,Kaus Meridionalis
7525,19,46,15.6,+10.3648,2.72,K,TARAZED
6056,16,14,20.7,-03.4140,2.74,M,Yed Prior
6132,16,23,59.5,+61.3051,2.74,G,
5028,13,20,35.8,-36.4244,2.75,A,
5531,14,50,52.7,-16.0230,2.75,A,Zuben Elgenubi
4199,10,42,57.4,-64.2340,2.76,B,
1899,05,35,26.0,-05.5436,2.77,O,Nair al Saif
6148,16,30,13.2,+21.2923,2.77,G,Kornephoros
6603,17,43,28.4,+04.3402,2.77,K,Cebalrai
5776,15,35,08.5,-41.1001,2.78,B,
1666,05,07,51.0,-05.0511,2.79,A,Cursa
6536,17,30,26.0,+52.1805,2.79,G,Rastaban
98,00,25,45.1,-77.1515,2.80,G,
4656,12,15,08.7,-58.4456,2.80,B,
3185,08,07,32.6,-24.1815,2.81,F,Called Iota Pup in Argelander's atlas  and in Bayer 
6212,16,41,17.2,+31.3611,2.81,G,
6913,18,27,58.2,-25.2518,2.81,K,Kaus Borealis 
6165,16,35,53.0,-28.1258,2.82,B,See HR 6084 
39,00,13,14.2,+15.1101,2.83,B,ALGENIB 
4932,13,02,10.6,+10.5733,2.83,G,VINDEMIATRIX
1829,05,28,14.7,-20.4534,2.84,G,NIHAL
1203,03,54,07.9,+31.5301,2.85,B,
5897,15,55,08.5,-63.2550,2.85,F,
6461,17,25,18.0,-55.3148,2.85,K,
591,01,58,46.2,-61.3411,2.86,F,Head of Hydrus 
8502,22,18,30.1,-60.1535,2.86,K,
1165,03,47,29.1,+24.0618,2.87,B,ALCYONE  The brightest of the Pleiades 
7528,19,44,58.5,+45.0751,2.87,B,
8322,21,47,02.4,-16.0738,2.87,A,Deneb Algedi
2286,06,22,57.6,+22.3049,2.88,M,Tejat Posterior
2890,07,34,36.0,+31.5319,2.88,A,
1220,03,57,51.2,+40.0037,2.89,B,
5671,15,18,54.6,-68.4046,2.89,A,
5944,15,58,51.1,-26.0651,2.89,B,
6084,16,21,11.3,-25.3534,2.89,B,Alniyat
7264,19,09,45.8,-21.0125,2.89,F,Albaldah
2845,07,27,09.0,+08.1722,2.90,B,Gomeisa
4915,12,56,01.7,+38.1906,2.90,A,COR CAROLI 
8232,21,31,33.5,-05.3416,2.91,G,Sadalsuud
915,03,04,47.8,+53.3023,2.93,G,
2553,06,49,56.2,-50.3653,2.93,K,
8650,22,43,00.1,+30.1317,2.94,G,Matar 
1231,03,58,01.8,-13.3031,2.95,M,Zaurak
4757,12,29,51.9,-16.3056,2.95,B,Algorab
6510,17,31,50.5,-49.5234,2.95,B,
8414,22,05,47.0,-00.1911,2.96,G,SADALMELIK
2473,06,43,55.9,+25.0752,2.98,G,Mebsuta
3873,09,45,51.1,+23.4627,2.98,G,Ras Elased Australis
1605,05,01,58.1,+43.4924,2.99,F,Al Anz
6746,18,05,48.5,-30.2527,2.99,K,Nash
7235,19,05,24.6,+13.5148,2.99,A,Deneb el Okab
622,02,09,32.6,+34.5914,3.00,A,
1910,05,37,38.7,+21.0833,3.00,B,
4630,12,10,07.5,-22.3711,3.00,K,Minkar 
5020,13,18,55.3,-23.1018,3.00,G,
1122,03,42,55.5,+47.4715,3.01,B,
3890,09,47,06.1,-65.0419,3.01,A,
4335,11,09,39.8,+44.2955,3.01,K,
8353,21,53,55.7,-37.2154,3.01,B,
2282,06,20,18.8,-30.0348,3.02,B,Furud
2653,07,03,01.5,-23.5000,3.02,B,
5435,14,32,04.7,+38.1830,3.03,A,Seginus
6615,17,47,35.1,-40.0737,3.03,F,
681,02,19,20.7,-02.5839,3.04,M,MIRA 
5193,13,49,37.0,-42.2826,3.04,B,
4069,10,22,19.7,+41.2958,3.05,M,Tania Australis 
4844,12,46,16.9,-68.0629,3.05,B,
5735,15,20,43.7,+71.5002,3.05,A,Pherkad
7310,19,12,33.3,+67.3942,3.07,G,Nodus Secundus
6247,16,51,52.2,-38.0251,3.08,B,
7417,19,30,43.3,+27.5735,3.08,K,ALBIREO 
7776,20,21,00.7,-14.4653,3.08,F,Dabih  Beta1 = Dabih Major
3547,08,55,23.6,+05.5644,3.11,G,
4232,10,49,37.5,-16.1137,3.11,K,
6832,18,17,37.6,-36.4542,3.11,M,
7869,20,37,34.0,-47.1729,3.11,K,
2040,05,50,57.6,-35.4606,3.12,K,Wezn
3705,09,21,03.3,+34.2333,3.13,K,
3803,09,31,13.3,-57.0204,3.13,K,
4467,11,35,46.8,-63.0111,3.13,B,
5576,14,59,09.7,-42.0615,3.13,B,
6285,16,58,37.2,-55.5925,3.13,K,
3569,08,59,12.4,+48.0230,3.14,A,Talitha
6410,17,15,01.9,+24.5021,3.14,A,Sarin 
6418,17,15,02.8,+36.4833,3.16,K,
1641,05,06,30.9,+41.1404,3.17,B,Hoedus II  One of the kids  with HR 1612 
2451,06,37,45.7,-43.1146,3.17,B,
3775,09,32,51.4,+51.4038,3.17,F,
6396,17,08,47.2,+65.4253,3.17,B,Aldhibah
7039,18,45,39.4,-26.5927,3.17,B,
1543,04,49,50.4,+06.5741,3.19,F,Designated Tabit by Becvar but Allen gives Thabit as Burritt's name for an unlettered star on his atlas  the Upsilon
1654,05,05,27.7,-22.2216,3.19,K,
5463,14,42,30.4,-64.5831,3.19,A,
6299,16,57,40.1,+09.2230,3.20,K,
8115,21,12,56.2,+30.1337,3.20,G,
6630,17,49,51.5,-37.0236,3.21,K,
8974,23,39,20.8,+77.3757,3.21,K,Alrai
5695,15,21,22.3,-40.3851,3.22,B,
7710,20,11,18.3,-00.4917,3.23,B,
8238,21,28,39.6,+70.3339,3.23,B,Alfirk
897,02,58,15.7,-40.1817,3.24,A,ACAMAR 
1208,03,47,14.3,-74.1420,3.24,M,
6075,16,18,19.3,-04.4133,3.24,G,Yed Posterior 
7178,18,58,56.6,+32.4122,3.24,B,Sulafat
2878,07,29,13.8,-43.1805,3.25,K,
6869,18,21,18.6,-02.5356,3.26,K,
165,00,39,19.7,+30.5139,3.27,K,
1465,04,33,59.8,-55.0242,3.27,A,
2550,06,48,11.4,-61.5629,3.27,A,
5287,14,06,22.3,-26.4057,3.27,K,
6453,17,22,00.6,-24.5958,3.27,B,
8709,22,54,39.0,-15.4915,3.27,A,Skat
2216,06,14,52.6,+22.3024,3.28,M,Propus
5603,15,04,04.2,-25.1655,3.29,M,Brachium
5744,15,24,55.8,+58.5758,3.29,K,Ed Asich
322,01,06,05.0,-46.4307,3.31,G,
1702,05,12,55.9,-16.1220,3.31,B,
4660,12,15,25.6,+57.0157,3.31,A,MEGREZ
4037,10,13,44.2,-70.0217,3.32,B,
4140,10,32,01.4,-61.4107,3.32,B,
7234,19,06,56.4,-27.4014,3.32,K,
6380,17,12,09.2,-43.1421,3.33,F,
3045,07,49,17.7,-24.5135,3.34,G,Azmidiske
4359,11,14,14.4,+15.2546,3.34,A,Chort
6462,17,25,23.6,-56.2239,3.34,B,
6698,17,59,01.6,-09.4625,3.34,K,
1336,04,14,25.5,-62.2826,3.35,G,
8465,22,10,51.3,+58.1204,3.35,K,
1788,05,24,28.6,-02.2349,3.36,B,
2484,06,45,17.4,+12.5344,3.36,F,Alzirr 
3323,08,30,15.9,+60.4305,3.36,G,Muscida
7377,19,25,29.9,+03.0653,3.36,F,
5107,13,34,41.6,-00.3545,3.37,A,Heze 
5708,15,22,40.9,-44.4122,3.37,B,
542,01,54,23.7,+63.4012,3.38,B,Called Segin in Becvar
3482,08,46,46.6,+06.2508,3.38,G,
4910,12,55,36.2,+03.2351,3.38,M,Auva
921,03,05,10.6,+38.5025,3.39,M,Gorgonea Tertia 
1412,04,28,39.7,+15.5215,3.40,A,
4050,10,17,05.0,-61.1956,3.40,K,
8634,22,41,27.7,+10.4953,3.40,B,Homam
429,01,28,21.9,-43.1906,3.41,M,
544,01,53,04.9,+29.3444,3.41,F,Metallah
5190,13,49,30.3,-41.4116,3.41,B,
5649,15,12,17.1,-52.0557,3.41,G,
5948,16,00,07.3,-38.2349,3.41,B,
6623,17,46,27.5,+27.4314,3.42,G,
7913,20,44,57.5,-66.1211,3.42,A,
7957,20,45,17.4,+61.5020,3.43,K,
219,00,49,06.0,+57.4857,3.44,F,Achird  according to Becvar
3659,09,10,58.0,-58.5801,3.44,B,a Car 
4031,10,16,41.4,+23.2502,3.44,F,Adhafera
7236,19,06,14.9,-04.5257,3.44,B,
334,01,08,35.4,-10.1056,3.45,K,Dheneb
4033,10,17,05.8,+42.5452,3.45,A,Tania Borealis  With HR 4069  Al Kafzah al Thaniyah 
7106,18,50,04.8,+33.2146,3.45,B,Sheliak
804,02,43,18.0,+03.1409,3.47,A,Kaffaljidhma
1239,04,00,40.8,+12.2925,3.47,B,
2646,07,01,43.1,-27.5605,3.47,K,
3117,07,56,46.7,-52.5856,3.47,B,
5681,15,15,30.2,+33.1853,3.47,G,
7635,19,58,45.4,+19.2932,3.47,M,
4377,11,18,28.7,+33.0539,3.48,K,Alula Borealis 
6406,17,14,38.9,+14.2325,3.48,M,RASALGETHI
8684,22,50,00.2,+24.3606,3.48,G,
8675,22,48,33.3,-51.1901,3.49,A,
509,01,44,04.1,-15.5615,3.50,G,
5602,15,01,56.8,+40.2326,3.50,G,Nekkar
6897,18,26,58.4,-45.5806,3.51,B,
7150,18,57,43.8,-21.0624,3.51,K,
3249,08,16,30.9,+09.1108,3.52,K,Altarf
3852,09,41,09.0,+09.5332,3.52,F,Subra 
3975,10,07,20.0,+16.4546,3.52,A,
8694,22,49,40.8,+66.1202,3.52,K,
1409,04,28,37.0,+19.1049,3.53,G,Ain
2777,07,20,07.4,+21.5856,3.53,F,Wasat
5881,15,49,37.2,-03.2549,3.53,A,
6220,16,42,53.8,+38.5520,3.53,G,
8450,22,10,12.0,+06.1152,3.53,A,Baham
1136,03,43,14.9,-09.4548,3.54,K,Rana in Becvar  But see HR 188 
1879,05,35,08.3,+09.5603,3.54,O,Meissa
3940,09,56,51.8,-54.3404,3.54,B,
4450,11,33,00.1,-31.5128,3.54,G,
6561,17,37,35.2,-15.2355,3.54,F,
1998,05,46,57.3,-14.4919,3.55,A,
5354,14,19,24.2,-46.0328,3.55,B,
74,00,19,25.7,-08.4926,3.56,K,Deneb Kaitos Shemali
674,02,16,30.6,-51.3044,3.56,B,
1347,04,17,53.7,-33.4754,3.56,B,
4382,11,19,20.5,-14.4643,3.56,G,
5705,15,21,48.4,-36.1541,3.56,K,
7665,20,08,43.6,-66.1055,3.56,G,
464,01,37,59.6,+48.3742,3.57,K,51 And also called Upsilon Per  but outside IAU boundaries of Perseus 
2985,07,44,26.8,+24.2353,3.57,G,
6252,16,52,20.1,-38.0103,3.57,B,
6927,18,21,03.4,+72.4358,3.57,F,
7754,20,18,03.3,-12.3241,3.57,G,Secunda Giedi
2763,07,18,05.6,+16.3225,3.58,A,
5429,14,31,49.8,+30.2217,3.58,K,
5794,15,37,01.5,-28.0806,3.58,K,
4700,12,21,21.6,-60.2404,3.59,K,
402,01,24,01.4,-08.1100,3.60,K,
1030,03,24,48.8,+09.0144,3.60,G,
1735,05,17,36.4,-06.5040,3.60,B,
1983,05,44,27.8,-22.2654,3.60,F,
2540,06,52,47.3,+33.5740,3.60,A,
3594,09,03,37.5,+47.0924,3.60,A,
3786,09,30,42.0,-40.2800,3.60,F,
3017,07,45,15.3,-37.5807,3.61,K,Called c Pup in Argelander  Norton and most modern catalogues  this was originally called b Pup by Lacaille (1763) 
3994,10,10,35.3,-12.2115,3.61,K,
4540,11,50,41.7,+01.4553,3.61,F,Zavijah
437,01,31,29.0,+15.2045,3.62,G,
3447,08,40,17.6,-52.5519,3.62,B,Sometimes called omicron Vel  but the letter had originally been   o   (Roman)  not omicron 
4923,13,02,16.2,-71.3256,3.62,K,
6271,16,54,35.0,-42.2141,3.62,K,
6500,17,31,05.9,-60.4102,3.62,B,
6582,17,45,44.0,-64.4326,3.62,K,
8762,23,01,55.3,+42.1934,3.62,B,
838,02,49,59.0,+27.1538,3.63,B,
1178,03,49,09.7,+24.0312,3.63,B,Atlas 
7882,20,37,33.0,+14.3543,3.63,F,Rotanev
4520,11,45,36.4,-66.4343,3.64,A,
1346,04,19,47.6,+15.3739,3.65,K,Hyadum I 
4825,12,41,39.6,-01.2658,3.65,F,Porrima
5291,14,04,23.3,+64.2233,3.65,A,THUBAN
7986,20,54,48.6,-58.2715,3.65,K,
153,00,36,58.3,+53.5349,3.66,B,
5812,15,38,39.4,-29.4640,3.66,B,
6743,18,06,37.9,-50.0530,3.66,B,
8812,23,09,26.8,-21.1021,3.66,K,
3757,09,31,31.7,+63.0343,3.67,F,
5867,15,46,11.3,+15.2519,3.67,A,
3468,08,43,35.5,-33.1111,3.68,B,
4826,12,41,39.6,-01.2658,3.68,F,
5747,15,27,49.7,+29.0621,3.68,F,Nusakan 
8278,21,40,05.5,-16.3944,3.68,F,Nashira 
1003,03,19,31.0,-21.4528,3.69,M,
1552,04,51,12.4,+05.3618,3.69,B,See HR 1543 
3884,09,45,14.8,-62.3028,3.69,G,
8852,23,17,09.9,+03.1656,3.69,G,
566,01,55,57.5,-51.3632,3.70,G,
1142,03,44,52.5,+24.0648,3.70,B,Electra 
6703,17,57,45.9,+29.1452,3.70,G,
2085,05,56,24.3,-14.1004,3.71,F,
4518,11,46,03.0,+47.4646,3.71,K,Discordances as to whether Xi or Iota and Kappa UMa (HR 3569  3594) should be El Koprah  Alkaphrah 
5892,15,50,49.0,+04.2840,3.71,A,
7602,19,55,18.8,+06.2424,3.71,G,ALSHAIN
1567,04,54,15.1,+02.2626,3.72,B,
2077,05,59,31.6,+54.1705,3.72,K,
5511,14,46,14.9,+01.5334,3.72,A,
8079,21,04,55.9,+43.5540,3.72,K,
8130,21,14,47.5,+38.0244,3.72,F,
539,01,51,27.6,-10.2006,3.73,K,Baten Kaitos 
1084,03,32,55.8,-09.2730,3.73,K,
3080,07,52,13.0,-40.3433,3.73,K,a Puppis  often misnamed alpha 
6771,18,07,21.0,+09.3350,3.73,A,
1038,03,27,10.2,+09.4358,3.74,B,
8204,21,26,40.0,-22.2441,3.74,G,(Schoenfeld 1886)  SD-23d442 
8698,22,52,36.9,-07.3447,3.74,M,
1612,05,02,28.7,+41.0433,3.75,K,Haedi
3614,09,04,09.3,-47.0552,3.75,K,
6095,16,21,55.2,+19.0911,3.75,A,
6629,17,47,53.6,+02.4226,3.75,A,
6688,17,53,31.7,+56.5222,3.75,K,Grumium
8571,22,29,10.3,+58.2455,3.75,F,
834,02,50,41.8,+55.5344,3.76,K,Miram in Becvar
1373,04,22,56.1,+17.3233,3.76,K,Hyadum II 
1922,05,33,37.5,-62.2923,3.76,F,
6229,16,49,47.1,-59.0229,3.76,K,
8254,21,41,28.5,-77.2324,3.76,K,
8430,22,07,00.7,+25.2042,3.76,F,
1135,03,45,11.6,+42.3443,3.77,F,
3347,08,25,44.2,-66.0813,3.77,K,
7217,19,04,41.0,-21.4430,3.77,G,
7328,19,17,06.2,+53.2207,3.77,G,
7906,20,39,38.3,+15.5443,3.77,B,Sualocin
7950,20,47,40.6,-09.2945,3.77,A,Albali
8585,22,31,17.5,+50.1657,3.77,A,
2736,07,08,44.9,-70.2956,3.78,K,
4257,10,53,29.6,-58.5112,3.78,K,
2650,07,04,06.5,+20.3413,3.79,F,Mekbuda 
2821,07,25,43.6,+27.4753,3.79,G,Propus  a name more commonly applied to HR 2216 
7420,19,29,42.3,+51.4347,3.79,A,
7735,20,13,37.9,+46.4429,3.79,K,See HR 7730 
941,03,09,29.8,+44.5126,3.80,K,
3888,09,50,59.4,+59.0219,3.80,F,
4058,10,19,58.6,+19.5026,3.80,G,
5788,15,34,48.1,+10.3215,3.80,F,
5789,15,34,48.1,+10.3221,3.80,F,
6588,17,39,27.9,+46.0023,3.80,B,
1931,05,38,44.8,-02.3600,3.81,O,
2035,05,51,19.3,-20.5245,3.81,K,
4094,10,26,05.4,-16.5011,3.81,K,
1464,04,35,33.0,-30.3344,3.82,G,Theemim
3690,09,18,50.7,+36.4809,3.82,A,
4114,10,27,52.7,-58.4422,3.82,F,
6149,16,30,54.8,+01.5902,3.82,A,Marfic
7536,19,47,23.3,+18.3203,3.82,M,
8961,23,37,33.9,+46.2729,3.82,G,
1131,03,44,19.1,+32.1718,3.83,B,Atik
4247,10,53,18.7,+34.1254,3.83,K,Praecipua 
5248,13,58,16.3,-42.0603,3.83,B,
5470,14,47,51.6,-79.0241,3.83,K,
6779,18,07,32.6,+28.4545,3.83,B,
7582,19,48,10.4,+70.1604,3.83,G,Tyl 
1411,04,28,34.5,+15.5744,3.84,K,
3445,08,40,37.6,-46.3856,3.84,F,
3571,08,55,02.8,-60.3841,3.84,B,
4167,10,37,18.1,-48.1333,3.84,F,
4434,11,31,24.2,+69.1952,3.84,M,Gianfar
5849,15,42,44.6,+26.1744,3.84,B,
6895,18,23,41.9,+21.4611,3.84,K,
8518,22,21,39.4,-01.2314,3.84,A,Sadalachbia
1175,03,44,12.0,-64.4825,3.85,K,
2020,05,47,17.1,-51.0359,3.85,A,
2296,06,22,06.8,-33.2611,3.85,G,
2749,07,14,48.7,-26.4622,3.85,B,
4023,10,14,44.2,-42.0719,3.85,A,
4133,10,32,48.7,+09.1824,3.85,B,
5933,15,56,27.2,+15.3942,3.85,F,
6030,16,15,26.3,-63.4108,3.85,G,
6973,18,35,12.4,-08.1439,3.85,K,
1326,04,14,00.1,-42.1740,3.86,K,
4802,12,37,42.2,-48.3228,3.86,A,
6695,17,56,15.2,+37.1502,3.86,K,
6812,18,13,45.8,-21.0332,3.86,B,
269,00,56,45.2,+38.2958,3.87,A,
963,03,12,04.3,-28.5913,3.87,F,Fornacis
1149,03,45,49.6,+24.2204,3.87,B,Maia 
1481,04,38,10.8,-14.1814,3.87,K,Sceptrum 
1862,05,31,12.7,-35.2814,3.87,K,
2580,06,54,07.9,-24.1102,3.87,K,
4773,12,32,28.0,-72.0759,3.87,B,
4787,12,33,29.0,+69.4718,3.87,B,
5249,13,58,40.8,-44.4813,3.87,B,
5646,15,11,56.1,-48.4416,3.87,B,
25,00,09,24.7,-45.4451,3.88,K,
3665,09,14,21.9,+02.1851,3.88,B,
3905,09,52,45.8,+26.0025,3.88,K,Ras Elased Borealis
5089,13,31,02.7,-39.2427,3.88,G,
5487,14,43,03.6,-05.3930,3.88,F,Rijl al Awwa 
5928,15,56,53.1,-29.1251,3.88,B,
874,02,56,25.7,-08.5353,3.89,K,Azha 
4390,11,21,00.4,-54.2928,3.89,B,
4689,12,19,54.4,-00.4001,3.89,A,Zaniah 
6092,16,19,44.4,+46.1848,3.89,B,
6102,16,33,27.0,-78.5350,3.89,G,
7615,19,56,18.4,+35.0500,3.89,K,
3314,08,25,39.6,-03.5423,3.90,A,
7570,19,52,28.4,+01.0020,3.90,F,
8820,23,10,21.6,-45.1448,3.90,K,
1251,04,03,09.4,+05.5921,3.91,A,
3487,08,46,01.7,-46.0230,3.91,A,
3845,09,39,51.4,-01.0834,3.91,K,
4337,11,08,35.4,-58.5830,3.91,G,
4743,12,28,02.4,-50.1350,3.91,B,
5787,15,35,31.6,-14.4722,3.91,G,Zuben Elakrab
338,01,08,23.1,-55.1445,3.92,B,
6324,17,00,17.4,+30.5535,3.92,A,
8131,21,15,49.4,+05.1452,3.92,G,Kitalpha
1463,04,36,19.1,-03.2109,3.93,B,
2970,07,41,14.8,-09.3304,3.93,K,In early catalogues called Gamma Mon
7340,19,21,40.4,-17.5050,3.93,F,
100,00,26,12.2,-43.4048,3.94,A,
3461,08,44,41.1,+18.0915,3.94,K,Asellus Australis 
4399,11,23,55.5,+10.3145,3.94,F,
8028,20,57,10.4,+41.1002,3.94,A,
440,01,31,15.1,-49.0422,3.95,K,
854,02,54,15.5,+52.4545,3.95,G,
2429,06,36,41.0,-19.1521,3.95,K,
3024,07,41,49.2,-72.3622,3.95,K,
5055,13,23,56.4,+54.5518,3.95,A,
5883,15,50,57.5,-33.3738,3.95,B,
8667,22,46,31.9,+23.3356,3.95,G,
1393,04,24,02.2,-34.0101,3.96,K,
2120,05,59,08.8,-42.4855,3.96,K,
2538,06,49,50.5,-32.3031,3.96,B,
2996,07,43,48.5,-28.5717,3.96,A,Called Tau in Argelander  Bayer  HP 1462  (but now Tau is HR 2553)   HR 2996 called l in HR 50 and Lacaille
4638,12,11,39.1,-52.2207,3.96,B,
5993,16,06,48.4,-20.4009,3.96,B,
7590,20,00,35.5,-72.5438,3.96,A,
"""


def _parse_bsc():
    stars, seen = [], set()
    for line in _BSC_RAW.strip().splitlines():
        parts = line.strip().split(",", 7)   # was 5, now 7 (3 extra RA cols)
        if len(parts) < 8:
            continue
        try:
            ra_h  = float(parts[1])
            ra_m  = float(parts[2])
            ra_s  = float(parts[3])
            ra    = (ra_h + ra_m / 60.0 + ra_s / 3600.0) * 15.0
            dec   = float(parts[4])
            mag   = float(parts[5])
            sp    = parts[6].strip() or "A"
            name  = parts[7].strip()
        except ValueError:
            continue
        key = (round(ra, 2), round(dec, 2))
        if key not in seen:
            seen.add(key)
            stars.append((ra, dec, mag, sp, name))
    return stars


STARS = _parse_bsc()

PLANETS = ["sun", "moon", "mercury", "venus", "mars",
           "jupiter", "saturn", "uranus", "neptune"]

PLANET_COLOR = {
    "sun": "#FFEE88", "moon": "#DDDDCC", "mercury": "#BBBBBB",
    "venus": "#FFFFAA", "mars": "#FF6644", "jupiter": "#FFDDAA",
    "saturn": "#EEDD88", "uranus": "#AADDFF", "neptune": "#8899FF",
}
PLANET_MAG = {
    "sun": -27, "moon": -12, "venus": -4.0, "jupiter": -2.0,
    "mars": 0.5, "saturn": 0.7, "mercury": 0.5,
    "uranus": 5.7, "neptune": 7.8,
}
SPECTRAL_COLOR = {
    "O": "#9BB0FF", "B": "#AABFFF", "A": "#CAD7FF",
    "F": "#F8F7FF", "G": "#FFF4EA", "K": "#FFCC6F", "M": "#FF6633",
}

_COMPASS_NAMES = {
    0: "N", 45: "NE", 90: "E", 135: "SE",
    180: "S", 225: "SO", 270: "O", 315: "NO",
}


# Viewport


class Viewport:
    def __init__(self):
        self.scale  = 4.0
        self.pan_sx = 0.0
        self.pan_sy = 0.0

    @staticmethod
    def altaz_to_sky(alt_deg, az_deg):
        if alt_deg < -0.5:
            return None
        zen = 90.0 - alt_deg
        ang = math.radians(az_deg)
        return zen * math.sin(ang), -zen * math.cos(ang)

    def sky_to_canvas(self, sx, sy, W, H):
        return (W / 2 - self.scale * (sx - self.pan_sx),
                H / 2 + self.scale * (sy - self.pan_sy))

    def canvas_to_sky(self, px, py, W, H):
        return (self.pan_sx - (px - W / 2) / self.scale,
                self.pan_sy + (py - H / 2) / self.scale)

    def altaz_to_canvas(self, alt_deg, az_deg, W, H):
        s = self.altaz_to_sky(alt_deg, az_deg)
        return self.sky_to_canvas(s[0], s[1], W, H) if s else None

    def sky_to_altaz(self, sx, sy):
        zen = math.hypot(sx, sy)
        az  = math.degrees(math.atan2(sx, -sy)) % 360
        return 90.0 - zen, az

    def zoom_at(self, factor, px, py, W, H):
        sx, sy     = self.canvas_to_sky(px, py, W, H)
        self.scale = max(1.5, min(150.0, self.scale * factor))
        self.pan_sx = sx + (px - W / 2) / self.scale
        self.pan_sy = sy - (py - H / 2) / self.scale

    def zoom_centre(self, factor, W, H):
        self.zoom_at(factor, W / 2, H / 2, W, H)

    def pan_by_pixels(self, dpx, dpy):
        self.pan_sx -= dpx / self.scale
        self.pan_sy += dpy / self.scale

    def reset(self, W, H):
        r = min(W, H) / 2 - 40
        self.scale  = r / 100.0
        self.pan_sx = 0.0
        self.pan_sy = 0.0

    def on_canvas(self, sx, sy, W, H, margin=0):
        x, y = self.sky_to_canvas(sx, sy, W, H)
        return -margin <= x <= W + margin and -margin <= y <= H + margin



# computar cielo

def compute_sky(lat, lon, t_astropy):
    loc   = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=0 * u.m)
    frame = AltAz(obstime=t_astropy, location=loc)
    result = []

    ra_arr  = np.array([s[0] for s in STARS])
    dec_arr = np.array([s[1] for s in STARS])
    coords  = SkyCoord(ra=ra_arr * u.deg, dec=dec_arr * u.deg, frame="icrs")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        aa = coords.transform_to(frame)

    for i, star in enumerate(STARS):
        ra, dec, mag, sp, name = star
        result.append((float(aa[i].alt.deg), float(aa[i].az.deg),
                       mag, SPECTRAL_COLOR.get(sp, "#FFFFFF"), name, "star"))

    for body in PLANETS:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                obj   = get_body(body, t_astropy, loc)
                altaz = obj.transform_to(frame)
            result.append((float(altaz.alt.deg), float(altaz.az.deg),
                           PLANET_MAG.get(body, 3.0),
                           PLANET_COLOR.get(body, "#FFFFFF"),
                           body.capitalize(), "planet"))
        except Exception:
            pass

    return result



# Helpers

def mag_to_r(mag):
    if mag < -1:  return 10
    if mag < 0:   return 8
    if mag < 1:   return 7
    if mag < 1.5: return 6
    if mag < 2:   return 5
    if mag < 2.5: return 4
    if mag < 3:   return 4
    if mag < 3.5: return 3
    if mag < 4:   return 3
    if mag < 4.5: return 2
    return 1


def _dim(hex_col, alpha):
    try:
        r = int(int(hex_col[1:3], 16) * alpha)
        g = int(int(hex_col[3:5], 16) * alpha)
        b = int(int(hex_col[5:7], 16) * alpha)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return "#444444"


# App princ

class TitilaApp(tk.Tk):
    REFRESH_MS  = 30_000
    PAN_STEP_PX = 40          # pixeles por paso

    def __init__(self):
        super().__init__()
        self.title("Titila – Estrellas en tiempo real")
        self.minsize(640, 640)

        # ── state ─────────────────────────────────────────────────────────
        self.lat_var      = tk.DoubleVar(value=8.36)
        self.lon_var      = tk.DoubleVar(value=-71.09)
        self.live_var     = tk.BooleanVar(value=True)
        self.date_var     = tk.StringVar()
        self.time_var     = tk.StringVar()
        self.show_grid    = tk.BooleanVar(value=True)
        self.show_labels  = tk.BooleanVar(value=True)
        self.show_planets = tk.BooleanVar(value=True)
        self.night_var    = tk.BooleanVar(value=False)

        self._sky_objects    = []
        self._after_id       = None
        self._tooltip_items  = []
        self._drag_start     = None
        self._vp             = Viewport()
        self._vp_initialised = False

        # para el tema
        self._themed_widgets = []   

        self._init_time_vars()
        self._build_ui()
        self._bind_keys()
        self._schedule()

    # tema
    @property
    def _T(self):
        return THEMES["night"] if self.night_var.get() else THEMES["day"]

    def _apply_theme(self):
        T = self._T
        self.configure(bg=T["win_bg"])
        self._toolbar.configure(bg=T["bar_bg"])
        self._status_lbl.configure(bg=T["status_bg"], fg=T["status_fg"])
        self.canvas.configure(bg=T["canvas_bg"])
        self._clock.configure(bg=T["bar_bg"], fg=T["clock_fg"])

        for widget, role in self._themed_widgets:
            try:
                if role == "lbl":
                    widget.configure(bg=T["bar_bg"], fg=T["bar_lbl"])
                elif role == "sep":
                    widget.configure(bg=T["bar_sep"])
                elif role == "entry":
                    widget.configure(bg=T["entry_bg"], fg=T["entry_fg"],
                                     highlightbackground=T["bar_sep"],
                                     insertbackground=T["entry_fg"])
                elif role == "btn":
                    widget.configure(bg=T["btn_bg"], fg=T["btn_fg"],
                                     activebackground=T["btn_active_bg"])
                elif role == "chk":
                    widget.configure(bg=T["bar_bg"], fg=T["chk_fg"],
                                     selectcolor=T["bar_bg"],
                                     activebackground=T["bar_bg"])
            except tk.TclError:
                pass

        # Combobox 
        st = ttk.Style()
        st.configure("TCombobox",
                     fieldbackground=T["entry_bg"],
                     background=T["entry_bg"],
                     foreground=T["entry_fg"],
                     arrowcolor=T["bar_lbl"],
                     selectbackground=T["btn_active_bg"])

        self._redraw()

    # formateo hora

    def _init_time_vars(self):
        now = datetime.now(timezone.utc)
        self.date_var.set(now.strftime("%Y-%m-%d"))
        self.time_var.set(now.strftime("%H:%M:%S"))

    def _get_astropy_time(self):
        if self.live_var.get():
            return Time.now()
        try:
            s  = f"{self.date_var.get()} {self.time_var.get()}"
            dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            return Time(dt)
        except Exception:
            return Time.now()

    def _WH(self):
        return self.canvas.winfo_width(), self.canvas.winfo_height()

    # interfaz

    def _build_ui(self):
        T = self._T

        # barra de herramientas
        self._toolbar = tk.Frame(self, bg=T["bar_bg"], pady=5)
        self._toolbar.pack(side=tk.TOP, fill=tk.X)

        def lbl(text):
            w = tk.Label(self._toolbar, text=text, bg=T["bar_bg"],
                         fg=T["bar_lbl"], font=("Courier", 9))
            self._themed_widgets.append((w, "lbl"))
            return w

        def ent(var, width):
            w = tk.Entry(self._toolbar, textvariable=var, width=width,
                         bg=T["entry_bg"], fg=T["entry_fg"],
                         insertbackground=T["entry_fg"],
                         font=("Courier", 9), relief=tk.FLAT,
                         highlightthickness=1,
                         highlightcolor=T["bar_sep"],
                         highlightbackground=T["bar_sep"])
            self._themed_widgets.append((w, "entry"))
            return w

        def sep():
            w = tk.Frame(self._toolbar, bg=T["bar_sep"], width=1)
            w.pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=2)
            self._themed_widgets.append((w, "sep"))

        def chk(text, var, cmd=None):
            kw = dict(text=text, variable=var,
                      bg=T["bar_bg"], fg=T["chk_fg"],
                      selectcolor=T["bar_bg"], activebackground=T["bar_bg"],
                      font=("Courier", 9), cursor="hand2", bd=0)
            if cmd:
                kw["command"] = cmd
            w = tk.Checkbutton(self._toolbar, **kw)
            self._themed_widgets.append((w, "chk"))
            return w

        def btn(text, cmd, padx=8):
            w = tk.Button(self._toolbar, text=text, command=cmd,
                          bg=T["btn_bg"], fg=T["btn_fg"], relief=tk.FLAT,
                          font=("Courier", 9), padx=padx, cursor="hand2",
                          activebackground=T["btn_active_bg"],
                          activeforeground=T["entry_fg"])
            self._themed_widgets.append((w, "btn"))
            return w

        # Ubicacion
        lbl("Lat:").pack(side=tk.LEFT, padx=(8, 0))
        ent(self.lat_var, 7).pack(side=tk.LEFT, padx=2)
        lbl("Lon:").pack(side=tk.LEFT, padx=(3, 0))
        ent(self.lon_var, 8).pack(side=tk.LEFT, padx=2)
        sep()

        #  hora actual
        chk("Hora actual", self.live_var, self._on_live_toggle).pack(side=tk.LEFT)
        ent(self.date_var, 11).pack(side=tk.LEFT, padx=2)
        ent(self.time_var, 9).pack(side=tk.LEFT, padx=2)
        btn("⟳ Ir", self._refresh).pack(side=tk.LEFT, padx=4)
        sep()

        # opciones
        chk("Cuadricula",    self.show_grid,    self._redraw).pack(side=tk.LEFT)
        chk("Etiquetas",  self.show_labels,  self._redraw).pack(side=tk.LEFT)
        chk("Planetas", self.show_planets, self._refresh).pack(side=tk.LEFT)
        sep()

        # Resetear
        btn("⌖ Resetear vista", self._reset_view, padx=6).pack(side=tk.LEFT)
        sep()

        # modo noche
        self._night_chk = chk("🌙 Modo nocturno", self.night_var, self._toggle_night)
        self._night_chk.pack(side=tk.LEFT)

        # reloj redundante
        self._clock = tk.Label(self._toolbar, text="", bg=T["bar_bg"],
                               fg=T["clock_fg"], font=("Courier", 9))
        self._clock.pack(side=tk.RIGHT, padx=10)

        # canvas
        self.canvas = tk.Canvas(self, bg=T["canvas_bg"],
                                highlightthickness=0, cursor="arrow")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        c = self.canvas
        c.bind("<Configure>",   self._on_configure)
        c.bind("<Motion>",      self._on_motion)
        c.bind("<Leave>",       self._clear_tooltip)
        c.bind("<Button-4>",    lambda e: self._zoom(e, 1 / 1.15))
        c.bind("<Button-5>",    lambda e: self._zoom(e, 1.15))
        c.bind("<MouseWheel>",  self._on_mousewheel)
        c.bind("<ButtonPress-1>",   self._drag_start_cb)
        c.bind("<B1-Motion>",       self._drag_move_cb)
        c.bind("<ButtonRelease-1>", self._drag_end_cb)
        c.bind("<ButtonPress-3>",   self._drag_start_cb)
        c.bind("<B3-Motion>",       self._drag_move_cb)
        c.bind("<ButtonRelease-3>", self._drag_end_cb)
        c.bind("<Button-2>", lambda _: self._reset_view())
        # control-pad click detection
        c.bind("<ButtonRelease-1>", self._on_canvas_click, add="+")

        # barra de estado
        self._status_var = tk.StringVar(value="Inicializando…")
        self._status_lbl = tk.Label(self, textvariable=self._status_var,
                                    bg=T["status_bg"], fg=T["status_fg"],
                                    font=("Courier", 8), anchor=tk.W, padx=8)
        self._status_lbl.pack(side=tk.BOTTOM, fill=tk.X)

        # Combobox style
        st = ttk.Style()
        st.theme_use("clam")
        st.configure("TCombobox",
                     fieldbackground=T["entry_bg"], background=T["entry_bg"],
                     foreground=T["entry_fg"], arrowcolor=T["bar_lbl"],
                     selectbackground=T["btn_active_bg"])

    def _bind_keys(self):
        """Bind keyboard shortcuts to the window."""
        self.bind("<Up>",        lambda _: self._key_pan(0,  -self.PAN_STEP_PX))
        self.bind("<Down>",      lambda _: self._key_pan(0,   self.PAN_STEP_PX))
        self.bind("<Left>",      lambda _: self._key_pan(-self.PAN_STEP_PX, 0))
        self.bind("<Right>",     lambda _: self._key_pan( self.PAN_STEP_PX, 0))
        self.bind("<minus>",      lambda _: self._key_zoom(1 / 1.2))
        self.bind("<equal>",     lambda _: self._key_zoom(1 / 1.2))
        self.bind("<KP_Add>",    lambda _: self._key_zoom(1 / 1.2))
        self.bind("<plus>",     lambda _: self._key_zoom(1.2))
        self.bind("<KP_Subtract>", lambda _: self._key_zoom(1.2))
        self.bind("<KP_0>",      lambda _: self._reset_view())
        self.bind("<Key-0>",     lambda _: self._reset_view())
       # self.bind("<n>",         lambda _: self._toggle_night())
       # self.bind("<N>",         lambda _: self._toggle_night())

    # panel de control

    _PAD_BTN_SIZE = 28   
    _PAD_GAP      = 3    
    _PAD_MARGIN   = 12   

    def _pad_layout(self, W, H):
        """
        diccionario
          [      ] [ up   ] [      ]
          [ left ] [ rst  ] [ right]
          [zoom- ] [ down ] [zoom+ ]
        """
        bs = self._PAD_BTN_SIZE
        g  = self._PAD_GAP
        m  = self._PAD_MARGIN
        step = bs + g

        # abajo derecha anclado
        ox = W - m - 3 * step + g
        oy = H - m - 3 * step + g

        def cell(col, row):
            x1 = ox + col * step
            y1 = oy + row * step
            return x1, y1, x1 + bs, y1 + bs

        return {
            "up":       cell(1, 0),
            "left":     cell(0, 1),
            "reset":    cell(1, 1),
            "right":    cell(2, 1),
            "zoom_out": cell(0, 2),
            "down":     cell(1, 2),
            "zoom_in":  cell(2, 2),
        }

    def _pad_labels(self):
        return {
            "up":       "▲",
            "down":     "▼",
            "left":     "◀",
            "right":    "▶",
            "reset":    "⌖",
            "zoom_in":  "+",
            "zoom_out": "−",
        }

    # eventos

    def _on_configure(self, _=None):
        W, H = self._WH()
        if W > 10 and not self._vp_initialised:
            self._vp.reset(W, H)
            self._vp_initialised = True
        self._redraw()

    def _on_live_toggle(self):
        if self.live_var.get():
            self._init_time_vars()
            self._refresh()

    def _toggle_night(self):
        # tema manual
        if  self.night_var.get():
            self.night_var.set(True)
        else:
            self.night_var.set(False)
        self._apply_theme()

    def _reset_view(self):
        W, H = self._WH()
        self._vp.reset(W, H)
        self._redraw()

    def _zoom(self, event, factor):
        W, H = self._WH()
        self._vp.zoom_at(factor, event.x, event.y, W, H)
        self._redraw()

    def _on_mousewheel(self, event):
        self._zoom(event, 1 / 1.15 if event.delta < 0 else 1.15)

    def _key_pan(self, dpx, dpy):
        self._vp.pan_by_pixels(dpx, dpy)
        self._redraw()

    def _key_zoom(self, factor):
        W, H = self._WH()
        self._vp.zoom_centre(factor, W, H)
        self._redraw()

    def _drag_start_cb(self, event):
        self._drag_start = (event.x, event.y,
                            self._vp.pan_sx, self._vp.pan_sy)
        self.canvas.config(cursor="fleur")

    def _drag_move_cb(self, event):
        if self._drag_start is None:
            return
        x0, y0, psx0, psy0 = self._drag_start
        self._vp.pan_sx = psx0 + (event.x - x0) / self._vp.scale
        self._vp.pan_sy = psy0 - (event.y - y0) / self._vp.scale
        self._redraw()

    def _drag_end_cb(self, _):
        self._drag_start = None
        self.canvas.config(cursor="arrow")

    def _on_canvas_click(self, event):
        # toques
        if self._drag_start is not None:
            return
        W, H = self._WH()
        layout = self._pad_layout(W, H)
        for name, (x1, y1, x2, y2) in layout.items():
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self._pad_action(name)
                return

    def _pad_action(self, name):
        self.canvas.config(cursor="arrow")
        s = self.PAN_STEP_PX
        if name == "up":        self._key_pan(0, -s)
        elif name == "down":    self._key_pan(0,  s)
        elif name == "left":    self._key_pan(-s, 0)
        elif name == "right":   self._key_pan( s, 0)
        elif name == "zoom_in":  self._key_zoom(1.2)
        elif name == "zoom_out": self._key_zoom(1 /1.2)
        elif name == "reset":    self._reset_view()

    # planteo

    def _schedule(self):
        self._refresh()
        self._after_id = self.after(self.REFRESH_MS, self._schedule)

    def _refresh(self):
        if self._after_id:
            self.after_cancel(self._after_id)
        if self.live_var.get():
            self._init_time_vars()
        lat = self.lat_var.get()
        lon = self.lon_var.get()
        t   = self._get_astropy_time()
        self._status_var.set("Computando posiciones…")

        def worker():
            try:
                objs = compute_sky(lat, lon, t)
                self.after(0, lambda: self._on_done(objs, t))
            except Exception as exc:
                self.after(0, lambda: self._status_var.set(f"Error: {exc}"))

        threading.Thread(target=worker, daemon=True).start()
        self._after_id = self.after(self.REFRESH_MS, self._schedule)

    def _on_done(self, objects, t):
        self._sky_objects = objects
        utc = t.strftime('%H:%M:%S %d %b %Y')
        self._clock.config(text=utc)
        vis = sum(1 for o in objects if o[0] > 0)
        self._status_var.set(
            f"Lat {self.lat_var.get():.2f}°  "
            f"Lon {self.lon_var.get():.2f}°  │  "
            f"{vis} objetos sobre horizonte  │  {utc}  │  "
            f"Rueda/+− para zoom  ·  Arrastra el cursor o usa las flechas para mover  ·  0 para restablecer "
        )
        self._redraw()

    # dibujar canvas

    def _redraw(self, *_):
        c    = self.canvas
        T    = self._T
        W, H = self._WH()
        if W < 10 or H < 10:
            return

        c.delete("all")
        vp = self._vp

        # fondo
        c.create_rectangle(0, 0, W, H, fill=T["canvas_bg"], outline="")
        ri, ro = T["sky_inner"], T["sky_outer"]
        zx, zy = vp.sky_to_canvas(0, 0, W, H)
        for step in range(28, 0, -1):
            f   = step / 28
            rr  = int(ri[0] + (ro[0] - ri[0]) * (1 - f))
            gg  = int(ri[1] + (ro[1] - ri[1]) * (1 - f))
            bb  = int(ri[2] + (ro[2] - ri[2]) * (1 - f))
            col = f"#{rr:02x}{gg:02x}{bb:02x}"
            pr  = vp.scale * 90 * f
            c.create_oval(zx - pr, zy - pr, zx + pr, zy + pr,
                          fill=col, outline="")

        if self.show_grid.get():
            self._draw_grid(c, T, W, H)

        self._draw_horizon_ring(c, T, W, H)
        self._draw_compass_ring(c, T, W, H)
        self._draw_objects(c, T, W, H)
        self._draw_zenith_marker(c, T, W, H)
        self._draw_hud(c, T, W, H)
        self._draw_control_pad(c, T, W, H)

    # cuadricula

    def _draw_grid(self, c, T, W, H):
        vp = self._vp

        for alt in range(0, 91, 15):
            zen  = 90.0 - alt
            r_px = zen * vp.scale
            zx, zy = vp.sky_to_canvas(0, 0, W, H)
            if alt == 0:
                col, wd, dash = T["horizon"], 2, ()
            else:
                col, wd, dash = T["grid_ring"], 1, (4, 6)
            c.create_oval(zx - r_px, zy - r_px, zx + r_px, zy + r_px,
                          outline=col, width=wd, dash=dash)
            lx, ly = vp.sky_to_canvas(zen, 0.0, W, H)
            if 0 < alt < 90 and 0 <= lx <= W and 0 <= ly <= H:
                c.create_text(lx + 4, ly, text=f"{alt}°",
                              fill=T["grid_lbl"], font=("Courier", 9), anchor="w")

        for az in range(0, 360, 10):
            ang    = math.radians(az)
            sx_out = 90 * math.sin(ang)
            sy_out = -90 * math.cos(ang)
            ox, oy = vp.sky_to_canvas(0, 0, W, H)
            ex, ey = vp.sky_to_canvas(sx_out, sy_out, W, H)
            if az % 90 == 0:
                col, dash = T["grid_spoke_card"], ()
            elif az % 30 == 0:
                col, dash = T["grid_spoke_maj"], (4, 6)
            else:
                col, dash = T["grid_spoke_min"], (2, 10)
            c.create_line(ox, oy, ex, ey, fill=col, dash=dash, width=1)

            if az % 30 == 0:
                lsx1 = 84 * math.sin(ang)
                lsy1 = -84 * math.cos(ang)

                magicnumber = 0.0523599

                lsx = lsx1 * math.cos(magicnumber) - lsy1 * math.sin(magicnumber)
                lsy = lsx1 * math.sin(magicnumber) + lsy1 * math.cos(magicnumber)


                lx, ly = vp.sky_to_canvas(lsx, lsy, W, H)
                if 0 <= lx <= W and 0 <= ly <= H:
                    c.create_text(lx, ly, text=f"{az}°",
                                  fill=T["grid_az_lbl"],
                                  font=("Courier", 9), anchor="center")

    # horizonte (anillo)

    def _draw_horizon_ring(self, c, T, W, H):
        vp   = self._vp
        zx, zy = vp.sky_to_canvas(0, 0, W, H)
        r_px = 90 * vp.scale
        c.create_oval(zx - r_px, zy - r_px, zx + r_px, zy + r_px,
                      outline=T["horizon"], width=3)

    # Brujula

    def _draw_compass_ring(self, c, T, W, H):
        vp      = self._vp
        inner   = 90.5
        outer1  = 91.5
        mid5    = 92.5
        mid10   = 94.0
        label_r = 98.2
        name_r  = 106.0

        for az in range(0, 360):
            ang  = math.radians(az)
            sa, ca = math.sin(ang), -math.cos(ang)

            r_out = mid10 if az % 10 == 0 else (mid5 if az % 5 == 0 else outer1)
            x1, y1 = vp.sky_to_canvas(inner * sa, inner * ca, W, H)
            x2, y2 = vp.sky_to_canvas(r_out * sa, r_out * ca, W, H)

            if not (-200 < x1 < W + 200 and -200 < y1 < H + 200):
                continue

            if az % 10 == 0:
                col, wd = T["comp_tick10"], 2
            elif az % 5 == 0:
                col, wd = T["comp_tick5"], 1
            else:
                col, wd = T["comp_tick1"], 1

            c.create_line(x1, y1, x2, y2, fill=col, width=wd)

            if az % 10 == 0:
                lx, ly = vp.sky_to_canvas(label_r * sa, label_r * ca, W, H)
                if -40 < lx < W + 40 and -40 < ly < H + 40:
                    c.create_text(lx, ly, text=str(az),
                                  fill=T["comp_num"], font=("Courier", 10),
                                  angle=(az - 90) % 360)

        for az, name in _COMPASS_NAMES.items():
            ang  = math.radians(az)
            card = len(name) == 1
            nsx  = name_r * math.sin(ang)
            nsy  = -name_r * math.cos(ang)
            nx, ny = vp.sky_to_canvas(nsx, nsy, W, H)
            if -60 < nx < W + 60 and -60 < ny < H + 60:
                c.create_text(nx, ny, text=name,
                              fill=T["comp_card"] if card else T["comp_inter"],
                              font=("Courier", 11 if card else 8,
                                    "bold" if card else "normal"))

    # objetos

    def _draw_objects(self, c, T, W, H):
        vp       = self._vp
        deferred = []

        for obj in self._sky_objects:
            alt, az, mag, color, name, kind = obj
            if kind == "planet" and not self.show_planets.get():
                continue
            s = Viewport.altaz_to_sky(alt, az)
            if s is None:
                continue
            sx, sy = s
            if not vp.on_canvas(sx, sy, W, H, margin=20):
                continue
            x, y = vp.sky_to_canvas(sx, sy, W, H)
            r    = mag_to_r(mag)

            if mag < 3:
                gr = r + max(2, int((3 - mag) * 2.5))
                c.create_oval(x - gr, y - gr, x + gr, y + gr,
                              fill=_dim(color, 0.15), outline="")

            if kind == "planet":
                c.create_oval(x - r, y - r, x + r, y + r,
                              fill=color, outline="#FFFFFF", width=1)
                bn = name.lower()
                if bn == "saturn":
                    c.create_oval(x - r - 5, y - 2, x + r + 5, y + 2,
                                  outline="#BB9944", width=1)
                if bn == "sun":
                    for ray in range(0, 360, 45):
                        ra_ = math.radians(ray)
                        c.create_line(x + (r + 2) * math.cos(ra_),
                                      y + (r + 2) * math.sin(ra_),
                                      x + (r + 7) * math.cos(ra_),
                                      y + (r + 7) * math.sin(ra_),
                                      fill="#FFDD44", width=1)
                if bn == "moon":
                    c.create_arc(x - r, y - r, x + r, y + r,
                                 start=270, extent=180,
                                 fill=_dim(color, 0.6), outline="",
                                 style=tk.CHORD)
            else:
                c.create_oval(x - r, y - r, x + r, y + r,
                              fill=color, outline="")

            if self.show_labels.get():
                if kind == "planet" and name.lower() not in ("uranus", "neptune"):
                    deferred.append((x, y + r + 8, name, _dim(color, 0.9)))
                elif kind == "star" and name and mag < 2.8:
                    deferred.append((x, y + r + 7, name, _dim(color, 0.75)))

        for lx, ly, lt, lc in deferred:
            c.create_text(lx, ly, text=lt, fill=lc,
                          font=("Courier", 8), anchor="n")

    # zenith (vertical)

    def _draw_zenith_marker(self, c, T, W, H):
        zx, zy = self._vp.sky_to_canvas(0, 0, W, H)
        if not (0 <= zx <= W and 0 <= zy <= H):
            return
        s = 8
        c.create_line(zx - s, zy, zx + s, zy, fill=T["zenith"], width=1)
        c.create_line(zx, zy - s, zx, zy + s, fill=T["zenith"], width=1)
        c.create_text(zx + s + 3, zy, text="Z",
                      fill=T["zenith"], font=("Courier", 7), anchor="w")

    # hud

    def _draw_hud(self, c, T, W, H):
        vp = self._vp
        csx, csy = vp.canvas_to_sky(W / 2, H / 2, W, H)
        alt, az  = vp.sky_to_altaz(csx, csy)
        deg100   = 100 / vp.scale
        hud = (f"Centro: Az {az:.1f}°  Alt {alt:.1f}°  │  "
               f"{deg100:.1f}°/100px")
        c.create_text(8, H - 4, text=hud, anchor="sw",
                      fill=T["hud_txt"], font=("Courier", 8))

        # norte
        n_sx, n_sy = 0.0, -2.0
        nx, ny = vp.sky_to_canvas(n_sx, n_sy, W, H)
        cxm, cym = 30, 30
        ang  = math.atan2(nx - W / 2, -(ny - H / 2))
        L    = 18
        c.create_line(cxm - L * math.sin(ang), cym + L * math.cos(ang),
                      cxm + L * math.sin(ang), cym - L * math.cos(ang),
                      fill=T["hud_arrow"], width=2,
                      arrow=tk.LAST, arrowshape=(8, 10, 4))
        c.create_text(cxm, cym + L + 10, text="Vertical",
                      fill=T["hud_arrow"], font=("Courier", 8, "bold"))

    # Panel

    def _draw_control_pad(self, c, T, W, H):
        layout = self._pad_layout(W, H)
        labels = self._pad_labels()
        bs     = self._PAD_BTN_SIZE

        xs = [x1 for x1, y1, x2, y2 in layout.values()]
        ys = [y1 for x1, y1, x2, y2 in layout.values()]
        x2s = [x2 for x1, y1, x2, y2 in layout.values()]
        y2s = [y2 for x1, y1, x2, y2 in layout.values()]
        pad = 6
        c.create_rectangle(min(xs) - pad, min(ys) - pad,
                           max(x2s) + pad, max(y2s) + pad,
                           fill=T["pad_bg"], outline=T["pad_border"],
                           width=1)

        for name, (x1, y1, x2, y2) in layout.items():
            # Boton
            c.create_rectangle(x1, y1, x2, y2,
                               fill=T["pad_btn_bg"],
                               outline=T["pad_border"], width=1)
            # Simbolo
            label = labels[name]
            # Zoom 
            font_sz = 13 if name in ("zoom_in", "zoom_out") else 11
            c.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                          text=label, fill=T["pad_btn_fg"],
                          font=("Courier", font_sz, "bold"))

    # herrramientas

    def _clear_tooltip(self, *_):
        for item in self._tooltip_items:
            self.canvas.delete(item)
        self._tooltip_items.clear()

    def _on_motion(self, event):
        if self._drag_start:
            self._clear_tooltip()
            return
        self._clear_tooltip()
        W, H = self._WH()
        vp   = self._vp
        T    = self._T
        best, best_d = None, 16

        for obj in self._sky_objects:
            alt, az, mag, color, name, kind = obj
            if kind == "planet" and not self.show_planets.get():
                continue
            s = Viewport.altaz_to_sky(alt, az)
            if not s:
                continue
            x, y = vp.sky_to_canvas(s[0], s[1], W, H)
            d    = math.hypot(event.x - x, event.y - y)
            if d < best_d:
                best_d, best = d, obj

        if not best:
            return
        alt, az, mag, color, name, kind = best
        label = name if name else ("Star" if kind == "star" else kind)
        tip   = f"{label}\nAlt {alt:.1f}°  Az {az:.1f}°\nMag {mag:.1f}"
        tx, ty = event.x + 14, event.y - 14
        bg  = self.canvas.create_rectangle(
            tx - 130, ty - 50, tx + 20, ty + 4,
            fill=T["tip_bg"], outline=T["tip_border"], width=1)
        txt = self.canvas.create_text(
            tx - 126, ty -46 , text=tip, fill=T["tip_fg"],
            font=("Courier", 8), anchor="nw")
        self._tooltip_items = [bg, txt]


# applicacion

if __name__ == "__main__":
    app = TitilaApp()
    app.geometry("1080x600")
    app.state("zoomed")
    app.mainloop()

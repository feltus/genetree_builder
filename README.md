# genetree_builder

## Background
These scripts communicate with the ENSEMBL BIOMART APIs (Ensembl, Metazoa, Plants, Fungi, Protists, Bacteria) to pull gene trees using a list of species names.
biomart_url = "https://www.ensembl.org/biomart/martservice"

## Input file format
Strongylocentrotus purpuratus
Daphnia pulex
Octopus bimaculoides
Lingula anatina
Aplysia californica
Crassostrea gigas
Nematostella vectensis
Clytia hemisphaerica
Mnemiopsis leidyi
Amphimedon queenslandica

## Usage
__________________________________________________________
### ensembl_dataset_finder.py: Searches Searching for across Ensembl APIs to find the best matching dataset ID.
__________________________________________________________
```
# With a file containing species names (one per line)
python genetree_builder/ensembl_dataset_finder.py species_list.txt

# Interactive mode
python genetree_builder/ensembl_dataset_finder.py --interactive

# Specify output filename
python genetree_builder/ensembl_dataset_finder.py species_list.txt --output my_results.csv
```
EXAMPLE OUTPUT:
Read 1 species from test-metazoa.txt

Searching for Daphnia pulex across Ensembl APIs...
Searching for Daphnia pulex in Ensembl...
Searching for Daphnia pulex in Metazoa...
Searching for Daphnia pulex in Plants...
Searching for Daphnia pulex in Fungi...
Searching for Daphnia pulex in Protists...
Searching for Daphnia pulex in Bacteria...
Found 3 potential datasets for Daphnia pulex:
  1. Metazoa - dpgca021134715v1rs_eg_gene (score: 60.8)
  2. Protists - pultimum_eg_gene (score: 41.6)
  3. Fungi - mlaricipopulina_eg_gene (score: 39.6)
Results saved to ensembl_datasets_20250723_085501.csv

Results Summary:
====================================================================================================
Species                        API             Dataset                        Match Score Virtual Schema
====================================================================================================
Daphnia pulex                  Metazoa         dpgca021134715v1rs_eg_gene     60.8       metazoa_mart
Daphnia pulex                  Protists        pultimum_eg_gene               41.6       protists_mart
Daphnia pulex                  Fungi           mlaricipopulina_eg_gene        39.6       fungi_mart
----------------------------------------------------------------------------------------------------

__________________________________________________________

### list_metazoa_datasets.py: Lists all datasets in the metazoa BIOMART API.
__________________________________________________________
```
python genetree_builder/list_metazoa_datasets.py

Example Output:
Fetching BioMart registry from Ensembl Metazoa...
Found mart: Ensembl Metazoa Genes 61 (name: metazoa_mart, schema: metazoa_mart)
Found mart: Ensembl Metazoa Variations 61 (name: metazoa_variations, schema: metazoa_mart)
Found mart: Ensembl Metazoa Sequences 61 (name: metazoa_sequences, schema: metazoa_mart)
Found mart: Ensembl Metazoa Genomic Features 61 (name: metazoa_genomic_features, schema: metazoa_mart)
Found mart: Ontology Mart 114 (name: ontology, schema: metazoa_mart)

Using mart: Ensembl Metazoa Genes 61 (metazoa_mart)

Found 372 datasets in Ensembl Metazoa:
  apgca001949145v1_eg_gene - Acanthaster planci (Crown-of-thorns starfish) genes (OKI_Apl_1.0)
  aegca000204515v1rs_eg_gene - Acromyrmex echinatior (Panamanian leaf-cutter ant) genes (Aech_3.9)
  amgca013753865v1_eg_gene - Acropora millepora (Stony coral, JS-1) genes (Amil_v2.1)
  aegca011057435_eg_gene - Actinia equina (Beadlet anemone, AE1) genes (equina_smartden.arrow4.noredun)
  atgca009602425v1_eg_gene - Actinia tenebrosa (Australian red waratah sea anemone) genes (ASM960242v1)
  apgca005508785v2rs_eg_gene - Acyrthosiphon pisum (Pea aphid, AL4f) genes (pea_aphid_22Mar2018_4r6ur_v2)
  acgca023614345v1rs_eg_gene - Adelges cooleyi (Spruce gall adelgid, 19-005CV) genes (UGA_ACOO_1.1)
  avaga_eg_gene - Adineta vaga (Rotifer) genes (AMS_PRJEB1171_v1)
  aalvpagwg_eg_gene - Aedes aegypti (Yellow fever mosquito, LVP_AGWG) genes (AaegL5)
  aagca035046485v1rs_eg_gene - Aedes albopictus (Asian tiger mosquito, Foshan) - GCA_035046485.1 genes (GCA035046485v1)
  atgca024364675v1rs_eg_gene - Aethina tumida (Small hive beetle, Nest 87) genes (icAetTumi1.1)
  apgca000699045v2_eg_gene - Agrilus planipennis (Emerald ash borer, EAB-ADULT) genes (Apla_2.0)
  aagca933228735v1_eg_gene - Amblyteles armatorius (Ichneumon Wasp, reference) genes (iyAmbArma2.1)
  aagca019059575v1_eg_gene - Amphibalanus amphitrite (Acorn barnacle, SeventyFive) genes (NRLGWU_Aamphi_draft)
  aqgca000090795v2rs_eg_gene - Amphimedon queenslandica (Demosponge) genes (v1.1)
  atgca001186105v1rs_eg_gene - Amyelois transitella (Naval orange worm, UIUC subculture of SPIRL-1966) genes (ASM118610v1)
  algca028408465v1rs_eg_gene - Anastrepha ludens (Mexican fruit fly, Willacy) genes (idAnaLude1.1)
  aogca027943255v1rs_eg_gene - Anastrepha obliqua (WestIndian fruit fly, idAnaObli1) genes (idAnaObli1_1.0)
  angca916049575v1_eg_gene - Ancistrocerus nigricornis (Potter wasp, reference) genes (iyAncNigr1.1)
  ajgca011630105v1_eg_gene - Anneissia japonica (Sea lily, Jap-2015-1) genes (ASM1163010v1)
  aagca000349125v2vb_eg_gene - Anopheles albimanus (Mosquito, ALBI9_A) - GCA_000349125.2 genes (AalbS2)
  aagca013758885v1rs_eg_gene - Anopheles albimanus (Mosquitos, STELCA) - GCF_013758885.1 [RefSeq annotation] genes (VT_AalbS3_pri_1.0)
  aarabiensis_eg_gene - Anopheles arabiensis (Mosquito, Dongola) genes (AaraD1)
  aagca914969975_eg_gene - Anopheles atroparvus (Mosquito, Infravec2 EBRE) genes (atroparvus_hifiasm_n225_277Mb)
  achristyi_eg_gene - Anopheles christyi (Mosquito, ACHKN1017) genes (AchrA1)
  acgca004136515v2vb_eg_gene - Anopheles coluzzii (Mosquito, Ngousso) - GCA_004136515.2 genes (AcolN1)
  acgca943734685v1rs_eg_gene - Anopheles coluzzii (Mosquitos) genes (AcolN3)
  aculicifacies_eg_gene - Anopheles culicifacies (Mosquito, A-37) genes (AculA1)
  adgca943734745v1rs_eg_gene - Anopheles darlingi (American malaria mosquito) - GCA_943734745.1 genes (GCA943734745v1)
  adarlingi_eg_gene - Anopheles darlingi (American malaria mosquito, Coari) genes (AdarC3)
  adirus_eg_gene - Anopheles dirus (Mosquito, WRAIR2) genes (AdirW1)
  aepiroticus_eg_gene - Anopheles epiroticus (Mosquito, Epiroticus2) genes (AepiE1)
  afarauti_eg_gene - Anopheles farauti (Mosquito, FAR1) genes (AfarF2)
  afgca943734845v1rs_eg_gene - Anopheles funestus (African malaria mosquito) genes (idAnoFuneDA-416_04)
  afunestus_eg_gene - Anopheles funestus (African malaria mosquito, FUMOZ) genes (AfunF3)
  aggca943734735v2vb_eg_gene - Anopheles gambiae (African malaria mosquito) - GCA_943734735.2 genes (GCA943734735v2)
  agambiae_eg_gene - Anopheles gambiae (African malaria mosquito, PEST) - GCA_000005575.1 genes (AgamP4)
  amaculatus_eg_gene - Anopheles maculatus (Mosquito, maculatus3) genes (AmacM1)
  amelas_eg_gene - Anopheles melas (Mosquito, CM1001059_A) genes (AmelC2)
  amerus_eg_gene - Anopheles merus (Mosquito, MAF) genes (AmerM2)
  aminimus_eg_gene - Anopheles minimus (Mosquito, MINIMUS1) genes (AminM1)
  aqgca000349065v1vb_eg_gene - Anopheles quadriannulatus (Mosquito, SANGWE) - GCA_000349065.1 genes (AquaS1)
  aschina_eg_gene - Anopheles sinensis (Mosquito, China) genes (AsinC2)
  asinensis_eg_gene - Anopheles sinensis (Mosquito, SINENSIS) genes (AsinS2)
  asindian_eg_gene - Anopheles stephensi (Asian malaria mosquito, Indian) genes (AsteI2)
  astephensi_eg_gene - Anopheles stephensi (Asian malaria mosquito, SDA-500) genes (AsteS1)
  aglabripennis_eg_gene - Anoplophora glabripennis (Asian long-horned beetle, ALB-LARVAE) genes (Agla_2.0)
  aggca022605725v3rs_eg_gene - Anthonomus grandis grandis (Boll weevil) genes (icAntGran1.3)
  aggca014905175v1_eg_gene - Aphidius gifuensis (Parasitoid wasp, YNYX2018) genes (ASM1490517v1)
  adgca000469605v1rs_eg_gene - Apis dorsata (Giant honeybee) genes (Apis_dorsata_1.3)
  afgca000184785v2rs_eg_gene - Apis florea (Dwarf honeybee) genes (Aflo_1.0)
  amellifera_eg_gene - Apis mellifera (Honey bee, DH4) genes (Amel_HAv3.1)
  acgca000002075v2_eg_gene - Aplysia californica (California sea hare, F4 #8) genes (AplCal3.0)
  abgca947563725v1rs_eg_gene - Argiope bruennichi (Spiders) - GCF_947563725.1 [RefSeq annotation] genes (qqArgBrue1.1)
  asuum_eg_gene - Ascaris suum (Pig roundworm, AG01) genes (ASM18702v3)
  argca902459465v3_eg_gene - Asterias rubens (European starfish) genes (eAstRub1.3)
  argca917208135v1_eg_gene - Athalia rosae (Coleseed sawfly, reference) genes (iyAthRosa1.1)
  acephalotes_eg_gene - Atta cephalotes (Leaf-cutter ant) genes (Attacep1.0)
  bdgca000789215v2_eg_gene - Bactrocera dorsalis (Oriental fruit fly, Punador) genes (ASM78921v2)
  blgca001853355v1_eg_gene - Bactrocera latifrons (Solanum fruit fly, USDA-ARS-PBARC rearing strain) genes (ASM185335v1)
  bngca024586455v2rs_eg_gene - Bactrocera neohumeralis (Lesser Queensland fruit fly, Rockhampton) genes (APGP_CSIRO_Bneo_wtdbg2_racon_allhic_juicebox.fasta_v2)
  btgca016617805v2_eg_gene - Bactrocera tryoni (Queensland fruitfly, S06) genes (CSIRO_BtryS06_freeze1)
  bantarctica_eg_gene - Belgica antarctica (Antarctic midge) genes (ASM77530v1)
  btasiaii5_eg_gene - Bemisia tabaci (Silverleaf whitefly, Asia II-5) genes (ASIAII5_n227_616Mb)
  btssa1nig_eg_gene - Bemisia tabaci (Silverleaf whitefly, SSA1-SG1 Ng) genes (SSA1SG1_Nigeria_n4493_656Mb)
  btssa1ug_eg_gene - Bemisia tabaci (Silverleaf whitefly, SSA1-SG1 Ug) genes (SSA1_SG1_Uganda_n955_657Mb)
  btssa2nig_eg_gene - Bemisia tabaci (Silverleaf whitefly, SSA2 Ng) genes (SSA2_Nigeria_n785_625mb)
  btssa3nig_eg_gene - Bemisia tabaci (Silverleaf whitefly, SSA3 Ng) genes (SSA3_Nigeria_2278n_648mb)
  btuganda1_eg_gene - Bemisia tabaci (Silverleaf whitefly, Uganda-1) genes (Uganda1_n5713_630Mb)
  bagca900239965v1rs_eg_gene - Bicyclus anynana (Squinting bush brown) genes (Bicyclus_anynana_v1.2)
  bggca947242115v1rs_eg_gene - Biomphalaria glabrata (Bloodfluke planorb) - GCA_947242115.1 genes (GCA947242115v1)
  bglabrata_eg_gene - Biomphalaria glabrata (Bloodfluke planorb, BB02) genes (BglaB1)
  bagca024516045v2rs_eg_gene - Bombus affinis (Rusty patched bumble bee, iyBomAffi1) genes (iyBomAffi1.2)
  bhgca024542735v1rs_eg_gene - Bombus huntii (Hunt's bumblebee, Logan2020A) genes (iyBomHunt1.1)
  bimpatiens_eg_gene - Bombus impatiens (Common eastern bumblebee) genes (BIMP_2.2)
  btgca910591885v2_eg_gene - Bombus terrestris (buff-tailed bumblebee, reference) genes (iyBomTerr1.2)
  bvgca011952275v1rs_eg_gene - Bombus vancouverensis nearcticus (Montane Bumble Bee, JDL1245) genes (Bvanc_JDL1245)
  bmgca003987935v1rs_eg_gene - Bombyx mandarina (Wild silkworm, Bman2017) genes (ASM398793v1)
  bmori_eg_gene - Bombyx mori (Domestic silkworm, p50T) genes (Bmori_2016v1.0)
  bmgca030269925v1rs_eg_gene - Bombyx mori (Silk Moth) - GCF_030269925.1 [RefSeq annotation] genes (ASM3026992v2)
  blanceolatum_eg_gene - Branchiostoma lanceolatum (Amphioxus) genes (BraLan2)
  bmalayi_eg_gene - Brugia malayi (Nematode, FR3) genes (Bmal-4.0)
  cbrenneri_eg_gene - Caenorhabditis brenneri (Nematode) genes (C_brenneri-6.0.1b)
  cbriggsae_eg_gene - Caenorhabditis briggsae (Nematode) genes (CB4)
  celegans_eg_gene - Caenorhabditis elegans (Nematode, N2) genes (WBcel235)
  cjaponica_eg_gene - Caenorhabditis japonica (Nematode) genes (C_japonica-7.0.1)
  cremanei_eg_gene - Caenorhabditis remanei (Nematode) genes (C_remanei-15.0.1)
  cfgca003227725v1rs_eg_gene - Camponotus floridanus (Florida carpenter ant, SB8) genes (Cflo_v7.5)
  cteleta_eg_gene - Capitella teleta (Bristle worm) genes (Capitella teleta v1.0)
  chgca021464435v1rs_eg_gene - Cataglyphis hispanica (Desert ant, Lineage 1) genes (ULB_Chis1_1.0)
  csgca000671375v2_eg_gene - Centruroides sculpturatus (Bark scorpion, CEXI.00-Female) genes (Cexi_2.0)
  ccgca000347755v4_eg_gene - Ceratitis capitata (Mediterranean fruit fly) genes (Ccap_2.0)
  cigca013357705v1rs_eg_gene - Chelonus insularis (Parasitoid wasp, UGA/USDA-ARS -01) genes (ASM1335770v1)
  cqgca026875155v2rs_eg_gene - Cherax quadricarinatus (Australian red claw crayfish, HC-2022) genes (ASM2687515v2)
  ccgca905475395v1rs_eg_gene - Chrysoperla carnea (Insects) - GCF_905475395.1 [RefSeq annotation] genes (inChrCarn1.1)
  clectularius_eg_gene - Cimex lectularius (Bed bug, Harlan) genes (Clec_2.0)
  chgca902728285_eg_gene - Clytia hemisphaerica (Jellyfish, Z4C2) genes (Clytia_hemisphaerica_genome_assembly)
  cfgca000648655v2_eg_gene - Copidosoma floridanum (Parasitoid wasp, CFLO.00-Male) genes (Cflo_2.0)
  cmgca914767935v1_eg_gene - Coremacera marginata (Sieve-winged Snailkiller, reference) genes (idCorMarg1.1)
  cggca020080835v1_eg_gene - Cotesia glomerata (White butterfly parasite wasp, CgM1) genes (MPM_Cglom_v2.3)
  cagca025612915v2rs_eg_gene - Crassostrea angulata (Portuguese oyster, pt1a10) genes (ASM2561291v2)
  cgigas_eg_gene - Crassostrea gigas (Pacific oyster) genes (cgigas_uk_roslin_v1)
  cvgca002022765v4_eg_gene - Crassostrea virginica (Eastern oyster, RU13XGHG1-28) genes (C_virginica_3.0)
  csgca002891405v2rs_eg_gene - Cryptotermes secundus (Drywood termite) genes (Csec_1.0)
  cfgca003426905v1rs_eg_gene - Ctenocephalides felis (Cat flea, EL2017-DRISC) genes (ASM342690v1)
  cpgca016801865v2rs_eg_gene - Culex pipiens pallens (Northern house mosquito, TS) genes (TS_CPP_V2)
  cqgca015732765v1vb_eg_gene - Culex quinquefasciatus (Southern house mosquito, JHB) genes (VPISU_Cqui_1.0_pri_paternal)
  cquinquefasciatus_eg_gene - Culex quinquefasciatus (Southern house mosquito, Johannesburg) genes (CpipJ2)
  cbgca036172545v1rs_eg_gene - Culicoides brevitarsis (Flies, CSIRO-B50_1) - GCF_036172545.1 [RefSeq annotation] genes (AGI_CSIRO_Cbre_v1)
  csonorensis_eg_gene - Culicoides sonorensis (Biting Midge) genes (Cson1)
  cpgca033807575v1rs_eg_gene - Cydia pomonella (The codling moth, Wapato2018A) - GCF_033807575.1 [RefSeq annotation] genes (ilCydPomo1)
  cfgca029955315v1rs_eg_gene - Cylas formicarius (Sweet potato weevil, icCylForm1) genes (icCylForm1.1)
  dvgca025091365v1rs_eg_gene - Daktulosphaira vitifoliae (Grape phylloxera, Bord-2020) genes (ASM2509136v1)
  dplexippus_eg_gene - Danaus plexippus plexippus (Monarch butterfly, F-2) genes (Dplex_v4)
  dcgca022539665v3rs_eg_gene - Daphnia carinata (Water flea, CSIRO-1) genes (CSIRO_AGI_Dcar_v0.2)
  dmgca020631705v2_eg_gene - Daphnia magna (Fresh water planktonic, NIES) genes (ASM2063170v1.1)
  dpgca021134715v1rs_eg_gene - Daphnia pulex (Common water flea, KAP4) genes (ASM2113471v1)
  dpgca021234035v2rs_eg_gene - Daphnia pulicaria (Water flea, SC F1-1A) genes (SC_F0_13B)
  dpgca000355655v1_eg_gene - Dendroctonus ponderosae (Mountain pine beetle) genes (DendPond_male_1.0)
  dggca004324835v1_eg_gene - Dendronephthya gigantea (Carnation coral, DGI-Jeju-01) genes (DenGig_1.0)
  dagca023375885v2rs_eg_gene - Dermacentor andersoni (Rocky Mountain wood tick, qqDerAnde1) genes (qqDerAnde1.2)
  dsgca013339745v2rs_eg_gene - Dermacentor silvarum (Tick, Dsil-2018) genes (BIME_Dsil_1.4)
  dpgca001901225v2_eg_gene - Dermatophagoides pteronyssinus (European house dust mite, airmid) genes (ASM190122v2)
  dvgca917563875v2rs_eg_gene - Diabrotica virgifera virgifera (Western corn rootworm) genes (PGI_DIABVI_V3a)
  dvgca003013835v2_eg_gene - Diabrotica virgifera virgifera (Western corn rootworm, Ped12-6-A-3) genes (Dvir_v2.0)
  dcgca000475195v1rs_eg_gene - Diaphorina citri (Asian citrus psyllid) genes (Diaci_psyllid_genome_assembly_version_1.1)
  dggca904063045v1_eg_gene - Dimorphilus gyrociliatus (Segmented worms) genes (Dgyrociliatus_assembly)
  dtinctorium_eg_gene - Dinothrombium tinctorium (Red velvet mite, UoL-WK) genes (DtinU1)
  dcgca026250575v1rs_eg_gene - Diorhabda carinulata (Northern tamarisk beetle, Delta) genes (icDioCari1.1)
  dsgca026230105v1rs_eg_gene - Diorhabda sublineata (Subtropical tamarisk beetle, icDioSubl1.1) genes (icDioSubl1.1)
  dngca001186385v1_eg_gene - Diuraphis noxia (Russian wheat aphid, RWA2) genes (Dnoxia_1.0)
  dpgca020536995v1rs_eg_gene - Dreissena polymorpha (Zebra mussel, Duluth1) genes (UMN_Dpol_1.0)
  dagca009650485v2rs_eg_gene - Drosophila albomicans (Fruit fly, 15112-1751.03) genes (ASM965048v2)
  dagca017639315v2rs_eg_gene - Drosophila ananassae (Fruit fly, 14024-0371.13) genes (ASM1763931v2)
  dananassae_eg_gene - Drosophila ananassae (Fruit fly, TSC#14024-0371.13) genes (dana_caf1)
  dagca001654025v1rs_eg_gene - Drosophila arizonae (Fruit fly, ariz_Son04) genes (ASM165402v1)
  dbgca025231255v1rs_eg_gene - Drosophila biarmipes (Fruit fly, raj3) genes (RU_DBia_V1.1)
  dbgca000236285v2rs_eg_gene - Drosophila bipectinata (Fruit fly) genes (Dbip_2.0)
  dbgca011750605v1rs_eg_gene - Drosophila busckii (Fruit fly, San Diego stock center stock number 13000-0081.31) genes (ASM1175060v1)
  degca000224195v2rs_eg_gene - Drosophila elegans (Fruit fly) genes (Dele_2.0)
  degca003286155v2rs_eg_gene - Drosophila erecta (Fruit fly, 14021-0224.00,06,07) genes (DereRS2)
  derecta_eg_gene - Drosophila erecta (Fruit fly, TSC#14021-0224.01) genes (dere_caf1)
  degca018153835v1rs_eg_gene - Drosophila eugracilis (Fruit fly, 14026-0451.02) genes (ASM1815383v1)
  dfgca018152265v1rs_eg_gene - Drosophila ficusphila (Fruit fly, 14025-0441.05) genes (ASM1815226v1)
  dggca018153295v1rs_eg_gene - Drosophila grimshawi (Fruit fly, 15287-2541.00) genes (ASM1815329v1)
  dgrimshawi_eg_gene - Drosophila grimshawi (Fruit fly, TSC#15287-2541.00) genes (dgri_caf1)
  dggca900245975v1rs_eg_gene - Drosophila guanche (Fruit fly) genes (DGUA_6)
  dggca025200985v1rs_eg_gene - Drosophila gunungcola (Fruit fly, Sukarami) genes (Dgunungcola_SK_2)
  dhgca003285905v2rs_eg_gene - Drosophila hydei (Fruit fly, 15085-1641.00,03,60) genes (DhydRS2)
  digca004354385v1rs_eg_gene - Drosophila innubila (Fruit fly, TH190305) genes (UK_Dinn_1.0)
  dkgca018152535v1rs_eg_gene - Drosophila kikkawai (Fruit fly, 14028-0561.14) genes (ASM1815253v1)
  dmgca004382145v1rs_eg_gene - Drosophila mauritiana (Fruit fly, mau12) genes (ASM438214v1)
  dmelanogaster_eg_gene - Drosophila melanogaster (Fruit fly) - GCA_000001215.4 [FlyBase annotation] genes (BDGP6.54)
  dmgca003369915v2rs_eg_gene - Drosophila miranda (Fruit fly, MSH22) genes (D.miranda_PacBio2.1)
  dmgca018153725v1rs_eg_gene - Drosophila mojavensis (Fruit fly, 15081-1352.22) genes (ASM1815372v1)
  dmojavensis_eg_gene - Drosophila mojavensis (Fruit fly, TSC#15081-1352.22) genes (dmoj_caf1)
  dngca001654015v2rs_eg_gene - Drosophila navojoa (Fruit fly, navoj_Jal97) genes (UFRJ_Dnav_4.2)
  dogca018151105v1rs_eg_gene - Drosophila obscura (Fruit fly, BZ-5 IFL) genes (ASM1815110v1)
  dpgca003286085v2rs_eg_gene - Drosophila persimilis (Fruit fly, 14011-0111.01,24,50) genes (DperRS2)
  dpersimilis_eg_gene - Drosophila persimilis (Fruit fly, MSH-3) genes (dper_caf1)
  dpgca009870125v2rs_eg_gene - Drosophila pseudoobscura (Fruit fly, MV2-25) genes (UCI_Dpse_MV25)
  dpseudoobscura_eg_gene - Drosophila pseudoobscura pseudoobscura (Fruit fly, MV2-25) genes (Dpse_3.0)
  drgca018152115v1rs_eg_gene - Drosophila rhopaloa (Fruit fly, 14029-0021.01) genes (ASM1815211v1)
  dsgca016746245v2rs_eg_gene - Drosophila santomea (Fruit fly, STO CAGO 1482) genes (Prin_Dsan_1.1)
  dsechellia_eg_gene - Drosophila sechellia (Fruit fly, Rob3c) genes (dsec_caf1)
  dsgca004382195v2rs_eg_gene - Drosophila sechellia (Fruit fly, sech25) genes (ASM438219v2)
  dsimulans_eg_gene - Drosophila simulans (Fruit fly, w501) genes (ASM75419v3)
  dsgca016746395v2rs_eg_gene - Drosophila simulans (Fruit fly, w501) genes (Prin_Dsim_3.1)
  dsgca008121235v1rs_eg_gene - Drosophila subobscura (Fruit fly, 14011-0131.10) genes (UCBerk_Dsub_1.0)
  dsgca014743375v2rs_eg_gene - Drosophila subpulchrella (Fruit fly, 33 F10 #4) genes (RU_Dsub_v1.1)
  dsgca013340165v1rs_eg_gene - Drosophila suzukii (Fruit fly, WT3_2.0) genes (LBDM_Dsuz_2.1.pri)
  dtgca018152695v1rs_eg_gene - Drosophila takahashii (Fruit fly, IR98-3 E-12201) genes (ASM1815269v1)
  dtgca016746235v2rs_eg_gene - Drosophila teissieri (Fruit fly, GT53w) genes (Prin_Dtei_1.1)
  dvgca003285735v2rs_eg_gene - Drosophila virilis (Fruit fly, 15010-1051.48,49,85) genes (DvirRS2)
  dvirilis_eg_gene - Drosophila virilis (Fruit fly, TSC#15010-1051.87) genes (dvir_caf1)
  dwgca018902025v2rs_eg_gene - Drosophila willistoni (Fruit fly, 14030-0811.24) genes (UCI_dwil_1.1)
  dwillistoni_eg_gene - Drosophila willistoni (Fruit fly, TSC#14030-0811.24) genes (dwil_caf1)
  dygca016746365v2rs_eg_gene - Drosophila yakuba (Fruit fly, Tai18E2) genes (Prin_Dyak_Tai18E2_2.1)
  dngca001272555v1rs_eg_gene - Dufourea novaeangliae (Bee, 0120121106) genes (ASM127255v1)
  eggca000524195v1rs_eg_gene - Echinococcus granulosus (Dog tapeworm) genes (ASM52419v1)
  esgca024679095v1rs_eg_gene - Eriocheir sinensis (Chinese mitten crab) genes (ASM2467909v1)
  emgca001483705v1rs_eg_gene - Eufriesea mexicana (Bee, 0111107269) genes (ASM148370v1)
  ecgca000591075v1rs_eg_gene - Eurytemora carolleeae (Crustaceans) - GCF_000591075.1 [RefSeq annotation] genes (Eaff_2.0)
  edgca001417965v1_eg_gene - Exaiptasia diaphana (Sea anemone, CC7) genes (Aiptasia_genome_1.1)
  fcandida_eg_gene - Folsomia candida (Springtail, str. VU population) genes (ASM221717v1)
  gogca000255335v2rs_eg_gene - Galendromus occidentalis (Western predatory mite) genes (Mocc_1.0)
  gmgca003640425v2rs_eg_gene - Galleria mellonella (Greater wax moth, Carbio01_MB) genes (ASM364042v2)
  gagca016097555v1_eg_gene - Gigantopelta aegis (Deep sea snail, Gae_Host) genes (Gae_host_genome)
  gausteni_eg_gene - Glossina austeni (Tsetse fly, TTRI) genes (GausT1)
  gbrevipalpis_eg_gene - Glossina brevipalpis (Tsetse fly, IAEA) genes (GbreI1)
  gfuscipes_eg_gene - Glossina fuscipes (Tsetse fly, IAEA_lab_2018) genes (Yale_Gfus_2)
  gmorsitans_eg_gene - Glossina morsitans morsitans (Tsetse fly, Yale) - GCA_001077435.1 genes (GmorY1)
  gpallidipes_eg_gene - Glossina pallidipes (Tsetse fly, IAEA) genes (GpalI1)
  gpalpalis_eg_gene - Glossina palpalis gambiensis (Tsetse fly, IAEA) genes (GpapI1)
  gpgca936435175v1_eg_gene - Glyphotaelius pellucidus (Caddisflies, reference) genes (iiGlyPell1.1)
  gsgca954871325v1rs_eg_gene - Gordionus sp. m RMFG-2023 (Horsehair worms) - GCF_954871325.1 [RefSeq annotation] genes (tfGorSpeb1_WG_v2)
  hlgca001263275v1rs_eg_gene - Habropoda laboriosa (Southeastern blueberry bee, 0110345459) genes (ASM126327v1)
  hlgca013339765v2vb_eg_gene - Haemaphysalis longicornis (Longhorned tick, HaeL-2018) - GCA_013339765.2 genes (GCA013339765v2)
  hpgca963675165v1rs_eg_gene - Halichondria panicea (Sponges) - GCF_963675165.1 [RefSeq annotation] genes (odHalPani1.1)
  hrgca003918875v1rs_eg_gene - Haliotis rubra (Blacklip abalone, DU_JTF1) genes (ASM391887v1)
  hrgca023055435v1rs_eg_gene - Haliotis rufescens (Red abalone, VD_foot) genes (xgHalRufe1.0.p)
  hhgca000696795v2rs_eg_gene - Halyomorpha halys (Brown marmorated stink bug, HHAL.00) genes (Hhal_2.0)
  hsgca003227715v2rs_eg_gene - Harpegnathos saltator (Indian jumping ant, DR-91) genes (Hsal_v8.5)
  hmelpomene_eg_gene - Heliconius melpomene (Postman butterfly) genes (Hmel1)
  hagca023701775v1rs_eg_gene - Helicoverpa armigera (Cotton bollworm, SCD) genes (HaSCD2)
  hzgca022581195v1rs_eg_gene - Helicoverpa zea (Corn earworm, HzStark_Cry1AcR) genes (ilHelZeax1.1)
  hrobusta_eg_gene - Helobdella robusta (Freshwater leech) genes (Helro1)
  higca905115235v1_eg_gene - Hermetia illucens (Black soldier fly) genes (iHerIll2.2.curated.20191125)
  hmiamia_eg_gene - Hofstenia miamia (Panther worm, MS-H3) genes (HmiaM1)
  hvgca021130785v2rs_eg_gene - Homalodisca vitripennis (Glassy winged sharpshooter, AUS2020) genes (UT_GWSS_2.1)
  hagca018991925v1_eg_gene - Homarus americanus (American lobster, GMGI-L3) genes (GMGI_Hamer_2.0)
  hggca958450375v1_eg_gene - Homarus gammarus (European lobster, reference) genes (Homarus_gammarus)
  hagca000764305v2_eg_gene - Hyalella azteca (Amphipod, HAZT.00-mixed) genes (Hazt_2.0)
  hagca013339685v2vb_eg_gene - Hyalomma asiaticum (Tick, Hyas-2018) - GCA_013339685.2 genes (GCA013339685v2)
  hagca013339685v1_eg_gene - Hyalomma asiaticum (Tick, Hyas-2018) genes (ASM1333968v1)
  hvgca022113875v1rs_eg_gene - Hydra vulgaris (Swiftwater hydra, 105) genes (Hydra_105_v3)
  hsgca029227915v2rs_eg_gene - Hydractinia symbiolongicarpus (Hydrozoan, clone_291-10) genes (HSymV2.1)
  hagca026225885v1rs_eg_gene - Hylaeus anthracinus (Anthricinan yellow-faced bee, JK02) genes (UHH_iyHylAnth1.0_haploid)
  hvgca026283585v1rs_eg_gene - Hylaeus volcanicus (Volcano Masked Bee, JK05) genes (UHH_iyHylVolc1.0_haploid)
  hmicrostoma_eg_gene - Hymenolepis microstoma (Rodent tapeworm) genes (HMN_v3)
  hegca002082055v1_eg_gene - Hypsibius exemplaris (Water bear tardigrade, Z151) genes (nHd_3.1)
  ixgca917499995v1_eg_gene - Ichneumon xanthorius (Ichneumon Wasp, reference) genes (iyIchXant1.1)
  iegca921293095v1rs_eg_gene - Ischnura elegans (Damselflies) - GCF_921293095.1 [RefSeq annotation] genes (ioIscEleg1.1)
  ipgca013358835v2vb_eg_gene - Ixodes persulcatus (Taiga tick, Iper-2018) - GCA_013358835.2 genes (GCA013358835v2)
  ipgca013358835v1_eg_gene - Ixodes persulcatus (Taiga tick, Iper-2018) genes (BIME_Iper_1.3)
  isise6_eg_gene - Ixodes scapularis (Black-legged tick, ISE6) genes (IscaI1)
  isgca016920785v2_eg_gene - Ixodes scapularis (Black-legged tick, PalLabHiFi) genes (ASM1692078v2)
  iscapularis_eg_gene - Ixodes scapularis (Black-legged tick, Wikel) genes (IscaW1)
  lggca023078275v1rs_eg_gene - Leguminivora glycinivorella (Soybean pod borer, SPB_JAAS2020) genes (LegGlyc_1.1)
  lsgca016086655v3rs_eg_gene - Lepeophtheirus salmonis (Salmon louse, Lsal2020) genes (UVic_Lsal_1.0)
  ldgca000500325v2_eg_gene - Leptinotarsa decemlineata (Colorado potato beetle, Imidocloprid resistant) genes (Ldec_2.0)
  ldeliense_eg_gene - Leptotrombidium deliense (Harvest mite, UoL-UT) genes (LdelU1)
  llgca917563855v2_eg_gene - Limnephilus lunatus (Caddisflies, reference) genes (iiLimLuna2.2)
  lmgca917880885v1_eg_gene - Limnephilus marmoratus (Caddisflies, reference) genes (iiLimMarm1.1)
  lrgca929108145v2_eg_gene - Limnephilus rhombicus (Caddisflies, reference) genes (iiLimRhom1.2)
  lfgca944474755v1_eg_gene - Limnoperna fortunei (Golden mussel, reference) genes (xbLimFort5.1)
  lpgca000517525v1_eg_gene - Limulus polyphemus (Atlantic horseshoe crab) genes (Limulus_polyphemus_2.1.2)
  lhgca000217595v1rs_eg_gene - Linepithema humile (Argentine ant) genes (Lhum_UMD_V04)
  llgca910592395v2_eg_gene - Lineus longissimus (Bootlace worm, reference) genes (tnLinLong1.2)
  lagca001039355v2_eg_gene - Lingula anatina (Lamp shell, Amm_Jpn) genes (LinAna2.0)
  ljgca032854445v1rs_eg_gene - Liolophura japonica (Chitons, JHLJ2023) - GCF_032854445.1 [RefSeq annotation] genes (CUHK_Ljap_v2)
  lloa_eg_gene - Loa loa (Eye worm, Cameroon SouthWest Province isolate) genes (Loa_loa_V3)
  lgigantea_eg_gene - Lottia gigantea (Owl limpet) genes (Lotgi1)
  lcuprina_eg_gene - Lucilia cuprina (Australian sheep blowfly, LS) genes (ASM118794v1)
  lcgca022045245v1rs_eg_gene - Lucilia cuprina (Australian sheep blowfly, Lc7/37) genes (ASM2204524v1)
  llongipalpis_eg_gene - Lutzomyia longipalpis (Sand fly, Jacobina) genes (LlonJ1)
  llgca024334085v1rs_eg_gene - Lutzomyia longipalpis (Sand fly, SR_M1_2022) genes (ASM2433408v1)
  lpgca015342785v2rs_eg_gene - Lytechinus pictus (Painted urchin, DCL-2020) genes (UCSD_Lpic_2.1)
  lvgca018143015v1_eg_gene - Lytechinus variegatus (Green sea urchin, NC3) genes (Lvar_3.0)
  magca933228815v1_eg_gene - Machimus atricapillus (Kite-tailed Robberfly, reference) genes (idMacAtri3.1)
  mngca015104395v2rs_eg_gene - Macrobrachium nipponense (Crustaceans, FS-2020) - GCF_015104395.2 [RefSeq annotation] genes (ASM1510439v2)
  mqgca028750875v1rs_eg_gene - Macrosteles quadrilineatus (Aster leafhopper, MER2022) genes (UCM_ALF_1.0)
  mggca963853765v1rs_eg_gene - Magallana gigas (Bivalves) - GCF_963853765.1 [RefSeq annotation] genes (xbMagGiga1.1)
  mggca030247185v2rs_eg_gene - Malaya genurostris (Mosquitos, Urasoe2022) genes (Malgen_1.1)
  msgca014839805v1rs_eg_gene - Manduca sexta (Tobacco hornworm, Smith_Timp_Sample1) genes (JHU_Msex_v1.0)
  mdestructor_eg_gene - Mayetiola destructor (Hessian fly, Kansas Great Plain) genes (Mdes_1.0)
  mrgca000220905v1rs_eg_gene - Megachile rotundata (Alfalfa leafcutting bee) genes (MROT_1.0)
  mscalaris_eg_gene - Megaselia scalaris (Coffin fly) genes (Msca1)
  msgca002803265v2rs_eg_gene - Melanaphis sacchari (Sugarcane aphid, LSU) genes (SCAv2.0)
  mcgca905220565v1_eg_gene - Melitaea cinxia (Glanville fritillary, reference) genes (ilMelCinx1.1)
  mmgca014805675v2_eg_gene - Mercenaria mercenaria (Hard clam (quahog), YKG-2019) genes (ASM1480567v1.1)
  magca030272935v1cm_eg_gene - Microctonus aethiopoides (Parasitoid wasp, French) genes (UoO_Maeth_FR)
  magca030347275v1cm_eg_gene - Microctonus aethiopoides (Parasitoid wasp, Irish) genes (UoO_Maeth_IR)
  magca030272655v1cm_eg_gene - Microctonus aethiopoides (Parasitoid wasp, Moroccan) genes (UoO_Maeth_MO)
  mhgca030347285v1cm_eg_gene - Microctonus hyperodae (Parasitoid wasp, Lincoln) genes (UoO_Mhyp)
  mdgca026212275v2rs_eg_gene - Microplitis demolitor (Parasitoid wasp, Queensland-Clemson2020A) genes (iyMicDemo2.1a)
  mmgca029852145v1rs_eg_gene - Microplitis mediator (Endoparasitoid wasp, UGA2020A) genes (iyMicMedi2.1)
  mygca002113885v2_eg_gene - Mizuhopecten yessoensis (Yesso scallop, PY_sf001) genes (ASM211388v2)
  mleidyi_eg_gene - Mnemiopsis leidyi (Warty comb jelly) genes (MneLei_Aug2011)
  mpgca013373865v2_eg_gene - Monomorium pharaonis (Pharaoh ant, MP-MQ-018) genes (ASM1337386v2)
  mdomestica_eg_gene - Musca domestica (House fly, aabys) genes (MdomA1)
  magca026914265v1rs_eg_gene - Mya arenaria (Soft-shell clam, MELC-2E11) genes (ASM2691426v1)
  mtgca943737955v1_eg_gene - Myopa tessellatipennis (Thick-headed flies, reference) genes (idMyoTess1.1)
  mcgca021869535v1rs_eg_gene - Mytilus californianus (California mussel, M0D057914Y) genes (xbMytCali1.0.p)
  nvitripennis_eg_gene - Nasonia vitripennis (Jewel wasp, AsymCx) genes (Nvit_psr_1.1)
  namericanus_eg_gene - Necator americanus (New World hookworm, N. amaericanus Hunan isolate) genes (N_americanus_v1)
  nvectensis_eg_gene - Nematostella vectensis (Starlet sea anemone, CH2 x CH6) genes (ASM20922v1)
  nlgca021901455v1rs_eg_gene - Neodiprion lecontei (Redheaded pine sawfly, iyNeoLeco1) genes (iyNeoLeco1.1)
  npgca021155775v1rs_eg_gene - Neodiprion pinetum (White pine sawfly, iyNeoPine1) genes (iyNeoPine1.1)
  nlgca014356525v1rs_eg_gene - Nilaparvata lugens (Brown planthopper, BPH) genes (ASM1435652v1)
  obgca001194135v2rs_eg_gene - Octopus bimaculoides (California two-spot octopus, UCB-OBI-ISO-001) genes (ASM119413v2)
  osgca006345805v1_eg_gene - Octopus sinensis (East Asian common octopus) genes (ASM634580v1)
  ovolvulus_eg_gene - Onchocerca volvulus (Nematode, O. volvulus Cameroon isolate) genes (ASM49940v2)
  otgca000648695v2_eg_gene - Onthophagus taurus (Dung beetle) genes (Otau_2.0)
  obgca003672135v1_eg_gene - Ooceraea biroi (Clonal raider ant, clonal line C1) genes (Obir_v5.4)
  ongca028296485v1rs_eg_gene - Oppia nitens (Oribatid soil mite, AA-2021) genes (nextdenovo_longstitch_racon4_pilon3)
  ofgca002042975v1_eg_gene - Orbicella faveolata (Mountainous star coral, FL) genes (ofav_dov_v1)
  ocincta_eg_gene - Orchesella cincta (Springtail) genes (ASM171814v1)
  oagca000612105v2_eg_gene - Orussus abietinus (Parasitic wood wasp, OABI.00-Male) genes (Oabi_2.0)
  oegca023158985v1rs_eg_gene - Ostrea edulis (European flat oyster, OE_ROSLIN_2020) genes (OEROSLIN_1.1)
  ofgca903813345v1_eg_gene - Owenia fusiformis (Segmented worms) genes (Owenia_assembly_annotated)
  pcgca014898815v1rs_eg_gene - Panonychus citri (Citrus red mite, SS) genes (ASM1489881v1)
  pmgca019649055v1rs_eg_gene - Paramacrobiotus metropolitanus (Water bear tardigrade, TYO) genes (Prichtersi_v1.0)
  ptgca000365465v3_eg_gene - Parasteatoda tepidariorum (Common house spider, Goettingen) genes (Ptep_3.0)
  ppgca917208275v1_eg_gene - Patella pellucida (Blue-rayed limpet, reference) genes (xgPatPell1.1)
  pvgca932274485v1_eg_gene - Patella vulgata (Common limpet, reference) genes (xgPatVulg1.1)
  pmgca015706575v1_eg_gene - Patiria miniata (Bat star starfish, m_02_andy) genes (Pmin_3.0)
  pmgca902652985v1rs_eg_gene - Pecten maximus (Great Scallop) genes (xPecMax1.1)
  pggca024362695v1rs_eg_gene - Pectinophora gossypiella (Pink bollworm) genes (ilPecGoss1.1)
  phumanus_eg_gene - Pediculus humanus corporis (Human body louse, USDA) genes (PhumU2)
  pcgca019202785v2rs_eg_gene - Penaeus chinensis (Fleshy prawn) genes (ASM1920278v2)
  pjgca017312705v1_eg_gene - Penaeus japonicus (Kuruma shrimp, Ginoza2017) genes (Mj_TUMSAT_v1.0)
  pmgca015228065v1_eg_gene - Penaeus monodon (Black tiger shrimp, SGIC_2016) genes (NSTDA_Pmon_1)
  pvgca003789085v1_eg_gene - Penaeus vannamei (Pacific white shrimp) genes (ASM378908v1)
  pagca947086385v1rs_eg_gene - Phlebotomus argentipes (Sand fly) genes (Phlebotomus_argentipes_genome_assembly)
  ppapatasi_eg_gene - Phlebotomus papatasi (Sand fly, Israel) genes (PpapI1)
  ppgca024763615v2rs_eg_gene - Phlebotomus papatasi (Sand fly, M1) genes (Ppap_2.0)
  ppgca918844115v2_eg_gene - Phlebotomus perniciosus (Murcia) genes (pperniciosus_asm_v2.0)
  pdgca026936325v1cm_eg_gene - Platynereis dumerilii (Dumeril's clam worm, lab) - GCA_026936325.1 [Community annotation] genes (EMBL_pdum_1.0)
  pigca027563975v1rs_eg_gene - Plodia interpunctella (Indianmeal moth, USDA-ARS_2022_Savannah) genes (ilPloInte3.1)
  pdgca003704095v1_eg_gene - Pocillopora damicornis (Cauliflower coral, RSMAS) genes (ASM370409v1)
  pbgca000187915v1rs_eg_gene - Pogonomyrmex barbatus (Red harvester ant) genes (Pbar_UMD_V03)
  pcgca001313835v1rs_eg_gene - Polistes canadensis (Red paper wasp, GaletaPanama2010) genes (ASM131383v1)
  pdgca001465965v1rs_eg_gene - Polistes dominula (European paper wasp, PdomPennStateAug2009) genes (Pdom_r1.2)
  pfgca010416935v1rs_eg_gene - Polistes fuscatus (Common paper wasp, 324) genes (CU_Pfus_HIC)
  ppgca011947565v2_eg_gene - Pollicipes pollicipes (Goose neck barnacle, AB1234) genes (Ppol_2)
  pcgca003073045v1_eg_gene - Pomacea canaliculata (Apple snail, SZHN2017) genes (ASM307304v1)
  plgca012934845v2gb_eg_gene - Pomphorhynchus laevis (Thorny-headed worm, GPI110) genes (ASM1293484v2)
  ptgca017591435v1_eg_gene - Portunus trituberculatus (Swimming crab, SZX2019) genes (ASM1759143v1)
  pcgca000485595v2_eg_gene - Priapulus caudatus (Penis worm) genes (Priapulus_caudatus-5.0.1)
  ppacificus_eg_gene - Pristionchus pacificus (Nematode, PS312) genes (El_Paco)
  pcgca020424385v2_eg_gene - Procambarus clarkii (Red swamp crayfish, Jiangsu) genes (ASM2042438v2)
  rpgca013731165v1_eg_gene - Rhagoletis pomonella (Apple magot fly, Grant_MI) genes (Rhpom_1.0)
  rmgca013339725v1_eg_gene - Rhipicephalus microplus (Southern cattle tick, Rmic-2018) genes (ASM1333972v1)
  rsgca013339695v2rs_eg_gene - Rhipicephalus sanguineus (Brown dog tick, Rsan-2018) genes (BIME_Rsan_1.4)
  rprolixus_eg_gene - Rhodnius prolixus (Kissing bug, CDC) - GCA_000181055.3 genes (RproC3)
  rmgca003676215v3_eg_gene - Rhopalosiphum maidis (Corn leaf aphid, BTI-1) genes (ASM367621v3)
  skgca000003605v1_eg_gene - Saccoglossus kowalevskii (Acorn worm) genes (Skow_1.1)
  sscabiei_eg_gene - Sarcoptes scabiei (Itch mite, SSS_KF_BRIS2020) genes (ASM1459567v1)
  sagca021461395v2rs_eg_gene - Schistocerca americana (American grasshopper, TAMUIC-IGC-003095) genes (iqSchAmer2.1)
  scgca023864275v2rs_eg_gene - Schistocerca cancellata (South American locust, TAMUIC-IGC-003103) genes (iqSchCanc2.1)
  sggca023897955v2rs_eg_gene - Schistocerca gregaria (Grasshoppers, iqSchGreg1) genes (iqSchGreg1.2)
  sngca023898315v2rs_eg_gene - Schistocerca nitens (Vagrant locust, TAMUIC-IGC-003100) genes (iqSchNite1.1)
  spgca021461385v2rs_eg_gene - Schistocerca piceifrons (Central American locust, TAMUIC-IGC-003096) genes (iqSchPice1.1)
  ssgca023864345v3rs_eg_gene - Schistocerca serialis cubense (Grasshoppers, TAMUIC-IGC-003099) genes (iqSchSeri2.2)
  shgca000699445v3rs_eg_gene - Schistosoma haematobium (Flatworms) - GCF_000699445.3 [RefSeq annotation] genes (UoM_Shae.V3)
  shgca000699445v2rs_eg_gene - Schistosoma haematobium (Urinary blood fluke) genes (SchHae_2.0)
  smansoni_eg_gene - Schistosoma mansoni (Flatworm) genes (Smansoni_v7)
  sfgca003268045v1_eg_gene - Sipha flava (Yellow sugarcane aphid, LNK) genes (YSA_version1)
  sogca002938485v2rs_eg_gene - Sitophilus oryzae (Rice weevil) genes (Soryzae_2.0)
  sinvicta_eg_gene - Solenopsis invicta (Red fire ant, M01_SB) genes (UNIL_Sinv_3.0)
  sfgca023101765v3rs_eg_gene - Spodoptera frugiperda (Fall armyworm, SF20-4) genes (AGI-APGP_CSIRO_Sfru_2.0)
  sdgca010614865v2rs_eg_gene - Stegodyphus dumicola (Social spider, AA2019) genes (ASM1061486v2)
  smimosarum_eg_gene - Stegodyphus mimosarum (African social velvet spider) genes (Stegodyphus_mimosarum_v1)
  scalcitrans_eg_gene - Stomoxys calcitrans (Stable fly, USDA) genes (ScalU1)
  smaritima_eg_gene - Strigamia maritima (Soil centipede) genes (Smar1)
  spurpuratus_eg_gene - Strongylocentrotus purpuratus (Purple sea urchin, Spur 01) genes (Spur_5.0)
  sratti_eg_gene - Strongyloides ratti (Threadworm) genes (S_ratti_ED321_v5_0_4)
  spgca002571385v1_eg_gene - Stylophora pistillata (Hood coral, CSM Monaco) genes (Stylophora_pistillata_v1)
  tdalmanni_eg_gene - Teleopsis dalmanni (Malaysian stalk-eyed fly, 2A) genes (ASM223713v2)
  turticae_eg_gene - Tetranychus urticae (Two-spotted spider mite) genes (ASM23943v1)
  tkitauei_eg_gene - Thelohanellus kitauei (Myxozoan endoparasite) genes (ASM82789v1)
  tpgca012932325v1rs_eg_gene - Thrips palmi (Melon Thrips, BJ-2018) genes (TpBJ_2018v1)
  tcgca007210705_eg_gene - Tigriopus californicus (Copepod, San Diego) genes (Tcal_SD_v2.1)
  tygca030247195v1rs_eg_gene - Topomyia yanbarensis (Mosquitos, Yona2022) genes (ASM3024719v1)
  trgca029784135v1rs_eg_gene - Toxorhynchites rutilus septentrionalis (Elephant mosquito, SRP) genes (ASM2978413v1)
  tvgca011764245_eg_gene - Trialeurodes vaporariorum (Greenhouse whitefly, IVF) genes (ASM1176424v1)
  tcastaneum_eg_gene - Tribolium castaneum (Red flour beetle, Georgia GA2) genes (Tcas5.2)
  tmgca015345945v1rs_eg_gene - Tribolium madens (Black flour beetle, multiple individuals) genes (Tmad_KSU_1.1)
  tspiralis_eg_gene - Trichinella spiralis (Pork worm, ISS_195) genes (Tspiralis1)
  tpgca000599845v3_eg_gene - Trichogramma pretiosum (Parasitoid wasp, Unisexual culture from Peru) genes (Tpre_2.0)
  tadhaerens_eg_gene - Trichoplax adhaerens (Placozoa, Grell-BS-1999) genes (ASM15027v1)
  tmuris_eg_gene - Trichuris muris (Nematode) genes (TMUE3.0)
  udgca026930045v1rs_eg_gene - Uloborus diversus (Orb Weaver, 005) genes (Udiv.v.3.1)
  ulgca029784155v1rs_eg_gene - Uranotaenia lowii (Mosquitos, MFRU-FL) genes (ASM2978415v1)
  vdgca002443255_eg_gene - Varroa destructor (Honeybee mite) genes (Vdes_3.0)
  vjgca002532875v1rs_eg_gene - Varroa jacobsoni (Varroa mite, VJ856) genes (vjacob_1.0)
  vcgca019457755v1rs_eg_gene - Venturia canescens (Endoparasitoid wasp, UGA) genes (ASM1945775v1)
  wsgca029784165v1rs_eg_gene - Wyeomyia smithii (Pitcher plant Mosquito, HCP4-BCI-WySm-NY-G18) genes (ASM2978416v1)
  zcgca012273895v2rs_eg_gene - Zerene cesonia (Southern Dogface) genes (Zerene_cesonia_1.1)
  zcgca028554725v2rs_eg_gene - Zeugodacus cucurbitae (Melon fly, PBARC_wt_2022May) genes (idZeuCucr1.2)
  znevadensis_eg_gene - Zootermopsis nevadensis (Nevada dampwood termite) genes (ZooNev1.0)

__________________________________________________________
### gene_tree_fetcher.py
__________________________________________________________
```
Basic usage:

python ensembl_gene_tree.py species_list.txt

To force a specific API (bypassing auto-detection):

python genetree_builder/ensembl_gene_tree_v0-6.py species_list.txt --force Metazoa
```
```
#!/bin/bash

#SBATCH --job-name=TREES     # Set the job name
#SBATCH --nodes 1
#SBATCH --tasks-per-node 1
#SBATCH --cpus-per-task 1
#SBATCH --mem 64gb
#SBATCH --time 72:00:00

cd /scratch/ffeltus/emily_ensembl_20250522/trees 
python genetree_builder/ensembl_gene_tree.py species_ensembl-metazoa.txt 
```
### EXAMPLE OUTPUT:
==================================================
Processing species: Daphnia pulex
Using API: Metazoa
Dataset: dpgca021134715v1rs_eg_gene
==================================================
Gene list file Daphnia_pulex_protein-coding_genes.csv not found for Daphnia pulex
Fetching genes from BioMart...
Fetching genes from BioMart using dataset: dpgca021134715v1rs_eg_gene
Fetched 15295 protein-coding genes
CSV file 'Daphnia_pulex_protein-coding_genes.csv' has been created with 15295 genes.
CSV columns: ['gene_id', 'gene_symbol', 'ensembl_id']
Row 1: {'gene_id': 'LOC124192653', 'gene_symbol': 'Unknown', 'ensembl_id': 'LOC124192653'}
Row 2: {'gene_id': 'LOC124188803', 'gene_symbol': 'Unknown', 'ensembl_id': 'LOC124188803'}
Row 3: {'gene_id': 'LOC124193278', 'gene_symbol': 'Unknown', 'ensembl_id': 'LOC124193278'}
Row 4: {'gene_id': 'LOC124193500', 'gene_symbol': 'Unknown', 'ensembl_id': 'LOC124193500'}
Row 5: {'gene_id': 'LOC124209624', 'gene_symbol': 'Unknown', 'ensembl_id': 'LOC124209624'}
Total Daphnia pulex protein-coding genes: 15295
Starting from gene number: 1

Processing batch 1 of 153

__________________________________________________________

### DEPRECTATED: fetch_ensembl_genes.py: Fetches gene names from the appropriate BIOMART API. SCRIPT IS MISSING!
__________________________________________________________
```
# For standard Ensembl
python genetree_builder/genetree_builder/efetch_ensembl_genes.py species_list.txt

# For Ensembl Metazoa
python genetree_builder/genetree_bulder/efetch_ensembl_genes.py species_list.txt --metazoa

# To list available datasets (helpful for troubleshooting)
python genetree_builder/genetree_bulder/efetch_ensembl_genes.py --list --metazoa

# Interactive mode
python genetree_builder/genetree_bulder/efetch_ensembl_genes.py --interactive --metazoa
```

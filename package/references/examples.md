# Verified example calls (question → URL)

`BASE` = `https://visualization.osdr.nasa.gov/biodata/api`. All URLs verified live; row counts are approximate and grow over time.
Use these as templates: copy the closest one and change the values.

## Discovery by mission / project

**Q:** List every RR-1 (Rodent Research 1) assay with its technology and tissue.

```
BASE/v2/query/assays/?investigation.study.comment.Project%20Identifier=/RR-1([^\d]|$)|RR1([^\d]|$)/&investigation.study%20assays.study%20assay%20technology%20type&study.characteristics.material%20type&format=json.records
```
→ 80 rows, 25 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, investigation.study.comment.project identifier, study.characteristics.material type

**Q:** Which Inspiration4 datasets exist, with assay technology and material type?

```
BASE/v2/query/assays/?investigation.study.comment.Project%20Identifier=/Inspiration/&investigation.study%20assays.study%20assay%20technology%20type&study.characteristics.material%20type&format=json.records
```
→ 29 rows, 10 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, investigation.study.comment.project identifier, study.characteristics.material type

**Q:** Which datasets are hindlimb-unloading ground studies?

```
BASE/v2/query/datasets/?investigation.study.comment.Project%20Identifier=/Hindlimb_Unloading/&format=json.records
```
→ 41 rows, 41 datasets; cols: id.accession, investigation.study.comment.project identifier

**Q:** All Rodent Research datasets (any RR-# mission) and their mission label — anchored so 'Irradiation' is excluded.

```
BASE/v2/query/datasets/?investigation.study.comment.Project%20Identifier=/^RR-?\d|^RRRM/&format=json.records
```
→ 130 rows, 130 datasets; cols: id.accession, investigation.study.comment.project identifier

**Q:** RR-1 datasets that a project-identifier filter misses (null identifier) — cross-check by mission name.

```
BASE/v2/query/datasets/?investigation.study.comment.mission%20name=/SpaceX-4/&investigation.study.comment.Project%20Identifier&format=json.records
```
→ 31 rows, 31 datasets; cols: id.accession, investigation.study.comment.mission name, investigation.study.comment.project identifier

**Q:** Mouse RNA-seq datasets from spaceflight studies only (excludes ground analogs), with mission.

```
BASE/v2/query/assays/?study.characteristics.organism=/musculus/&investigation.study%20assays.study%20assay%20technology%20type=/rna-seq/&investigation.study.comment.project%20type=/spaceflight/&investigation.study.comment.Project%20Identifier&investigation.study.comment.mission%20name&format=json.records
```
→ 80 rows, 78 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, investigation.study.comment.mission name, investigation.study.comment.project identifier, investigation.study.comment.project type …

## Discovery by technology

**Q:** All mass-spectrometry assays and the material analysed.

```
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20technology%20type=/mass%20spectrometry/&study.characteristics.material%20type&format=json.records
```
→ 85 rows, 48 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, study.characteristics.material type

**Q:** All tonometry datasets.

```
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20technology%20type=/tonometry/&format=json.records
```
→ 2 rows, 2 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type

**Q:** Immunostaining or microscopy assays on eye tissue.

```
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20technology%20type=/immunostaining|microscopy/&study.characteristics.material%20type=/eye|retina|optic/&format=json.records
```
→ 9 rows, 3 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, study.characteristics.material type

**Q:** Which datasets have 16S or ITS amplicon differential-abundance files, with download URLs?

```
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20technology%20type=/16S|ITS/&file.data%20type=/differential%20abundance/&file.remote_url&format=json.records
```
→ 6 rows, 1 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, file.data type, file.file name, file.remote_url

**Q:** Amplicon (16S/ITS) datasets where a plant was the host organism (organism itself is 'Microbiota').

```
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20technology%20type=/16S|ITS/&study.characteristics.host%20organism=/lactuca|brassica|capsicum|solanum|raphanus|pisum|triticum/&study.characteristics.host%20strain&study.characteristics.organism%20part&format=json.records
```
→ 50 rows, 11 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, study.characteristics.host organism, study.characteristics.host strain, study.characteristics.organism part

**Q:** All datasets with behavioural data (measurement type Behavior).

```
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20measurement%20type=/behavior/&investigation.study%20assays.study%20assay%20technology%20type&format=json.records
```
→ 28 rows, 12 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay measurement type, investigation.study assays.study assay technology type

**Q:** Datasets with eye or retina tissue, any technology.

```
BASE/v2/query/assays/?study.characteristics.material%20type=/retina|eye|ocular|optic|cornea|lens|choroid|sclera/&investigation.study%20assays.study%20assay%20technology%20type&format=json.records
```
→ 49 rows, 20 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, study.characteristics.material type

**Q:** Single-cell RNA-seq datasets and organism.

```
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20technology%20type=/single-cell/&study.characteristics.organism&format=json.records
```
→ 39 rows, 33 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, study.characteristics.organism

## Discovery by organism

**Q:** All mouse bulk RNA-seq assays.

```
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20technology%20type=/rna-seq/&study.characteristics.organism=/musculus/&format=json.records
```
→ 113 rows, 111 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, study.characteristics.organism

**Q:** All Arabidopsis microarray datasets (meta-analysis corpus).

```
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20technology%20type=/microarray/&study.characteristics.organism=/arabidopsis/&format=json.records
```
→ 23 rows, 23 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, study.characteristics.organism

**Q:** Drosophila RNA-seq or microarray datasets that have a differential-expression file.

```
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20technology%20type=/rna-seq|microarray/&file.data%20type=/differential%20expression%20table/&study.characteristics.organism=/Drosophila/&format=json.records
```
→ 22 rows, 13 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, study.characteristics.organism, file.data type, file.file name

**Q:** Human datasets and their technologies.

```
BASE/v2/query/assays/?study.characteristics.organism=/sapiens/&investigation.study%20assays.study%20assay%20technology%20type&format=json.records
```
→ 142 rows, 114 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, study.characteristics.organism

## Discovery by tissue

**Q:** Kidney samples anywhere in OSDR, with organism and mission.

```
BASE/v2/query/samples/?study.characteristics.material%20type=/kidney/&study.characteristics.organism&investigation.study.comment.Project%20Identifier&format=json.records
```
→ 601 rows, 9 datasets; cols: id.accession, id.assay name, id.sample name, investigation.study.comment.project identifier, study.characteristics.material type, study.characteristics.organism

**Q:** Leg-muscle RNA-seq assays (tibialis, soleus, gastrocnemius, quadriceps) with spaceflight factor.

```
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20technology%20type=/rna-seq/&study.characteristics.material%20type=/tibialis|soleus|gastrocnemius|quadriceps/&study.factor%20value.spaceflight&format=json.records
```
→ 40 rows, 23 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, study.characteristics.material type, study.factor value.spaceflight

**Q:** Rodent and human leg-muscle assays of any technology.

```
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20technology%20type&study.characteristics.material%20type=/tibialis|soleus|gastrocnemius|quadriceps|digitorum|vastus/&study.characteristics.organism=/musculus|rattus|sapiens/&format=json.records
```
→ 90 rows, 47 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, study.characteristics.material type, study.characteristics.organism

**Q:** Spaceflight fecal-sample assays with the spaceflight factor value.

```
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20technology%20type&study.characteristics.material%20type=/feces/&study.factor%20value.spaceflight&format=json.records
```
→ 47 rows, 10 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, study.characteristics.material type, study.factor value.spaceflight

## Discovery by factor

**Q:** Datasets where the spaceflight factor is Space Flight, restricted to rats.

```
BASE/v2/query/datasets/?study.factor%20value.spaceflight=/space%20flight/&study.characteristics.organism=/rattus/&format=json.records
```
→ 7 rows, 7 datasets; cols: id.accession, study.characteristics.organism, study.factor value.spaceflight

**Q:** Ground irradiation studies with the absorbed dose as a column.

```
BASE/v2/query/assays/?investigation.study.comment.Project%20Identifier=/Irradiation/&study.factor%20value.absorbed%20radiation%20dose&format=json.records
```
→ 391 rows, 110 datasets; cols: id.accession, id.assay name, investigation.study.comment.project identifier, study.factor value.absorbed radiation dose

## Subject characteristics (sex / strain / age)

**Q:** Female mouse liver samples (characteristic first).

```
BASE/v2/query/samples/?study.characteristics.organism=/musculus/&study.characteristics.material%20type=/liver/&study.characteristics.sex=/female/&format=json.records
```
→ 820 rows, 15 datasets; cols: id.accession, id.assay name, id.sample name, study.characteristics.material type, study.characteristics.organism, study.characteristics.sex

**Q:** Same question, factor fallback (run only if the characteristic query returns 0 rows).

```
BASE/v2/query/samples/?study.characteristics.organism=/musculus/&study.characteristics.material%20type=/liver/&study.factor%20value.sex=/female/&format=json.records
```
→ 0 rows

**Q:** C57BL/6 mouse RNA-seq samples with sex and strain columns.

```
BASE/v2/query/samples/?investigation.study%20assays.study%20assay%20technology%20type=/rna-seq/&study.characteristics.organism=/musculus/&study.characteristics.strain=/C57BL/&study.characteristics.sex&format=json.records
```
→ 2528 rows, 84 datasets; cols: id.accession, id.assay name, id.sample name, investigation.study assays.study assay technology type, study.characteristics.organism, study.characteristics.sex …

**Q:** Which characteristic and factor fields does OSD-104 use (field discovery)?

```
BASE/v2/query/assays/?id.accession=OSD-104&study.characteristics&study.factor%20value&format=json.records
```
→ 4 rows, 1 datasets; cols: id.accession, id.assay name, study.characteristics.age at launch, study.characteristics.animal source, study.characteristics.launch mission, study.characteristics.material type …

**Q:** Every distinct strain value used in mouse studies (value discovery).

```
BASE/v2/query/datasets/?study.characteristics.organism=/musculus/&study.characteristics.strain=/./&format=json.records
```
→ 248 rows, 233 datasets; cols: id.accession, study.characteristics.organism, study.characteristics.strain

**Q:** Mouse samples with an 'age at launch' characteristic.

```
BASE/v2/query/samples/?study.characteristics.organism=/musculus/&study.characteristics.age%20at%20launch=/./&format=json.records
```
→ 5267 rows, 105 datasets; cols: id.accession, id.assay name, id.sample name, study.characteristics.age at launch, study.characteristics.organism

## Sample-level metadata

**Q:** All mouse RNA-seq samples with every characteristic column.

```
BASE/v2/query/samples/?investigation.study%20assays.study%20assay%20technology%20type=/rna-seq/&study.characteristics.organism=/musculus/&study.source%20name&study.characteristics&format=json.records
```
→ 3501 rows, 111 datasets; cols: id.accession, id.assay name, id.sample name, investigation.study assays.study assay technology type, study.characteristics.age, study.characteristics.age at euthanasia …

**Q:** All mouse RNA-seq samples with every factor-value column.

```
BASE/v2/query/samples/?investigation.study%20assays.study%20assay%20technology%20type=/rna-seq/&study.characteristics.organism=/musculus/&study.source%20name&study.factor%20value&format=json.records
```
→ 3501 rows, 111 datasets; cols: id.accession, id.assay name, id.sample name, investigation.study assays.study assay technology type, study.characteristics.organism, study.factor value.absorbed radiation dose …

**Q:** Mouse RNA-seq assay parameter values (library prep, instrument…).

```
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20technology%20type=/rna-seq/&study.characteristics.organism=/musculus/&assay.parameter%20value&format=json.records
```
→ 3486 rows, 111 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, study.characteristics.organism, assay.parameter value.aligned sequence data, assay.parameter value.aligned sequence data/alignment logs …

**Q:** Material type, organism and technology for every sample of OSD-104 (24 rows = samples).

```
BASE/v2/query/metadata/?id.accession=OSD-104&investigation.study%20assays.study%20assay%20technology%20type&study.characteristics.material%20type&study.characteristics.organism&format=json.records
```
→ 24 rows, 1 datasets; cols: id.accession, id.assay name, id.sample name, investigation.study assays.study assay technology type, study.characteristics.material type, study.characteristics.organism

**Q:** Same fields for OSD-104 at assay granularity (2 rows = assays).

```
BASE/v2/query/assays/?id.accession=OSD-104&investigation.study%20assays.study%20assay%20technology%20type&study.characteristics.material%20type&study.characteristics.organism&format=json.records
```
→ 2 rows, 1 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay technology type, study.characteristics.material type, study.characteristics.organism

## Known accession (REST tree)

**Q:** Dataset-level metadata for OSD-557.

```
BASE/v2/dataset/OSD-557/
```
→ JSON tree

**Q:** All assays in OSD-557.

```
BASE/v2/dataset/OSD-557/assays/
```
→ JSON tree

**Q:** All files in OSD-557 with download URLs.

```
BASE/v2/dataset/OSD-557/files/
```
→ JSON tree

**Q:** Samples and factor values for one named OSD-557 assay.

```
BASE/v2/query/metadata/?id.accession=OSD-557&id.assay%20name=OSD-557_bone-microstructure_micro-computed-tomography_SkyScan_1272_desktop_micro-CT_system&study.factor%20value&format=json.records
```
→ 12 rows, 1 datasets; cols: id.accession, id.assay name, id.sample name, study.factor value.spaceflight

## Files

**Q:** Processed RNA-seq files for OSD-515 with their subcategory (step A before pulling data).

```
BASE/v2/query/assays/?id.accession=OSD-515&file.filename=/differential_expression|Counts|contrasts/&file.subcategory&format=json.records
```
→ 10 rows, 1 datasets; cols: id.accession, id.assay name, file.filename, file.subcategory

**Q:** Differential-expression file download URL for OSD-168.

```
BASE/v2/query/assays/?id.accession=OSD-168&file.filename=/differential_expression/&file.remote_url&format=json.records
```
→ 2 rows, 1 datasets; cols: id.accession, id.assay name, file.filename, file.remote_url

**Q:** Which GeneLab-processed files does OSD-572 have (then drop subcategory 'Merged Sequence Data').

```
BASE/v2/query/assays/?id.accession=OSD-572&file.category=/genelab%20processed/&file.subcategory&file.filename&format=json.records
```
→ 4095 rows, 1 datasets; cols: id.accession, id.assay name, file.category, file.filename, file.subcategory

**Q:** Per-accession check for DE and DM tables (narrow-then-expand step 2).

```
BASE/v2/query/assays/?id.accession=OSD-47&file.filename=/differential_expression|differential_methylation/&format=json.records
```
→ 4 rows, 1 datasets; cols: id.accession, id.assay name, file.filename

**Q:** All TIFF or PNG image files in OSDR with their measurement type.

```
BASE/v2/query/assays/?investigation.study%20assays.study%20assay%20measurement%20type&file.remote_url=/tiff|png/&format=json.records
```
→ 96 rows, 5 datasets; cols: id.accession, id.assay name, investigation.study assays.study assay measurement type, file.remote_url

## Data-file contents

**Q:** OSD-515 RSEM raw counts table.

```
BASE/v2/query/data/?id=OSD-515&file.filename=GLDS-515_rna_seq_RSEM_Unnormalized_Counts_GLbulkRNAseq.csv&column.*&format=csv
```
→ 57278 data rows (csv)

**Q:** OSD-515 contrasts (learn exact group names).

```
BASE/v2/query/data/?id=OSD-515&file.filename=/contrasts_GLbulkRNAseq/&format=json.records
```
→ 2 rows; cols: OSD-515/OSD-515_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/index, OSD-515/OSD-515_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/(Ground Control)v(Space Flight), OSD-515/OSD-515_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/(Ground Control)v(Vivarium Control), OSD-515/OSD-515_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/(Space Flight)v(Vivarium Control), OSD-515/OSD-515_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/(Space Flight)v(Ground Control), OSD-515/OSD-515_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/(Vivarium Control)v(Ground Control) …

**Q:** OSD-515 genes with adjusted p ≤ 0.05 for Space Flight vs Ground Control (symbol, log2FC, adj p).

```
BASE/v2/query/data/?id=OSD-515&file.filename=GLDS-515_rna_seq_differential_expression_GLbulkRNAseq.csv&column.SYMBOL&column.Log2fc_(Space%20Flight)v(Ground%20Control)&column.Adj.p.value_(Space%20Flight)v(Ground%20Control)%3C=0.05&format=json.records
```
→ 3947 rows; cols: OSD-515/OSD-515_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/ENSEMBL, OSD-515/OSD-515_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/SYMBOL, OSD-515/OSD-515_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/Log2fc_(Space Flight)v(Ground Control), OSD-515/OSD-515_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/Adj.p.value_(Space Flight)v(Ground Control)

**Q:** Same, additionally up-regulated (log2FC ≥ 1), all columns.

```
BASE/v2/query/data/?id=OSD-515&file.filename=GLDS-515_rna_seq_differential_expression_GLbulkRNAseq.csv&column.Adj.p.value_(Space%20Flight)v(Ground%20Control)%3C=0.05&column.Log2fc_(Space%20Flight)v(Ground%20Control)%3E=1&column.*&format=csv
```
→ 2066 data rows (csv)

**Q:** OSD-48 contrasts — a two-factor study with no plain flight-vs-ground contrast.

```
BASE/v2/query/data/?id=OSD-48&file.filename=/contrasts_GLbulkRNAseq/&format=json.records
```
→ 2 rows; cols: OSD-48/OSD-48_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/index, OSD-48/OSD-48_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/(Ground Control & Carcass)v(Ground Control & Upon euthanasia), OSD-48/OSD-48_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/(Ground Control & Carcass)v(Space Flight & Carcass), OSD-48/OSD-48_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/(Ground Control & Carcass)v(Space Flight & Upon euthanasia), OSD-48/OSD-48_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/(Ground Control & Upon euthanasia)v(Space Flight & Carcass), OSD-48/OSD-48_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/(Ground Control & Upon euthanasia)v(Space Flight & Upon euthanasia) …

**Q:** OSD-48 flight vs ground (carcass dissection) DE genes, adj p ≤ 0.05; note %26 for '&'.

```
BASE/v2/query/data/?id=OSD-48&file.filename=GLDS-48_rna_seq_differential_expression_GLbulkRNAseq.csv&column.SYMBOL&column.Log2fc_(Space%20Flight%20%26%20Carcass)v(Ground%20Control%20%26%20Carcass)&column.Adj.p.value_(Space%20Flight%20%26%20Carcass)v(Ground%20Control%20%26%20Carcass)%3C=0.05&format=json.records
```
→ 635 rows; cols: OSD-48/OSD-48_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/ENSEMBL, OSD-48/OSD-48_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/SYMBOL, OSD-48/OSD-48_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/Log2fc_(Space Flight & Carcass)v(Ground Control & Carcass), OSD-48/OSD-48_transcription-profiling_rna-sequencing-(rna-seq)_Illumina/Adj.p.value_(Space Flight & Carcass)v(Ground Control & Carcass)

**Q:** OSD-267 16S ANCOM-BC1 differential-abundance table.

```
BASE/v2/query/data/?id=OSD-267&file.filename=/ancombc1_differential_abundance_16S_GLAmpSeq\.csv/&format=csv
```
→ 134 data rows (csv)

**Q:** Legacy microarray DE table without the _GL token (OSD-1); groups combine two factors with ' & ' (encode as %26).

```
BASE/v2/query/data/?id=OSD-1&file.filename=/differential_expression\.csv/&column.SYMBOL&column.Adj.p.value_(Space%20Flight%20%26%20uninfected)v(Ground%20Control%20%26%20uninfected)%3C=0.9&format=json.records
```
→ 95 rows; cols: OSD-1/OSD-1_transcription-profiling_dna-microarray_Affymetrix/ENSEMBL, OSD-1/OSD-1_transcription-profiling_dna-microarray_Affymetrix/SYMBOL, OSD-1/OSD-1_transcription-profiling_dna-microarray_Affymetrix/Adj.p.value_(Space Flight & uninfected)v(Ground Control & uninfected)

## Cross-dataset assembly

**Q:** Set A for intersection: datasets with a differential-expression file.

```
BASE/v2/query/datasets/?file.data%20type=/differential%20expression%20table/&format=json.records
```
→ 420 rows, 244 datasets; cols: id.accession, file.data type, file.file name

**Q:** Set B for intersection: datasets with a bisulfite / methylation assay.

```
BASE/v2/query/datasets/?investigation.study%20assays.study%20assay%20technology%20type=/bisulfite|methylation/&format=json.records
```
→ 26 rows, 21 datasets; cols: id.accession, investigation.study assays.study assay technology type

**Q:** Subjects shared by OSD-102 and OSD-104 (subject ID = project identifier | source name).

```
BASE/v2/query/samples/?id.accession=/^OSD-10[24]$/&investigation.study.comment.Project%20Identifier&study.source%20name&study.characteristics.material%20type&format=json.records
```
→ 76 rows, 2 datasets; cols: id.accession, id.assay name, id.sample name, investigation.study.comment.project identifier, study.characteristics.material type, study.source name

**Q:** Sex of every sample in Rodent Research mouse datasets (classify female-only datasets client-side).

```
BASE/v2/query/samples/?study.characteristics.organism=/musculus/&investigation.study.comment.Project%20Identifier=/^RR-?\d|^RRRM/&study.characteristics.sex&study.factor%20value.sex&format=json.records
```
→ 7681 rows, 124 datasets; cols: id.accession, id.assay name, id.sample name, investigation.study.comment.project identifier, study.characteristics.organism, study.characteristics.sex …

**Q:** Per-subject table for rodents: project id + source name + tissue + assay (aggregate client-side).

```
BASE/v2/query/samples/?study.characteristics.organism=/musculus|rattus/&investigation.study.comment.Project%20Identifier&study.source%20name&study.characteristics.material%20type&format=json.records
```
→ 31732 rows, 282 datasets; cols: id.accession, id.assay name, id.sample name, investigation.study.comment.project identifier, study.characteristics.material type, study.characteristics.organism …

## Citation and study-level facts

**Q:** DOI and title for OSD-104 (citation).

```
BASE/v2/query/datasets/?id.accession=OSD-104&investigation.study.comment.doi&investigation.study.study%20title&format=json.records
```
→ 1 rows, 1 datasets; cols: id.accession, investigation.study.comment.doi, investigation.study.study title

**Q:** Which mouse datasets are spaceflight studies (not ground analogs), with mission name?

```
BASE/v2/query/datasets/?study.characteristics.organism=/musculus/&investigation.study.comment.project%20type=/spaceflight/&investigation.study.comment.mission%20name&format=json.records
```
→ 163 rows, 163 datasets; cols: id.accession, investigation.study.comment.mission name, investigation.study.comment.project type, study.characteristics.organism

**Q:** Everything OSDR records at study level for OSD-557 (all comment fields).

```
BASE/v2/query/datasets/?id.accession=OSD-557&investigation.study.comment&format=json.records
```
→ 1 rows, 1 datasets; cols: id.accession, investigation.study.comment.acknowledgments, investigation.study.comment.data source accession, investigation.study.comment.data source link, investigation.study.comment.doi, investigation.study.comment.experiment platform …

## Keyword search (crude)

**Q:** Datasets whose title mentions kidney.

```
BASE/v2/query/datasets/?investigation.study.study%20title=/kidney/&format=json.records
```
→ 9 rows, 9 datasets; cols: id.accession, investigation.study.study title

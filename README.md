# mutagenesis-workflow

> Workflow for analysing mutagenesis experiments in proteins (educational purposes).

## Install

For now you can only clone the repository and use the script directly.

## Basic usage

```
$ python mutagenesis_workflow.py examples/GSE147194_ACE2_deep_mutagenesis.csv
```

```
$ python mutagenesis_workflow.py examples/GSE147194_ACE2_deep_mutagenesis.csv --filter-threshold 2 --filter-method or --output out_2
```

```
$ python mutagenesis_workflow.py examples/GSE147194_ACE2_deep_mutagenesis.csv --steps filter aa_props --filter-threshold 2 --filter-method mean --output out_3
```

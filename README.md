# MakePy

MakePy is a tool to generate a very simple makefile for your C projects. It scan all your C files in a specific path (recursively) and analyze the dependencies between they. Then it generates a make file with only the necesary files (C files that are not dependency in some level of the main file are not included).

## Instalation

```shell
pip install -r requirements.txt
```

## How to use

### Generate makefile

To generate the makefile of a project located in some `path` type:

```shell
python makepy.py [path]
```

### Setting a compilation ouput name

```shell
python makepy.py [path] [name]
```

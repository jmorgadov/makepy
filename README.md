# MakePy

MakePy is a tool to generate a very simple makefile for your C projects. It scan all your C files in a specific path and analyce the dependencies between they. The it uses this information to generate a correct compilation order.

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
python makepy.py [path] -o [name]
```

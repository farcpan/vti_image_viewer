# setup

## Python 

```
$ python --version
Python 3.10.6
```

```
$ cd converter
$ python -m venv .venv
$ source .venv/Scripts/activate
```

```
$ pip install matplotlib numpy pandas pynrrd scipy slicer vtk
```

* `.nrrd`ファイルを`converter`フォルダ直下に配置する

```
vti_image_viewer
    |
    `--- converter
    |       |
    |       `--- *.nrrd
    |       |
    |       `--- *.vti
    |       |
    |       `--- convert.py
    |       |
    |       `--- viewer.py
    |
    `--- viewer
    |
    `--- README_Setup.md
    |
    `--- README.md
```

---

## React

```
$ npm create vite@latest
│
◇  Project name:
│  viewer
│
◇  Select a framework:
│  React
│
◇  Select a variant:
│  TypeScript
│
◇  Use rolldown-vite (Experimental)?:
│  No
│
◇  Install with npm and start now?
│  Yes
│
◇  Scaffolding project in D:\Projects\ReactProjects\nrrd_viewer\nrrdviewer...
│
◇  Installing dependencies with npm...
```

```
$ cd viewer
$ npm install @kitware/vtk.js
```

---



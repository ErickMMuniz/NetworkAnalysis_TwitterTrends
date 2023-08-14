# Docker

## For XeLatex enviroment

### To build 
    docker build . -f docker/LaTexDocker -f xelatex-docker

### To run 
    docker run -v "/mnt/d/testFolder/testProgrammingProjects/networkX:/app" -it xelatex-docker /bin/bash

### Compile Tex file
    xelatex -file-line-error -interaction=nonstopmode main.tex

## For Python docker file

### To build 
    docker build -r ray-docker .

### To run 
    docker run -v "/mnt/d/testFolder/testProgrammingProjects/networkX:/app" -it ray-docker /bin/bash
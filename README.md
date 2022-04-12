# Redes complejas: Dinámica del comportamiento explosivo en tendencias de Twitter. 

---

## Resumen 

La comunicación es un fenómeno complejo desarrollado entre seres humanos. Este fenómeno nace de la necesidad del ser humano por un intercambio de ideas u opiniones. Debido al avance tecnológico, la comunicación ha optimizado su efectividad entre tiempos de respuesta y alcance entre personas.  Como consecuencia de la dinámica social, existen patrones de comunicación que se verán reflejados en estos nuevos medios tecnológicos. Uno de estos es el comportamiento explosivo: una alta interacción de ideas en cortos periodos de tiempo. El estudio de este fenómeno es importante debido a que tiene repercusiones políticas, sociales y hasta económicas. 

En este trabajo, se analizarán diversas redes sociales donde los nodos serán usuarios que interactuaron y los enlaces es la relación de seguimiento mutuo. Por cada tendencia o tema en la base de datos, se generarán redes temporales para caracterizar diversos patrones entre aquellas tendencias que tiene un comportamiento explosivo. Por tanto, el **objetivo principal** es determinar tendencias con comportamiento explosivo en función de métricas de centralidad y de redes sociales. 


## Herramientas de trabajo.

- Calculos
  - Python
  - R
  - Gephi 
  - Google Colab






### Datos

La base de datos fue recabada por el Centro de Investigación de Redes y Sistemas Complejos [(CNetS)](https://cnets.indiana.edu/). Estos datos son una recopilación de varios tweets con su respectivo usuario autor, tema asociado (tendencia) y tiempo en el cual la acción fue realizada.   Además, se cuenta con una lista de enlaces entre usuarios autores que es la relación de seguimiento mutuo. El periodo de tiempo donde se recabaron los datos fue del 24 de marzo de 2012 al 25 de abril de 2012. Por privacidad de la información, todos los usuarios tienen una identificación diferente a su usuario real.  

Con lo anterior, se puede generar diversas redes temporales, una por cada tendencia, indexadas en un periodo de tiempo de una hora para determinar un patrón en la interacción entre usuarios. Dando importancia en analizar la red inducida, que es aquella red generada por una lista de nodos, por aquellos nodos que iniciaron la comunicación de la tendencia. 


```latex
@inproceedings{weng2014predicting,
  title={Predicting successful memes using network and community structure},
  author={Weng, Lilian and Menczer, Filippo and Ahn, Yong-Yeol},
  booktitle={Eighth international AAAI conference on weblogs and social media},
  year={2014}
}
```

```latex
@article{weng2013virality,
  title={Virality prediction and community structure in social networks},
  author={Weng, Lilian and Menczer, Filippo and Ahn, Yong-Yeol},
  journal={Scientific reports},
  volume={3},
  number={1},
  pages={1--6},
  year={2013},
  publisher={Nature Publishing Group}
}
```


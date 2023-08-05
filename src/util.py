import multiprocessing
from tqdm import tqdm
from logging import warning



def parallel_map(func, lst):
  """
  Ejecuta cada elemento de la lista en paralelo.

  Args:
    func: La función a ejecutar en cada elemento de la lista.
    lst: La lista de elementos a ejecutar.

  Returns:
    Una lista de los resultados de la función ejecutada en cada elemento de la lista.
  """

  # Crea un pool de hilos.
  with multiprocessing.Pool() as pool:
    # Ejecuta cada elemento de la lista en paralelo.
    return list(tqdm(pool.imap(func, lst)))

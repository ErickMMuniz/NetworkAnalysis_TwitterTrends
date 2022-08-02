# import os.path
#
# from burstkit.calculate.graphs_attributes import calculate_some_metrics_and_return_graph_follower, \
#     calculate_some_metrics
# from burstkit.util import read_files as rf
# from logging import warning
# from networkit import overview
# from networkit import Graph
# from tqdm import tqdm
# #G = calculate_some_metrics_and_return_graph_follower()
# from burstkit.util.read_files import get_dataframe_trend_to_id, PATH_DATA_NETWORKS_BY_TREND
# from os import listdir
#
#
# def is_calculated_trend(trend: "str") -> "bool":
#     id = idmap[trend]
#     file_to_omite_trend = "communitie.csv"
#     is_calculated = False
#     try:
#         folder_attributes_to_read = listdir(os.path.join(PATH_DATA_NETWORKS_BY_TREND,f"TREND_ID_{id}","attributes"))
#         is_calculated = file_to_omite_trend in folder_attributes_to_read
#     except FileNotFoundError:
#         is_calculated = False
#     return not is_calculated
#
# if __name__ == '__main__':
#     idmap = get_dataframe_trend_to_id()
#     trends = list(idmap.keys())
#     print("Number of trends: ", len(trends))
#     # NOTE: this is a list of trends to calculate
#     # FIXME: The order of the list in only to my personal computer.
#     trends = list(filter(is_calculated_trend, trends))[10:21:1]
#     print("Number of trends to calculate: ", len(trends))
#
#     for trend in tqdm(trends, dynamic_ncols=True):
#         id = idmap[trend]
#         warning(f"[BEGIN][{trend}][{id}] -------------------     Processing trend -------------------")
#         g: "Graph" = rf.get_nk_graph_from_file(trend)
#         calculate_some_metrics(trend=trend,g = g  , save_to_file=True, from_colab = False)
#         warning(f"[END][{trend}][{id}] -------------------     Processing trend -------------------")


# Abourt red de vecinos

import burstkit.results as results

# from burstkit.results import red_vecinos
#
#
# Results from red_vecinos
# red_vecinos.main()


# Abourt red de vecinos
# from networkx import read_gexf
# import os
#
# from burstkit.util.read_files import get_timeline_tweets_by_trend
#
# list_trends = os.listdir("data/data_new_vecindad/data_new_vecindad")
#
# if __name__ == "__main__":
#     path_gexf_trends = dict(
#         map(
#             lambda trend: (trend.split('.')[0], f"data/data_new_vecindad/data_new_vecindad/{trend}"),
#             list_trends,
#         )
#     )
#
#     trends = list(path_gexf_trends.keys())
#     TREND = trends[0]
#     path_gexf = path_gexf_trends[TREND]
#
#     from networkx import Graph
#     from networkx import get_node_attributes
#     from logging import warning
#
#     warning(f"[BEGIN][{TREND}] -------------------     Processing trend -------------------")
#     g : Graph = read_gexf(path_gexf)
#     timeline: "DataFrame" = get_timeline_tweets_by_trend(TREND)
#     # print(g.nodes(data=True))
#     # core_array : list = list(get_node_attributes(g, "core"))
#     # print(core_array)
#     node_attributes: dict[str, dict] = dict(g.nodes(True))
#
#
#     # timeline['core'] = timeline[]
#     # b = explosivo
#     # code = core number
#     # ft = primer tweet
#     warning(f"[END][{TREND}] -------------------     Processing trend -------------------")



# Sobre la linea de tiempo. Volvemos a recuperar el timeline
import burstkit.results.plot_timelines_trends as result_plot_timelines_trends
if __name__ == '__main__':
    result_plot_timelines_trends.main()



#Sobre la linea de tiempo y comprarlo con un atributo.
# import burstkit.results.comparative_timeline_attribute as result_comparative_timeline_attribute
# if __name__ == '__main__':
#     result_comparative_timeline_attribute.main()

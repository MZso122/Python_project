# ebben gondoltam vegig hivni a subscripteket.

import alapok as alapok


def main(gui, cluster_num2:int = 6, print_extra_info:bool = False, abrak:bool = False, show_inertia_KMeans:bool = True,
         show_KMeans_pelda:bool = False, obj_path:string = 'raw_features_1st_q', obj_path_for_red:string = 'tomoritett_pirosak'):
    alapok.main_fn(gui, cluster_num2 = cluster_num2, print_extra_info = print_extra_info, abrak = abrak, show_inertia_KMeans = show_inertia_KMeans,
                    show_KMeans_pelda = show_KMeans_pelda, obj_path = obj_path, obj_path_for_red = obj_path_for_red)





if __name__ == '__main__':
    # alapok.raw2feat()
    main()




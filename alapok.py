
import os
import string
#os.environ["OMP_NUM_THREADS"] = "1"

from numpy import unique
from numpy import where
import numpy
import csv
import tkinter as tk
from sklearn.datasets import make_classification
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import SpectralClustering
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def print_hi(name: string) -> None:
        print(f'Hi, {name} \n')  


# ez a subject_info -t olvassa be
def readCSV_File(file_path: string) -> list:
    subject_info_ = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row (if present)

        for row in reader:
            value = row[:]  # Assuming the time series is in the first column
            subject_info_.append(value)

    return subject_info_


# kiíratáshoz használt...
def generateCSV(darab_: list, file_name: string) -> None:
    a = numpy.asarray(darab_)
    # print(a)
    numpy.savetxt(file_name, a.astype(int), fmt='%i',  delimiter=',')
    # numpy.savetxt(f, result.astype(int), fmt='%i', delimiter=",")


# ez a klaszterekbe került jelek görbéinek olvasásához kell
def readCSVFileNezegeto(file_path: string) -> list:
    gorbe = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        # next(reader)  # Skip header row if present

        for row in reader:
            value = float(row[0])  # Assuming the time series is in the first column
            gorbe.append(value)

    return gorbe


# némely matpoltlib-es cucchoz kell egy adatsor hosszú tengelyt generálni,
# mert nem megy anélkül. Ez egy ilyet csinál. Bemenetnek pedig maga az
# adatsor kell, itt számolok hosszát is.
def generateX_axis(data_: list) -> list:
    array_of_1s = []
    for i in range(len(data_)):
        array_of_1s.append(i)

    return array_of_1s


def main_fn(gui, cluster_num2:int = 6, print_extra_info:bool = False, abrak:bool = False, show_inertia_KMeans:bool = True, show_KMeans_pelda:bool = False,
            obj_path:string = 'raw_features_1st_q', obj_path_for_red:string = 'tomoritett_pirosak'):

# if __name__ == '__main__':
    print_hi('PyCharm')

    #abrak = False       -----------Fv arg

    #show_inertia_KMeans = True    -Fv arg
    #show_KMeans_pelda = False     -Fv arg

    # objektiv eleres a FELDOLGOZATLAN feature vektorok csv-ihez
    # mondjuk itt mar nem...
    #obj_path = 'raw_features_1st_q'   ---------Fv arg

    #obj_path_for_red = 'tomoritett_pirosak'   -Fv arg

    #
    # gui.hi_there["text"] = "Running"
    # gui.text = "Running"
 
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    # ax.plot(range(1, 20), range(1,20), marker='o')
    # ax.set_title('lkfdkjdslkfjsdkljfsldkfkjsdlkfj')
    # ax.set_xlabel('sdjkfhdskfheruoifher')
    # ax.set_ylabel('ldjfdslkfjkkdsfhewriufhiuwerfh')
    # # pyplot.show()
    canvas = FigureCanvasTkAgg(fig, master=gui)
    # canvas.draw()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # ndarray of
    nda_age_sex_bwi = []

    # a kesz csv ebbe lesz kiiratva __ Mik szerint:(age, s=sex, b=bmi)  __ Milyen modszerrel
    kiirato_age_s_b_filename_KMEANS = "kimenet/KMeans_ASB_cluster_{}.csv"
    # ez csak egy kezdet az TODO error handling(ek)nek...
    if kiirato_age_s_b_filename_KMEANS == "":
        print("jo lenne vmi eleresi_ut/nev a kiirt fajlnak")

    # az osszes subjectet tartalmazo csv file beolvasasa
    # es ndarray-va konvertalas az egyszerusegert jovoben
    subject_info = readCSV_File('subject-info.csv')
    ndarray_subj_info = numpy.asarray(subject_info)



    #
    # --------------ez egy nagy szűrés ami végigmegy a fájlokon és csak az ide kellőket olvassa be---------------------
    # -------------- a többit eldobja, vagy átugorja. Ehhez használ többféle értéket is amiket a -----------------------
    # -------------- feature-vector ból olvas be. ----------------------------------------------------------------------

    #
    # A feture_vec osszeallitasa:
    # 0 -> sistole_avg      (pressure)
    # 1 -> diastole_avg       (prssr)
    # 2 -> how_many_thrown          (a rossznak itelt szegmensek szama az atlagvetel soran)
    # 3 -> how_many_kiindulo_sig            (eredetileg mennyi jelszegmens volt)
    # 4 -> avg_sig_le  (ez hatarozza meg a max jel hoszt, ebben a lepesben(clastering) eljut, igy itt ez a relevans max)
    # 5 -> subject number   (hanyadik alany)
    # 6 -> hany karakterisztikus pontot talaltunk
    # 7+ -> a karakterpontok t, y[=f(t)] koordinataparok sorban: x1, y1, x2, y2, x3.......

    # az osszes feature_vec beolvasas, listaba
    list_of_files_features = [f for f in os.listdir(obj_path) if f.endswith('RawFeatures.csv')]

    # ezek minosegi mutatok
    keves_alapjan_atlagolt = 0
    jelmintaszam_0as = 0
    nem_jo_pontszam = 0

    # a mar feldolgozott feature_vec -ok
    formazott_features = []
    length_L = []
    # mivel a subj_info ertelemszeruen nem tudja, hogy melyik alany jele (akar reszben)
    # nem lett feldolgozva feat_vec -ra (mert hibas volt, vagy threshold alatti a minosege),
    # így kellett irjak egy atterest a subj_info es a kept == megtartott fea(ture)_vec -ok kozott
    raw_fea_num_to_subj_keys = []
    kept_fea_num_keys_to_subjs = []
    kept_fea_file_names = []

    # ez a vegtelen sor ertekeli a minosegeket es osszeallitja az elobbi listakat
    # itt lehet/van olyan, hogy eldob meg a kapott fea_vec -okbol, ha nem eleg jo a minoseguk.
    for f in range(len(list_of_files_features)):
        temp_features = []
        inner_temp = []

        feature_path = obj_path + '/' + list_of_files_features[f]
        actualis_features = readCSVFileNezegeto(feature_path)
        raw_fea_num_to_subj_keys.append(actualis_features[5])   # az 5os helyen a subj_num utazik
        temp_features.append(actualis_features[7:])             # 7tol felfele vannak a megtalalt karakterisztikus pontok adatai
        length_L.append(actualis_features[4])                   # milyen hosszu volt az adott jel. (T_max)

        if list_of_files_features[f][16] == '0':
            jelmintaszam_0as += 1
            #           print('0as a szama: ', list_of_files_features[f])
        elif (actualis_features[2]/actualis_features[3]) > 0.4:
            keves_alapjan_atlagolt += 1
            #           print('keves jelbol atlagolt: ', list_of_files_features[f])
        else:
            if len(temp_features[0]) == 10:
                #           print('GOOD; 5 csucs: ', list_of_files_features[f])
                kept_fea_num_keys_to_subjs.append(actualis_features[5])
                #           print(list_of_files_features[f])
                #           print(list_of_files_features[f][:17])
                kept_fea_file_names.append(list_of_files_features[f][:17]+'.csv_Atlag_gorbe_piros.csv')
                #           print('\n')
                #           print(feature_path + ':')
                #           print('5 csucs found')
                formazott_features.append(temp_features[0])
            elif len(temp_features[0]) == 8:
                #           print('GOOD; 4 csucs: ', list_of_files_features[f])
                kept_fea_num_keys_to_subjs.append(actualis_features[5])
                kept_fea_file_names.append(list_of_files_features[f][:17]+'.csv_Atlag_gorbe_piros.csv')

                inner_temp.append(temp_features[0][0])
                inner_temp.append(temp_features[0][1])
                inner_temp.append((temp_features[0][1] + temp_features[0][2]) / 2)
                inner_temp.append(temp_features[0][2])
                inner_temp.append(temp_features[0][3])

                inner_temp.append(temp_features[0][4])
                inner_temp.append(temp_features[0][5])
                inner_temp.append((temp_features[0][5] + temp_features[0][6]) / 2)
                inner_temp.append(temp_features[0][6])
                inner_temp.append(temp_features[0][7])

                formazott_features.append(inner_temp)
            elif len(temp_features[0]) == 6:
                #           print('GOOD; 3 csucs: ', list_of_files_features[f])
                kept_fea_num_keys_to_subjs.append(actualis_features[5])
                kept_fea_file_names.append(list_of_files_features[f][:17]+'.csv_Atlag_gorbe_piros.csv')

                #           print('\n')
                #           print(feature_path + ':')
                #           print('3 pont van, ket csucsu jel')

                inner_temp.append(temp_features[0][0])
                inner_temp.append(0)
                inner_temp.append(0)
                inner_temp.append(temp_features[0][1])
                inner_temp.append(temp_features[0][2])
                #           formazott_features.append(temp_features[0][1:])

                inner_temp.append(temp_features[0][3])
                inner_temp.append(0)
                inner_temp.append(0)
                inner_temp.append(temp_features[0][4])
                inner_temp.append(temp_features[0][5])
                #           formazott_features.append(temp_features[0][4:])

                formazott_features.append(inner_temp)
            elif len(temp_features[0]) == 2:
                #           print('GOOD; 1 csucs: ', list_of_files_features[f])
                kept_fea_num_keys_to_subjs.append(actualis_features[5])
                kept_fea_file_names.append(list_of_files_features[f][:17]+'.csv_Atlag_gorbe_piros.csv')

                #           print('\n')
                #           print(feature_path + ':')
                #           print('1 pont van, egy csucsu jel')

                inner_temp.append(temp_features[0][0])
                inner_temp.append(0)
                inner_temp.append(0)
                inner_temp.append(0)
                inner_temp.append(0)

                inner_temp.append(temp_features[0][1])
                inner_temp.append(0)
                inner_temp.append(0)
                inner_temp.append(0)
                inner_temp.append(0)

                formazott_features.append(inner_temp)
            else:   # ez kinda egy hiba nezegeto, igy itt hagytam az else-ben kommentben
                nem_jo_pontszam += 1
                # print('Nem 0as, jo atl, de nem jo pontszam: ', list_of_files_features[f])
                # print('\n')
                # print(feature_path + ':')
                # print('rossz csucsszam. Csucsszam:')
                # print(temp_features[0])

    # az elobbi for-loop eredmenyeinek kiiratasa
    print("kiiertekeles:\n")
    print('extran dobva \"keves alpjan\": ', keves_alapjan_atlagolt, 'db')
    print('extra eldobas \"0-as jelminta\" miatt:', jelmintaszam_0as, 'db')
    print('extra dobas \" deriv pont alapjan\": ', nem_jo_pontszam, 'db')
    print('formazott features hossza: ', len(formazott_features))

    nda_raw_fea_num_to_subj_keys = numpy.asarray(raw_fea_num_to_subj_keys)
    nda_kept_fea_num_keys_to_subjs = numpy.asarray(kept_fea_num_keys_to_subjs)
    if(print_extra_info):
        print('raw_fea_num_to_subj_keys:\n', raw_fea_num_to_subj_keys)
        print('nda_raw_fea_num_to_subj_keys:\n', nda_raw_fea_num_to_subj_keys)

        print('\nkept features \\ subjectnums:\n', kept_fea_num_keys_to_subjs,'\n')
        print('\n kept_file_names: \n', kept_fea_file_names, '\n')

    #
    # a form_fea-ban az elso 5 az x ertek (time); a masodik 5 pedig amplitude (y_value)
    # a feld_fea-ban: a2/a1, a3/a1, v1/v2; Ta2/Ta1, Ta3/Ta1, Tv2/Ta1; v2/a1, Tv1/Ta1
    # itt a feld(olgozott)_fea(tures) feltoltese tortenik,ezek ilyen irodalomban hasznalt ertekek/aranyok
    feldolgozott_features = []
    for rf in range(len(formazott_features)):
        temp_feld_fea = []

        # a2/a1, a3/a1, v1/v2;
        temp_feld_fea.append(formazott_features[rf][7]/formazott_features[rf][5])
        temp_feld_fea.append(formazott_features[rf][9]/formazott_features[rf][5])
        if formazott_features[rf][8] == 0:
            temp_feld_fea.append(0)
        else:
            temp_feld_fea.append(formazott_features[rf][6]/formazott_features[rf][8])

        # Ta2/Ta1, Ta3/Ta1, Tv2/Ta1;
        temp_feld_fea.append(formazott_features[rf][2]/formazott_features[rf][0])
        temp_feld_fea.append(formazott_features[rf][4]/formazott_features[rf][0])
        temp_feld_fea.append(formazott_features[rf][3]/formazott_features[rf][0])

        # v2/a1; Tv1/Ta1
        temp_feld_fea.append(formazott_features[rf][8]/formazott_features[rf][5])
        temp_feld_fea.append(formazott_features[rf][1]/formazott_features[rf][0])

        # Ta1/L
        temp_feld_fea.append(formazott_features[rf][0]/length_L[rf])

        # filling feldolg_feat -es
        feldolgozott_features.append(temp_feld_fea)

    # print(feldolgozott_features)
    #

    # -----------------------------------------kmeans pelda szett-------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    if show_KMeans_pelda:
        # define dataset
        X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1,
                                   random_state=4)
        print(X)
        print('x tipusa:')
        print(type(X))
        # define the model
        model = KMeans(n_clusters=2)
        # fit the model
        model.fit(X)
        # assign a cluster to each example
        yhat = model.predict(X)
        # retrieve unique clusters
        clusters = unique(yhat)
        # create scatter plot for samples from each cluster
        for cluster in clusters:
            # get row indexes for samples with this cluster
            row_ix1 = where(yhat == cluster)
            print(row_ix1)
            # create scatter of these samples
            pyplot.scatter(X[row_ix1, 0], X[row_ix1, 1])
        # show the plot
        pyplot.show()

    #
    # k-means clustering------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    #

    cluster_num = 8

    #                      6 alatt a 2 == 15 == 3*5
    rows=3
    cols=5
    possible_pairs = []

    for ii in range(cluster_num):
        for i in range(ii+1, cluster_num):
            possible_pairs.append(ii)
            possible_pairs.append(i)

    # print(possible_pairs)

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------- KMeans model2 --------------------------------------------------------

    ndarray_feldolgozott_features = numpy.asarray(feldolgozott_features)

    #cluster_num2 = 12
    # define the model
    model2 = KMeans(n_clusters=cluster_num2)
    # fit the model
    model2.fit(ndarray_feldolgozott_features)
    # assign a cluster to each example
    yhat2 = model2.predict(ndarray_feldolgozott_features)
    # retrieve unique clusters
    clusters2 = unique(yhat2)

    if abrak:
        # fig_3, axarr2 = pyplot.subplots(nrows=rows, ncols=cols, figsize=(18, 9))
        axarr2=ax
        ax.clear()
        # print(possible_pairs)
        for cluster2 in clusters2:
            row_ix2 = where(yhat2 == cluster2)
            # print(row_ix2)
            # print(type(row_ix2))
            # print(ndarray_feldolgozott_features[row_ix2, 0])
            for pp in range(int(len(possible_pairs)/2)):
                # print(pp)
                # print(pp//rows)
                # TODO ezek lehet csak akkor jok, ha pontosan jon ki a 'row*col = n alatt a k '
                axarr2[pp%rows, (pp//rows)].set_ylabel("Dims:{} {}".format(possible_pairs[pp*2], possible_pairs[2*pp+1]), fontsize=8, rotation=90)
                axarr2[pp%rows, (pp//rows)].scatter(ndarray_feldolgozott_features[row_ix2, possible_pairs[pp*2]], ndarray_feldolgozott_features[row_ix2, possible_pairs[pp*2+1]])
            # pyplot.scatter(ndarray_feldolgozott_features[row_ix2, 0], ndarray_feldolgozott_features[row_ix2, 1])
        axarr2[0, 2].set_title("KMeans (feldolgozott_features -ok) szerint klaszterezve", fontsize=16)
        pyplot.tight_layout()
        # pyplot.show()
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=1)


    # -----

    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------- KMEANS -> more important part(s) ---------------------------------------
    # ---------- Elbow method ----------
    if show_inertia_KMeans:
        inertias = []
        for i in range(1, 20):
            kmeans = KMeans(n_clusters=i)
            kmeans.fit(ndarray_feldolgozott_features)
            inertias.append(kmeans.inertia_)

        # fig = pyplot.figure()
        # ax = fig.add_subplot(111)
        ax.clear()
        ax.plot(range(1, 20), inertias, marker='o')
        ax.set_title('Elbow módszer')
        ax.set_xlabel('Klaszterszám')
        ax.set_ylabel('Inercia')
        # pyplot.show()
        # canvas = FigureCanvasTkAgg(fig, master=gui)
        canvas.draw()

    # fig_DB, axarr_DB = pyplot.subplots(nrows=rows, ncols=cols, figsize=(18, 9))

    for clstr in clusters2:
        row_ix2 = where(yhat2 == clstr)

        for i in row_ix2:
            # fig_kmeans_gorbek_per_clstr, ax_fig_kmns = pyplot.subplots(figsize=(10, 5))
            ax_fig_kmns=ax
            ax.clear()
            # print('ROW_IX: ')
            if(print_extra_info):
                print('obj_path_red: ', obj_path_for_red)
                print('i in row_ix:', i)
            avg_vonal = []
            cnt=0
            for ii in i:

                piros_path = obj_path_for_red + '/' + kept_fea_file_names[ii]
                actualis_piros_vonal = readCSVFileNezegeto(piros_path)

                if (print_extra_info):
                    print('\nkirajzolashoz:')
                    print('ii in i: ', ii)
                    print('kept_fea_file_names[i[ii]]: ', kept_fea_file_names[ii])
                    print(obj_path_for_red + '/' + kept_fea_file_names[ii])
                    print('piros_path: ', piros_path)

                if (cnt == 0):
                    avg_vonal = actualis_piros_vonal
                else:
                    avg_vonal = [cnt*x / (cnt+1) for x in avg_vonal]
                    dev_piros_vonal = [y / (cnt+1) for y in actualis_piros_vonal]
                    if len(avg_vonal)<len(dev_piros_vonal):
                        for suni in range(len(dev_piros_vonal)-len(avg_vonal)):
                            avg_vonal.append(0)
                    elif len(avg_vonal)>len(dev_piros_vonal):
                        for suni in range(len(avg_vonal)-len(dev_piros_vonal)):
                            dev_piros_vonal.append(0)

                    if (print_extra_info):
                        print('\nlen avg_vonal = ', len(avg_vonal), ', len dev_act_piros_v = ', len(dev_piros_vonal))
                    avg_vonal = [avg_vonal[x] + dev_piros_vonal[x] for x in range(len(avg_vonal))]
                ax_fig_kmns.plot(generateX_axis(actualis_piros_vonal), actualis_piros_vonal, color="red", lw="2")
                cnt += 1
            ax_fig_kmns.set_title("A klaszterbeli görbék", fontsize=9)
            ax_fig_kmns.plot(generateX_axis(avg_vonal), avg_vonal, color="green", lw="3")
            pyplot.tight_layout()
            # pyplot.show()
            canvas.draw()


    cnt = 0
    for cluster2 in clusters2:
        cnt += 1
        row_ix2 = where(yhat2 == cluster2)

        nda_age_sex_bwi.append((ndarray_subj_info[nda_kept_fea_num_keys_to_subjs[row_ix2].astype(int)-1, 0]).astype(int))
        nda_age_sex_bwi.append((ndarray_subj_info[nda_kept_fea_num_keys_to_subjs[row_ix2].astype(int)-1, 1]).astype(int))
        nda_age_sex_bwi.append((ndarray_subj_info[nda_kept_fea_num_keys_to_subjs[row_ix2].astype(int)-1, 2]).astype(int))
        nda_age_sex_bwi.append((ndarray_subj_info[nda_kept_fea_num_keys_to_subjs[row_ix2].astype(int)-1, 3]).astype(int))
        nda_age_sex_bwi.append((ndarray_subj_info[nda_kept_fea_num_keys_to_subjs[row_ix2].astype(int)-1, 5]).astype(int))

        #           print('\n')
        #           print(nda_age_sex_bwi)

        generateCSV(nda_age_sex_bwi, kiirato_age_s_b_filename_KMEANS.format(cnt))

        nda_age_sex_bwi = []




    print('\nDONE :\')')
    gui.hi_there["text"] = "Run program\n(click me)"






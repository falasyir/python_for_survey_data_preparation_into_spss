import pandas as pd
import numpy as np


def sort_kolom_multirespon(data_sort):
    """
    Melakukan sorting kolom pertanyaan multirespon
    
    Parameter
    ----------------
    data_sort : tabel dengan kolom pertanyaan multirespon
    
    Return
    ----------------
    data_sort : tabel dengan kolom yang sudah terurut
    """
    
    opsi_ke = [x.split("_")[-1] for x in data_sort.columns]
    list_kol = data_sort.columns

    #Mencari maksimum panjang karakter nomor pada nama kolom multirespon
    max_len = 1
    for i in range(len(opsi_ke)):
        panjang_char = len(opsi_ke[i])
        if panjang_char <= max_len:
            continue
        else:
            max_len = panjang_char

    #Membuat nama baru yang akan digunakan untuk sorting kolom
    new_opsi_ke_ = []
    for i in range(len(list_kol)):
        last_ = list_kol[i].split("_")[-1]
        panjang_last_ = len(last_)

        new_last_ = '0'*(max_len - panjang_last_) + last_
        new_first_ = list_kol[i].split("_")[:-1]
        new_first_ = "_".join(new_first_)
        new_klm_ = new_first_+"_"+new_last_
        new_opsi_ke_.append(new_klm_)

    data_sort.columns = new_opsi_ke_
    data_sort = data_sort.reindex(columns=sorted(new_opsi_ke_))

    opsi_ke__ = [x.split("_")[-1] for x in data_sort.columns]
    list_kol__ = data_sort.columns

    #Mengubah kembali nama kolom yang sudah di sorting ke nama semula
    final_opsi_ke = []
    for i in range(len(list_kol__)):
        last_ = list_kol__[i].split("_")[-1]

        new_last_ = last_.lstrip("0")
        new_first_ = list_kol__[i].split("_")[:-1]
        new_first_ = "_".join(new_first_)
        new_klm_ = new_first_+"_"+new_last_
        final_opsi_ke.append(new_klm_)

    data_sort.columns = final_opsi_ke    
    
    return data_sort



def labeling_dataset(dataset, label_jawaban, kolom_labeling, kolom_abai=[], 
                     reverse=False, kolom_multi_respon=None, versi_1=True):
    """
    Melakukan labeling value dataset
    
    Parameter
    ----------------
    dataset : data yang akan dilakukan labeling
    label_jawaban : tabel daftar label jawaban
    kolom_labeling : daftar kolom yang akan dilakukan labeling
    kolom_abai : daftar kolom yang akan di-skip / lewati saat tahap labeling
    reverse : bagaimana cara melakukan labeling
        False --> melakukan labeling dari angka ke kata
        True --> melakukan labeling dari kata ke angka
    kolom_multi_respon : daftar kolom yang termasuk multiresopn
        None --> jika None, maka hanya akan melakukan labeling seperti biasa (tidak mempedulikan kolom multiresopn)
    versi_1 : inisiasi versi untuk labeling
        False --> mengaktifkan versi 2
        True --> mengaktifkan versi 1 (default)
    
    Return
    ----------------
    dataset_hasil : tabel dengan kolom yang sudah diberi label value
    output_dict : data dictionary dari label-label kolom data
    """    
    
    dataset_hasil = dataset.copy()
    list_label = label_jawaban.columns
    output_dict = dict()
    
    for klm in kolom_labeling:
        label_ = klm.split("_")[0]
        
        # skip jika nama kolom punya kondisi berikut
        if (klm in kolom_abai) or ('rp' in klm) or ('%' in klm):
            continue        
        
        # Jika multirespon ada, dan versi 1 aktif
        elif (kolom_multi_respon!=None) and (klm in kolom_multi_respon) and (versi_1==True):
            value_ = [1]
            number_ = ["Ya"]
            
        # Jika multirespon ada, dan versi 2 aktif
        elif (kolom_multi_respon!=None) and (klm in kolom_multi_respon) and (versi_1==False):
            val_ = int(klm.split("_")[-1])
            value_ = [val_]
            number_ = label_jawaban[label_jawaban[label_].notnull()][label_].loc[val_]
            number_ = [number_]
            
        # Jika multirespon tidak ada / kolom selain multirespon
        elif (label_ in list_label):
            value_ = label_jawaban[label_jawaban[label_].notnull()]['label_jawaban'].values
            number_ = label_jawaban[label_jawaban[label_].notnull()][label_]

            
        # cara labeling reverse atau tidak
        if reverse==False:
            dict_label = pd.Series(number_, index=value_).to_dict()
        else:
            dict_label = pd.Series(value_, index=number_).to_dict()

        dataset_hasil[klm] = dataset_hasil[klm].map(dict_label)            
        output_dict[klm] = dict_label
            
    return dataset_hasil, output_dict



def get_kolom_multirespon(dataset):
    """
    Mendapatakan kolom mana saja dari dataset yang termasuk kolom pertanyaan multirespon
    
    Parameter
    ----------------
    dataset : tabel dataset
    
    Return
    ----------------
    first_multi_respon : list kolom pertama pada setiap pertanyaan multirespon
    kolom_multi_respon : list seluruh kolom pertanyaan multirespon
    """    
    
    list_kolom = dataset.columns
    
    # Mendapatkan kolom multirespon
    kolom_multi_respon = []
    for last_ in list_kolom:
        last_character = last_.split("_")[-1]

        try:
            int(last_character)
        except ValueError:
            continue

        kolom_multi_respon.append(last_)

        
    # Mendapatkan kolom pertama tiap kolom multirespon
    first_multi_respon = []
    for i, first_ in enumerate(kolom_multi_respon):
        if i==0:
            first_multi_respon.append(first_)
        else:
            prev_subques = kolom_multi_respon[i-1].split("_")[:-1]
            prev_subques = "_".join(prev_subques)

            current_subques = first_.split("_")[:-1]
            current_subques = "_".join(current_subques)

            if current_subques!=prev_subques:
                first_multi_respon.append(first_)    
                
    return first_multi_respon, kolom_multi_respon



def reassign_data_multirespon(dataframe_reassign_, first_multi_respon, kolom_multi_respon, versi=1):
    """
    Melakukan transformasi tabel dan reassign value pada kolom pertanyaan multirespon
    
    Parameter
    ----------------
    dataframe_reassign_ : tabel dataset yang akan di-reassign
    first_multi_respon : list kolom pertama pada setiap pertanyaan multirespon
    kolom_multi_respon : list seluruh kolom pertanyaan multirespon
    versi : tipe hasil reassign yang diinginkan
        versi = 1 --> jawaban seluruh kolom multirespon diubah menjadi 1 dengan keterangan 'Ya'
        versi = 2 --> jawaban seluruh kolom multirespon sesuai dengan nomor kolom multirespon dengan keterangan sesuai label jawaban
    
    Return
    ----------------
    dataframe_reassign : hasil tabel dataset
    new_kolom_multi_respon : list seluruh kolom pertanyaan multirespon setelah tabel ditransformasi
    """        
    
    dataframe_reassign = dataframe_reassign_.copy()
    new_kolom_multi_respon = []
    
    for klm in first_multi_respon:
        idx_insert = dataframe_reassign.columns.to_list().index(klm)

        column_insert = klm.split("_")[:-1]
        column_insert = "_".join(column_insert)

        # Menyisipkan satu kolom baru di sebelah kiri kolom pertama multirespon untuk menampung jawaban-jawaban multiresopn pada satu list array
        dataframe_reassign.insert(loc=idx_insert, column=column_insert, value=np.nan)

        label_ = klm.split("_")[0]
        column_same_label = [x for x in kolom_multi_respon if label_ in x]

        # Mengambil nilai multirespon dan memasukkannya ke dalam kolom baru yang sudah dibuat, kemudian menghapus kolom multirespon aslinya
        dataframe_reassign[column_insert] = dataframe_reassign[column_same_label].astype("Int64").applymap(lambda x: [x] if pd.notnull(x) else []).sum(1).tolist()
        dataframe_reassign = dataframe_reassign.drop(columns=column_same_label)

        # Mengubah format data jawaban multirespon dalam list array menjadi string
        for i in range(len(dataframe_reassign)):
            dataframe_reassign.at[i, column_insert] = [str(x) for x in dataframe_reassign.loc[i, column_insert]]

        # Menghilangkan kurung siku tanda bahwa data merupakan list array
        # #dataframe_reassign[column_insert] = dataframe_reassign[column_insert].str.strip('[]') # kalau value string
        dataframe_reassign[column_insert] = dataframe_reassign[column_insert].str.join(', ') # kalau value list

        # Membuat tabel sementara dengan dummy variable dari data yang ada / melakukan assign value ke kolom baru yang sesuai
        temp = dataframe_reassign[column_insert].str.get_dummies(sep=', ')
        temp.columns = ['%s_opsi_%s'%(column_insert, x) for x in temp.columns]

        # Mengubah data yang bernilai 0 hasil dummy menjadi NaN
        if versi==1:
            temp = temp.replace(0, np.nan)
            # temp = temp.astype("Int64")
        elif versi==2:
            for x in temp.columns:
                value_ = x.split("_")[-1]
                temp[x] = temp[x].replace([0, 1], [np.nan, int(value_)])
            # temp = temp.astype("Int64")        

        # Mengurutkan kolom multirespon yang baru
        temp = sort_kolom_multirespon(temp)
        new_kolom_multi_respon.extend(temp.columns.to_list())
        
        # Menambahkan tabel sementara yang suda dibuat ke tabel dataset
        idx_place = dataframe_reassign.columns.to_list().index(column_insert)
        dataframe_reassign = pd.concat([dataframe_reassign.iloc[:, :idx_place], temp, dataframe_reassign.iloc[:, idx_place+1:]], axis=1)
        
    return dataframe_reassign, new_kolom_multi_respon




def generate_spss_syntax(nama_file, data_dipakai, label_jawaban_melted, 
                         new_kolom_multi_respon, kolom_abai = [], versi=1):
    """
    Melakukan generate syntax spss untuk keperluan labeling value
    
    Parameter
    ----------------
    nama_file : nama file text tempat menyimpan hasil generate
    data_dipakai : dataset yang akan digunakan untuk proses generate
    label_jawaban_melted : tabel daftar label jawaban dengan kolom sesuai ketentuan / ['label_jawaban', 'label pertanyaan', 'jawaban']
    new_kolom_multi_respon : list seluruh kolom pertanyaan multirespon setelah tabel ditransformasi
    kolom_abai : kolom dataset yang akan diabaikan / di-skip pada proses generate syntax
    versi : tipe hasil reassign yang diinginkan
        versi = 1 --> jawaban seluruh kolom multirespon diubah menjadi 1 dengan keterangan 'Ya'
        versi = 2 --> jawaban seluruh kolom multirespon sesuai dengan nomor kolom multirespon dengan keterangan sesuai label jawaban
    
    Return
    ----------------
    text_file_syntax : file text berisi syntax spss yang siap di-running
    """        


    data_to_spss = data_dipakai.copy()
    
    # Membuat kolom data dengan syntax spss
    tabel_label_spss = data_to_spss[['subpertanyaan','label pertanyaan']]
    tabel_label_spss = tabel_label_spss.drop_duplicates(subset=['subpertanyaan'])
    tabel_label_spss = tabel_label_spss.merge(label_jawaban_melted, on='label pertanyaan')
    tabel_label_spss['syntax spss'] = tabel_label_spss['label_jawaban'].astype("str") + '"' + tabel_label_spss['jawaban'] + '"'
    
    # Membuat file teks dengan format .txt
    if ".txt" not in nama_file:
        text_file_syntax = open("%s.txt"%(nama_file),"w+")
    else:
        text_file_syntax = open(nama_file,"w+")

    unik_label = tabel_label_spss['label pertanyaan'].unique()

    for label_ in unik_label:
        tabel_label = tabel_label_spss[tabel_label_spss['label pertanyaan'].isin([label_])]

        unik_sub = tabel_label['subpertanyaan'].unique()

        for sublabel_ in unik_sub:
            tabel_sublabel = tabel_label[tabel_label['subpertanyaan'].isin([sublabel_])]

            # Syarat untuk skip / kolom yang akan abaikan dalam pembuatan syntax
            if (sublabel_ in kolom_abai) or ("rp" in sublabel_) or ("Rp" in sublabel_) or ("%" in sublabel_):
                continue

            elif sublabel_ in new_kolom_multi_respon:
                # print("multiple answer", sublabel_)
                if versi==1:
                    text_file_syntax.write('add value label %s\n'%(sublabel_))
                    syntax_spss = '1"Ya"'

                elif versi==2:
                    text_file_syntax.write('add value label %s\n'%(sublabel_))
                    lbl_jawaban_ = sublabel_.split("_")[-1] 
                    syntax_spss = tabel_sublabel[tabel_sublabel['label_jawaban'].isin([int(lbl_jawaban_)])]['syntax spss'].values[0]

                text_file_syntax.write("%s\n"%(syntax_spss))

            else:
                # print("single answer", sublabel_)
                text_file_syntax.write('add value label %s\n'%(sublabel_))

                syntax_spss = tabel_sublabel['syntax spss'].values


                for stx in syntax_spss:
                    text_file_syntax.write("%s\n"%(stx))

            text_file_syntax.write("\n")
    text_file_syntax.close()
    
    print("done")
    
    return text_file_syntax

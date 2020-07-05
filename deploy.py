import numpy as np
import skfuzzy as fuzz
import pyrebase


config = {
    "apiKey": "AIzaSyBwpH3VmoUM8u-K5VqoILo1IAH8Q8mruQU",
    "authDomain": "air-quality-monitoring-46f28.firebaseapp.com",
    "databaseURL": "https://air-quality-monitoring-46f28.firebaseio.com",
    "projectId": "air-quality-monitoring-46f28",
    "storageBucket": "air-quality-monitoring-46f28.appspot.com",
    "messagingSenderId": "794593332188",
    "appId": "1:794593332188:web:4746b845511babd6ad1d19",
    "measurementId": "G-4SS9FDXR9M"
}

firebase = pyrebase.initialize_app(config)


def ispu_prediction(input_suhu, input_kelembaban, input_CO, input_NO2):
    # Generate universe variables
    suhu = np.arange(0, 51, 1)
    kelembaban = np.arange(0, 101, 1)
    CO = np.arange(0, 101, 1)
    NO2 = np.arange(0, 12001, 1)

    # Generate fuzzy membership functions
    dingin = fuzz.trapmf(suhu, [0, 0, 18.5, 20.5])
    sejuk  = fuzz.trimf(suhu, [18.5, 20.5, 22.8])
    nyaman  = fuzz.trimf(suhu, [20.5, 22.8, 25.8])
    hangat  = fuzz.trimf(suhu, [22.8, 25.8, 27.2])
    panas = fuzz.trapmf(suhu, [25.8, 27.2, 51, 51])

    sangat_kering = fuzz.trimf(kelembaban, [0, 15, 25])
    kering = fuzz.trimf(kelembaban, [15, 25, 45])
    ideal  = fuzz.trimf(kelembaban, [25, 45, 65])
    lembab  = fuzz.trimf(kelembaban, [45, 65, 85])
    sangat_lembab = fuzz.trimf(kelembaban, [65, 85, 101])

    baik = fuzz.trimf(CO, [0, 7, 12])
    sedang  = fuzz.trimf(CO, [10, 15, 25])
    tidak_sehat  = fuzz.trimf(CO, [17, 25, 32])
    sangat_tidak_sehat = fuzz.trimf(CO, [25, 34, 46])
    berbahaya = fuzz.trapmf(CO, [34, 46, 101, 101])

    baik_x = fuzz.trapmf(NO2, [0, 15, 30, 35])
    sedang_x  = fuzz.trapmf(NO2, [30, 35, 50, 75])
    tidak_sehat_x  = fuzz.trimf(NO2, [55, 75, 85])
    sangat_tidak_sehat_x  = fuzz.trimf(NO2, [75, 85, 100])
    berbahaya_x = fuzz.trapmf(NO2, [100, 120, 150, 300])

    BA  = 50
    SE   = 100
    TS  = 199
    STS  = 299 
    BE = 500

    BA  = 50; SE   = 100; TS  = 199; STS  = 299; BE = 500
    FAM = [[BA,SE,TS,STS,BE], [SE,SE,TS,STS,BE], [TS,TS,TS,STS,BE], [STS,STS,STS,STS,BE], [BE,BE,BE,BE,BE]]

    suhu_wilayah = int(input_suhu)
    kelembaban_wilayah = int(input_kelembaban)
    CO_wilayah = int(input_CO) * 11.5/1000
    NO2_wilayah = int(input_NO2) * 1.88

    in_1 = []
    in_1.append(fuzz.interp_membership(suhu, dingin, suhu_wilayah))
    in_1.append(fuzz.interp_membership(suhu, sejuk, suhu_wilayah))
    in_1.append(fuzz.interp_membership(suhu, nyaman, suhu_wilayah))
    in_1.append(fuzz.interp_membership(suhu, hangat, suhu_wilayah))
    in_1.append(fuzz.interp_membership(suhu, panas, suhu_wilayah))

    in_2 = []
    in_2.append(fuzz.interp_membership(kelembaban, sangat_kering, kelembaban_wilayah))
    in_2.append(fuzz.interp_membership(kelembaban, kering, kelembaban_wilayah))
    in_2.append(fuzz.interp_membership(kelembaban, ideal, kelembaban_wilayah))
    in_2.append(fuzz.interp_membership(kelembaban, lembab, kelembaban_wilayah))
    in_2.append(fuzz.interp_membership(kelembaban, sangat_lembab, kelembaban_wilayah))

    in_3 = []
    in_3.append(fuzz.interp_membership(CO, baik, CO_wilayah))
    in_3.append(fuzz.interp_membership(CO, sedang, CO_wilayah))
    in_3.append(fuzz.interp_membership(CO, tidak_sehat, CO_wilayah))
    in_3.append(fuzz.interp_membership(CO, sangat_tidak_sehat, CO_wilayah))
    in_3.append(fuzz.interp_membership(CO, berbahaya, CO_wilayah))

    in_4 = []
    in_4.append(fuzz.interp_membership(NO2, baik_x, NO2_wilayah))
    in_4.append(fuzz.interp_membership(NO2, sedang_x, NO2_wilayah))
    in_4.append(fuzz.interp_membership(NO2, tidak_sehat_x, NO2_wilayah))
    in_4.append(fuzz.interp_membership(NO2, sangat_tidak_sehat_x, NO2_wilayah))
    in_4.append(fuzz.interp_membership(NO2, berbahaya_x, NO2_wilayah))


    print("Derajat Keanggotaan Suhu:")
    if in_1[0]>0 :
        print("dingin :"+ str(in_1[0]))
    if in_1[1]>0 :
        print("sejuk :"+ str(in_1[1]))
    if in_1[2]>0 :
        print("nyaman :"+ str(in_1[2]))
    if in_1[3]>0 :
        print("hangat :"+ str(in_1[3]))
    if in_1[4]>0 :
        print("panas :"+ str(in_1[4]))

    print("")
    print("Derajat Keanggotaan Kelembaban:")
    if in_2[0]>0 :
        print("sangat kering :"+ str(in_2[0]))
    if in_2[1]>0 :
        print("kering :"+ str(in_2[1]))
    if in_2[2]>0 :
        print("ideal :"+ str(in_2[2]))
    if in_2[3]>0 :
        print("lembab :"+ str(in_2[3]))
    if in_2[4]>0 :
        print("sangat lembab :"+ str(in_2[4]))

    print("")
    print("Derajat Keanggotaan CO:")
    if in_3[0]>0 :
        print("baik :"+ str(in_3[0]))
    if in_3[1]>0 :
        print("sedang :"+ str(in_3[1]))
    if in_3[2]>0 :
        print("tidak sehat :"+ str(in_3[2]))
    if in_3[3]>0 :
        print("sangat tidak sehat :"+ str(in_3[3]))
    if in_3[4]>0 :
        print("berbahaya :"+ str(in_3[4]))
        
    print("")
    print("Derajat Keanggotaan NO2:")
    if in_4[0]>0 :
        print("baik :"+ str(in_4[0]))
    if in_4[1]>0 :
        print("sedang :"+ str(in_4[1]))
    if in_4[2]>0 :
        print("tidak sehat :"+ str(in_4[2]))
    if in_4[3]>0 :
        print("sangat tidak sehat :"+ str(in_4[3]))
    if in_4[4]>0 :
        print("berbahaya :"+ str(in_4[4]))
        
    print("Matriks Suhu:")
    print(in_1)
    print("")
    print("Matriks Kelembaban:")
    print(in_2)
    print("")
    print("Matriks CO:")
    print(in_3)
    print("")
    print("Matriks NO2:")
    print(in_4)

    rul = []
    for i in range(5):
        for j in range(5):
            rule=fuzz.relation_min(in_3[i], in_4[j])
            rul.append(rule)
            #print(rule)
    penyebut=np.sum(rul)
    #Pembilang
    rul = []
    for i in range(5):
        for j in range(5):
            rule=fuzz.relation_min(in_3[i], in_4[j])
            rulxx= rule*FAM[i][j]
            rul.append(rulxx)
            #print(rulxx)
    pembilang=np.sum(rul)
    #print (pembilang)
    #print (penyebut)
    hasil = pembilang/penyebut
    #print (hasil)

    #logic hasil
    print("ISPU :"+ str(hasil))
    if hasil >= 0 and hasil <= 50.5 :
        print("Baik")
    if hasil> 50.5 and hasil<= 100.5:
        print("Sedang")
    if hasil> 100.5 and hasil<=199.5:
        print("Tidak Sehat")
    if hasil> 199.5 and hasil<= 299.5:
        print("Sangat Tidak Sehat")
    if hasil>= 299.5:
        print("Berbahaya")

    return hasil, suhu_wilayah, kelembaban_wilayah, CO_wilayah, NO2_wilayah
    # print(suhu_wilayah, kelembaban_wilayah, CO_wilayah, NO2_wilayah)

def data_handle():
    db = firebase.database()
    root = db.child("").get().val()

    for item in root:
        location = db.child(item + '/data').get().val()
        # print(location)

        if location != None:
            for data in location:
                # print(d)
                key = db.child(data).get().key()
                print(key)
                if not key:
                    continue
        else:
            continue
            
        # print(data)

        # for data in location:
        #     co = db.child(item + '/data/co2').get().val()
        #     no2 = db.child(item + '/data/no2').get().val()
        #     suhu = db.child(item + '/data/temperature').get().val()
        #     kelembaban = db.child(item + '/data/humidity').get().val()       

        




if __name__ == '__main__':
    data_handle()
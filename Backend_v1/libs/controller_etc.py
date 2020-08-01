from libs.controller_eto import *
from libs.controller_crop import *

def etc(data):
    '''
    data = 
        georef:
            -lat
            -lon
        crop:
            -Name
            -Category
            -start
            -end
        crop_stages:
            -Init
            -Dev
            -Mid
            -Late
    '''
    
    georef = data["georef"]
    crop = data["crop"]
    crop_stages = data["crop_stages"]
    eto = get_eto(georef["lat"], georef["lon"], crop["start"], crop["end"])
    kc = get_kc_from_name_cat(crop["Name"], crop["Category"])
    mask = kc_mask(crop_stages, kc)
    res = daily_etc(eto, mask)
    return res

def daily_etc(eto, mask):
    eto_original = eto
    eto = []
    days_data = []
    for k in eto_original:
        eto.append(eto_original[k])
        days_data.append(k)
    n_eto = len(eto)
    n_mask = len(mask)
    etc = []
    for i in range(n_eto):
        eto_daily = eto[i]
        if (i < n_mask):
            mask_daily = mask[i]
        else:
            mask_daily = mask[-1]
        etc_daily = float(eto_daily)*float(mask_daily)
        etc.append(etc_daily)
    response = {
        "etc": etc,
        "days": days_data
    }
    return response

def kc_mask(crop_stages, kc):
    total_days = int(float(crop_stages["Init"])) + int(float(crop_stages["Dev"])) + int(float(crop_stages["Mid"])) + int(float(crop_stages["Late"]))
    r1 = (0, int(float(crop_stages["Init"])))
    r2 = (r1[1], r1[1]+int(float(crop_stages["Dev"])))
    r3 = (r2[1], r2[1]+int(float(crop_stages["Mid"])))
    r4 = (r3[1], r3[1]+int(float(crop_stages["Late"])))
    ideal_days = list(range((total_days)))
    for i in range((total_days)):
        if (i >= r1[0] and i < r1[1]):
            kc_day = kc["Init"]      
        elif (i >=r2[0] and i < r2[1]):
            ref = i - r2[0]
            m = float(float(kc["Mid"]) - float(kc["Init"]))/float(crop_stages["Dev"])
            n = float(kc["Init"])
            kc_day = ref*m+n
        elif (i >=r3[0] and i < r3[1]):
            kc_day = float(kc["Mid"])
        elif (i >=r4[0] and i <= r4[1]):
            ref = i - r4[0]
            m = float(float(kc["End"]) - float(kc["Mid"]))/float(crop_stages["Late"])
            n = float(kc["Mid"])
            kc_day = ref*m+n
        ideal_days[i] = float(kc_day)
    return ideal_days
        
def HH(data, tonaladas_hectareas):
    suma = sum(data["etc"])#*10/float(tonaladas_hectareas)
    print (suma)
    return suma

if __name__ == "__main__":
    res = get_cat_name()
    val = None
    for k in res:
        val = res[k][0]
        break
    crop = val
    kc = get_kc_from_name_cat(crop["Name"], crop["Category"])
    res = kc_mask(crop, kc)
    print (res)
    print (kc)




from libs.interface_crop import *

def get_cat_name():
    res = load_dev_stages()
    data = {}
    for val in res:
        cat = val["Category"]
        name = val["Name"]
        if (cat not in data):
            data[cat] = []
        _ = val.pop('_id')
        _ = val.pop('_rev')
        data[cat].append(val)
    return data

def get_kc_from_name_cat(name, cat):
    res = load_crop_coefficients()
    for r in res:
        xname = r["Name"]
        xcat = r["Category"]
        if (xname == name and xcat == cat):
            _ = r.pop('_id')
            _ = r.pop('_rev')
            return r
    return None

if __name__ == "__main__":
    res = get_kc_from_name_cat("olives", "fruit trees")
    print (res)
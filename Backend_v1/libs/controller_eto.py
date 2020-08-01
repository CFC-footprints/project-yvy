from libs.interface_weather import *
import datetime, pyeto

def get_eto(lat, lon, start, end):
    weather = weather_request(lat, lon, start, end)
    data = weather["data"]
    response = {}
    for value in data:
        day = value["date"].split("-")
        t_min = value["tmin"]
        t_max = value["tmax"]
        t_avg = value["tavg"]
        #print ("{}\t{}\t{}".format(t_min, t_max, day))
        try:
            res = daily_eto(t_min, t_max, lat, day)
        except:
            res = -1
        #print ("Day: {}\t Eto: {}".format(day, res))
        key = "{}-{}-{}".format(day[0], day[1], day[2])
        response[key] = res
    response = complete_eto(response)
    return response    

def daily_eto(t_min, t_max, lat, day):
    '''
        day: tuple (year, month, day)
    '''
    lat = pyeto.deg2rad(float(lat))
    day_of_year = datetime.date(int(day[0]), int(day[1]), int(day[2])).timetuple().tm_yday
    sol_dec = pyeto.sol_dec(day_of_year)
    sha = pyeto.sunset_hour_angle(lat, sol_dec)
    ird = pyeto.inv_rel_dist_earth_sun(day_of_year)
    et_rad = pyeto.et_rad(lat, sol_dec, sha, ird) 

    t_avg = float(t_max+t_min)/2.0
    res = pyeto.hargreaves(t_min, t_max, t_avg, et_rad)
    return res

def complete_eto(data):
    keys = []
    eto = []
    for k in data:
        keys.append(k)
        eto.append(data[k])
    if (eto[0] == -1):
        for e in eto:
            if (e != -1):
                eto[0] = e
                break
    for e in range(1, len(eto)-1):
        if eto[e] == -1:
            if (eto[e-1] != -1 and eto[e+1] != -1):
                eto[e] = (eto[e+1] + eto[e-1])/2.0
            elif (eto[e-1] != -1 and eto[e+1] == -1):
                eto[e] = eto[e-1]
            elif (eto[e-1] == -1 and eto[e+1] != -1):
                eto[e] = eto [e+1]
    if (eto[-1] == -1):
        eto[-1] = eto[-2]

    for i in range(len(eto)):
        data[keys[i]] = eto[i]
    return data
            

if __name__ == "__main__":
    lat = "-33.416889"
    lon = "-70.606705"
    start = "2020-07-01"
    end = "2020-07-15"
    res = get_eto(lat, lon, start, end)
    for k in res:
        print("{}, {}".format(k, res[k]))
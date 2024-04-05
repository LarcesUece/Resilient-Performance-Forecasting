import requests
from datetime import date, datetime
from calendar import timegm

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

today = date.today()

base = "http://monipe-central.rnp.br"


def get_data(url_slice, time_range):
    url = base+url_slice
    header = {"time-range": time_range}
    response = requests.get(url, params=header, verify=False)
    url_final = url + "/?time-range=" + header["time-range"]
    #print(url_final[:-1])
    json_data = response.json()
    return json_data


def request_by_metadata_key(url, type):
    url_ = url
    response = requests.get(url_, verify=False)
    json_data = response.json()
    if (response.status_code == 200):
        for obj in json_data["event-types"]:
            if obj["event-type"] == type:
                return obj
    else:
        return response.status_code


def calc_mean(val):
    values = []
    for key, value in val.items():
        values.append(float(key)*value)
    return sum(values)/len(values)


#coleta a vazao
def request(folder, name, source, destination, type, time_range, target_bandwidth="9999999999"):
    disable_warnings(InsecureRequestWarning)
    url = "http://monipe-central.rnp.br/esmond/perfsonar/archive/?"
    hearder = {"pscheduler-test-type": type, "source": source, "destination": destination,
               "bw-target-bandwidth": target_bandwidth, "time-range": time_range}
    response = requests.get(url, params=hearder, verify=False)
    
    #print('endereço', response.url)
    
    json_data = response.json()
    if (response.status_code == 200):
        datas = []
        for obj in json_data:
            url_obj = obj["url"]
            #print('url: ', url_obj)
            get_url_base_obj = request_by_metadata_key(url_obj, type)
            
            if (not isinstance(get_url_base_obj, int)):
                url_base = get_url_base_obj["base-uri"]
                f = open(folder+name+" esmond data " + source.split('-')[1] + '-' + destination.split('-')[1] + ' ' +
                         today.strftime("%m-%d-%Y")+".csv", "w")
                f.write(f"{'Timestamp'},{'Data'}, {'Vazao'}\n")
                data = get_data(url_base, time_range)
                datas.insert(0, data)
            else:
                return "Error " + response.status_code
        teste = []
        for i in range(len(datas)):
            cont = 0
            soma = 0
            anterior = None
            for obj in datas[i]:
                data = datetime.fromtimestamp(int(obj["ts"]))
                dia = str(data).split()[0][-2::]
                if (str(data).split()[0][-5::]) not in teste:
                    teste.append(str(data).split()[0][-5::])
                if dia == anterior or anterior is None:
                    soma += obj["val"]
                    cont += 1
                    #f.write(datetime.fromtimestamp(int(obj["ts"])).strftime('%Y-%m-%d %H:%M:%S')+", "+str(obj["val"])+"\n")
                    f.write(f"{int(obj['ts'])},{datetime.fromtimestamp(int(obj['ts'])).strftime('%Y-%m-%d %H:%M:%S')},{str(obj['val'])}\n ")
                '''else:
                    media = soma/cont
                    ciclos = 6-cont
                    for i in range(ciclos):
                        cont += 1
                        f.write(datetime.fromtimestamp(
                            int(obj["ts"])).strftime('%Y-%m-%d %H:%M:%S')+", "+str(media)+"\n")
                    soma = 0
                if cont == 6:
                    cont = 0
                    anterior = None
                else:
                    anterior = dia'''
               
        f.close()
    else:
        return "Error: " + response.status_code

def request_retrans(folder, name, source, destination, type, time_range, target_bandwidth="9999999999"):
    disable_warnings(InsecureRequestWarning)
    url = "http://monipe-central.rnp.br/esmond/perfsonar/archive/?"
    hearder = {"pscheduler-test-type": type, "source": source, "destination": destination,
               "bw-target-bandwidth": target_bandwidth, "time-range": time_range}
    response = requests.get(url, params=hearder, verify=False)
    
    #print('endereço', response.url)
    
    json_data = response.json()
    if (response.status_code == 200):
        datas = []
        for obj in json_data:
            url_obj = obj["url"]
            get_url_base_obj = request_by_metadata_key(url_obj, "packet-retransmits")
            if (not isinstance(get_url_base_obj, int)):
                url_base = get_url_base_obj["base-uri"]
                #print(url_base)
                f = open(folder + name + " esmond data " + source.split('-')[1] + '-' + destination.split('-')[1] + ' ' +
                         today.strftime("%m-%d-%Y")+".csv", "w")
                f.write(f"{'Timestamp'},{'Data'}, {'Retransmitidos'}\n")
                data = get_data(url_base, time_range)
                datas.insert(0, data)
            else:
                return "Error " + response.status_code
        teste = []
        for i in range(len(datas)):
            cont = 0
            soma = 0
            anterior = None
            for obj in datas[i]:
                data = datetime.fromtimestamp(int(obj["ts"]))
                #print(data)
                dia = str(data).split()[0][-2::]
                #print("dia:", dia)
                if (str(data).split()[0][-5::]) not in teste:
                    teste.append(str(data).split()[0][-5::])
                if dia == anterior or anterior is None:
                    soma += obj["val"]
                    cont += 1
                    #f.write(datetime.fromtimestamp(int(obj["ts"])).strftime('%Y-%m-%d %H:%M:%S')+", "+str(obj["val"])+"\n")
                    f.write(f"{int(obj['ts'])},{datetime.fromtimestamp(int(obj['ts'])).strftime('%Y-%m-%d %H:%M:%S')},{str(obj['val'])}\n ")
                
        
        f.close()
    else:
        return "Error: " + response.status_code
    
def request_traceroute(folder, name, source, destination, type, time_range):
    limite = "?limit=26400"
    url = "http://monipe-central.rnp.br/esmond/perfsonar/archive/?"
    header = {"pscheduler-test-type": type, "source": source,
              "destination": destination, "time-range": time_range}
    response = requests.get(url, params=header, verify=False)

    json_data = response.json()
    values = []
    if (response.status_code == 200):
        print("Ok")
        bases = []
        for obj in json_data:
            types_list = obj['event-types']
            for obj_types in types_list:
                if obj_types.get('event-type') == "packet-trace":
                    bases.append(obj_types.get('base-uri'))
                    break
    
    with open(folder + name + " esmond data " + source.split('-')[1] + '-' + destination.split('-')[1] + ' ' +
                         today.strftime("%m-%d-%Y")+".csv", "w") as f:
        #f.write(f"{'Timestamp'},{'Data'}, {'xxxxx'}\n")
        
        for link in bases:
            
            values: list = get_data(link+limite, time_range)
            #print('values', values)
        
            for obj in values:
                #ip_hostname_list = [item['ip'] for item in value['val']]
                f.write(f"{int(obj['ts'])},{datetime.fromtimestamp(int(obj['ts'])).strftime('%Y-%m-%d %H:%M:%S')}, ")
                for dado in range(len(obj['val'])):
                    try:
                        #print(value['val'][ip]['ip'], value['val'][ip]['hostname'])
                        if dado != len(obj['val']) - 1:
                            f.write(f"{obj['val'][dado]['ip']}, {obj['val'][dado]['hostname']}, ")
                        else:
                            f.write(f"{obj['val'][dado]['ip']}, {obj['val'][dado]['hostname']} ")
                    except BaseException:
                        if dado != len(obj['val']) - 1:
                            f.write("'No Ip', 'No Hostname', ")
                        else:
                            f.write("'No Ip', 'No Hostname' ")
                f.write('\n')
           
    f.close()
    
def request_atraso(folder, name, source, destination, type, time_range, label):
    limite1 = "?limit=270000"
    url = "http://monipe-central.rnp.br/esmond/perfsonar/archive/?"
    header = {"pscheduler-test-type": type, "source": source,
              "destination": destination, "time-range": time_range}
    '''url_aux = url
    for k, v in header.items():
        url_aux += k + "=" + v + "&"
    url_aux = url_aux[:-1]
    print(url_aux)'''
    response = requests.get(url, params=header, verify=False)
    print(response.url)
    json_data = response.json()
    values = []
    if (response.status_code == 200):
        print("Ok")
        bases = []
        for obj in json_data:
            types_list = obj['event-types']
            for obj_types in types_list:
                if obj_types.get('event-type') == label:
                    bases.append(obj_types.get('base-uri'))
                    break
        with open(folder +name+" esmond data " + source.split('-')[1] + '-' + destination.split('-')[1] + ' ' + today.strftime("%m-%d-%Y")+".csv", "w") as f:
            f.write(f"{'Timestamp'},{'Data'}, {'Atraso (ms)'}\n")
            for link in bases:
                values = get_data(link+limite1, time_range)
                for value in values:
                    f.write(f"{value['ts']},{datetime.fromtimestamp(int(value['ts'])).strftime('%Y-%m-%d %H:%M:%S')}, {calc_mean(value['val'])}\n")

#não finalizada
def request_perda(name, source, destination, type, time_range, label):
    url = "http://monipe-central.rnp.br/esmond/perfsonar/archive/?"
    hearder = {"pscheduler-test-type": type, "source": source,
               "destination": destination, "time-range": time_range}
    response = requests.get(url, params=hearder)
    json_data = response.json()
    values = []
    if (response.status_code == 200):
        print("Ok")
        bases = []
        for obj in json_data:
            types_list = obj['event-types']
            for obj_types in types_list:
                if obj_types.get('event-type') == label:
                    bases.append(obj_types.get('base-uri'))
                    break
        with open("perda/"+name+" esmond data " + source.split('-')[1] + '-' + destination.split('-')[1] + ' ' + today.strftime("%m-%d-%Y")+".csv", "w") as f:
            for link in bases:
                values = get_data(link, time_range)
                tempos = [i['ts'] for i in values]
                tempos.sort()
                for value in values:
                    f.write(f"{value['ts']}, {value['val']}\n")
#----------------------------------------------------------------------

#enderecos para coleta de dados
source_address = ["monipe-ce-banda.rnp.br", "monipe-df-banda.rnp.br", "monipe-pr-banda.rnp.br", "monipe-mg-banda.rnp.br",
               "monipe-pa-banda.rnp.br"]
destination_address = ["monipe-sp-banda.rnp.br", "monipe-rj-banda.rnp.br", "monipe-am-banda.rnp.br", "monipe-rs-banda.rnp.br",
                "monipe-ba-banda.rnp.br"]
source_address_atraso = ["monipe-ce-atraso.rnp.br", "monipe-df-atraso.rnp.br", "monipe-pr-atraso.rnp.br", "monipe-mg-atraso.rnp.br",
               "monipe-pa-atraso.rnp.br"]
destination_address_atraso = ["monipe-sp-atraso.rnp.br", "monipe-rj-atraso.rnp.br", "monipe-am-atraso.rnp.br", "monipe-rs-atraso.rnp.br",
                       "monipe-ba-atraso.rnp.br"]

# for i in range(5):
#     request("datasets vazao/original/cubic/", "cubic", source_address[i], destination_address[i],
#         "throughput", "15552000")  # 6 meses
#     request("datasets vazao/original/bbr/","bbr", source_address[i], destination_address[i],
#         "throughput", "15552000", "10000000000")  # 6 meses
#     request_retrans("datasets retrans/bbr/","bbr", source_address[i], destination_address[i],
#         "throughput", "15552000", "10000000000")  # 6 meses
#     request_retrans("datasets retrans/cubic/","cubic", source_address[i], destination_address[i],
#         "throughput", "15552000", "10000000000")  # 6 meses
#     request_traceroute("datasets traceroute/", "traceroute", source_address_atraso[i], destination_address_atraso[i],
#                        "trace", "15552000")
#     request_atraso("datasets atraso/","atraso", source_address_atraso[i],destination_address_atraso[i], "latencybg", 
#                "15552000", "histogram-owdelay")  
    


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from qiskit import QuantumCircuit, transpile, Aer


def calc(img_info_list,dot_info_list):
    sim = Aer.get_backend("aer_simulator")
    qc = QuantumCircuit(4)
    gate(qc, img_info_list,dot_info_list)
    qc = transpile(qc, sim)
    qc.save_statevector()
    counts = sim.run(qc).result().get_counts()
    print(counts)
    result = counts
    return result


def gate(qc, img_info_list,dot_info_list):
    a = 30
    for i in range(5):
        for j in range(4):
            for image_info in img_info_list:
                name = image_info[0]
                x = image_info[1]
                y = image_info[2]
                if (
                    x >= 120 + 120 * i - a
                    and x <= 120 + 120 * i + a
                    and y >= 100 + 110 * j - a
                    and y <= 100 + 110 * j + a
                ):
                    if "CC" in name:
                        if "X" in name:
                            c1,c2 = 99,99
                            isc1found,isc2found = False,False
                            for dot_info in dot_info_list:
                                if dot_info[0] == name + "D_1":
                                    c1  = dot_info[2]
                                    isc1found  = True
                                if dot_info[1] == name + "D_2":
                                    c2 = dot_info[3]
                                    isc2found = True
                                    
                                if isc1found and isc2found:
                                    qc.ccx(c1,c2,j)
                                
                            
                    else:

                        if "C" in name: # 制御量子ビットゲート
                            if "H" in name:
                                for dot_info in dot_info_list:
                                    if(dot_info[0] == name+"D"):
                                        c = dot_info[1]
                                        qc.ch(c,j)
                            elif "X" in name:
                                for dot_info in dot_info_list:
                                    if(dot_info[0] == name+"D"):
                                        c = dot_info[1]
                                        qc.cx(c,j)
                            elif "Z" in name:
                                for dot_info in dot_info_list:
                                    if(dot_info[0] == name+"D"):
                                        c = dot_info[1]
                                        qc.cz(c,j)
                        else:
                            if "X" in name:
                                qc.x(j)
                            elif "H" in name:
                                qc.h(j)
                            elif "Z" in name:
                                qc.z(j)
                            elif "Y" in name:
                                qc.y(j)




@csrf_exempt  # CSRF保護を無効にする（テスト用）
def execute_python_code(request):
    if request.method == "POST":
        # POSTリクエストからデータを取得
        data = json.loads(request.body)
        print("requested", data)
        image_info_list = data["img_data"]
        dot_info_list = data["dot_data"]
        print("img",image_info_list)
        print("dot",dot_info_list)
        # データを計算する
        result = calc(image_info_list,dot_info_list)
        #result = [image_info_list,dot_info_list]
        # print(result)
        # 計算結果をJSONレスポンスとして返す
        return JsonResponse({"result": result})
    else:
        return JsonResponse({"error": "Invalid request method"})

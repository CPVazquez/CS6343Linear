import json
import sys

import requests

__author__ = "Carla Vazquez"
__version__ = "1.0.0"
__maintainer__ = "Carla Vazquez"
__email__ = "cpv150030@utdallas.edu"
__status__ = "Development"

url = "http://10.176.67.82:8080/workflow-request/"

if __name__ == "__main__":

    print("Which store are you generating a workflow for? \n\
        A. 7098813e-4624-462a-81a1-7e0e4e67631d\n\
        B. 5a2bb99f-88d2-4612-ac60-774aea9b8de4\n\
        C. b18b3932-a4ef-485c-a182-8e67b04c208c")
    storeSelect = input("Pick a store (A-C): ")

    while storeSelect != "A" and storeSelect != "B" and storeSelect != "C":
        storeSelect = input("Invalid selection. Pick A-C: ")
    
    if storeSelect == "A" :
        storeSelect = "7098813e-4624-462a-81a1-7e0e4e67631d"
    elif storeSelect == "B" :
        storeSelect = "5a2bb99f-88d2-4612-ac60-774aea9b8de4"
    else :
        storeSelect = "b18b3932-a4ef-485c-a182-8e67b04c208c"
    
    method = input("What deployment method do you want to use (persistent or edge): ")

    while method != "persistent" and method != "edge" :
        method = input("Invalid selection. Pick persistent or edge: ")

    print("What components do you want?\n\
        * order-verifier\n\
        * delivery-assigner\n\
        * cass\n\
        * restocker\n\
        * auto-restocker")
    components = input("Enter a space seperated list: ")

    while True: 
        valid = True
        components = components.lower()
        component_list = components.split()
        for comp in component_list :
            if comp == "order-verifier" :
                continue
            elif comp == "delivery-assigner" :
                continue
            elif comp == "cass" :
                continue
            elif comp == "restocker" :
                continue
            elif comp == "auto-restocker" :
                continue
            else :
                valid = False
        if valid :
            break 
        else :
            components = input("Invalid component selection. Please enter a space\n\serperated list of valid components: ")

    workflow_dict = {
        "method": method,
        "component-list": component_list,
    }

    workflow_json = json.dumps(workflow_dict)
    print("\nWorkflow Request Generated:\n"+ json.dumps(workflow_dict, sort_keys=True, indent=4))
    response = requests.post(url+storeSelect, json=workflow_json)
    
    if response.status_code == 200 :
        print("Workflow successfully deployed!")   
    else:
        print("Workflow deployment failed: " + response.text)
    

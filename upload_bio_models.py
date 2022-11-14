import argparse
import glob
import json
import shutil
import time
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import requests

url = "http://localhost:8001/"


def download_and_unzip(url, extract_to="."):
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)


parser = argparse.ArgumentParser()
parser.add_argument(
    "--hydrate_postgres", action="store_true", help="generate new training data"
)
args = parser.parse_args()


if args.hydrate_postgres:
    time.sleep(10)

    print("Starting process to upload artifacts to postgres.")
    # get experiments repo

    download_and_unzip(
        "https://github.com/DARPA-ASKEM/experiments/archive/refs/heads/main.zip"
    )
    time.sleep(2)

    #### Person ####
    def create_person(url=url):
        path = "persons"

        payload = json.dumps(
            {
                "name": "Adam Smith",
                "email": "Adam@test.io",
                "org": "Uncharted",
                "website": "",
                "is_registered": True,
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url + path, headers=headers, data=payload)

        return response.json()

    #### Project ####

    def create_project(url=url):
        path = "projects"

        payload = json.dumps(
            {
                "name": "My Project",
                "description": "First project in TDS",
                "assets": {},
                "status": "active",
            }
        )
        headers = {"Content-Type": "application/json"}

        # return project id (p1)
        response = requests.request("POST", url + path, headers=headers, data=payload)

        return response.json()

    #### Framework ####

    def create_framework(url=url):
        path = "frameworks"

        payload = json.dumps(
            {
                "name": "Petri Net",
                "version": "0.0.1",
                "semantics": "semantics_go_here",
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url + path, headers=headers, data=payload)

        return response.text

    person = create_person()
    person_id = person.get("person_id")
    project = create_project()
    project_id = project.get("project_id")
    create_framework()

    # loop over models
    folders = glob.glob("experiments-main/thin-thread-examples/biomodels/BIOMD*/")

    def asset_to_project(project_id, asset_id, asset_type):
        payload = json.dumps(
            {
                "project_id": project_id,
                "resource_id": asset_id,
                "resource_type": asset_type,
                "external_ref": "string",
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request(
            "POST", url + "assets", headers=headers, data=payload
        )

    for folder in folders:
        ## publications ##  todo
        # try:
        #     print("Upload publication")
        #     with open(folder+"document_doi.txt", "r") as f:
        #         doi_=f.read()
        #         print(doi_)

        #     with open(folder+"document_xdd_gddid.txt", "r") as f:
        #         gddid_=f.read()
        #         print(gddid_)
        # except Exception as e:
        #     print(f"error opening {folder}document_doi.txt . - {e}")

        ## model ##
        try:
            print("Upload Model with parameters")
            # load parameters of the model and set the type values
            parameter_types = {}
            with open(f"{folder}model_mmt_parameters.json", "r") as f:
                parameters = json.load(f)
                for parameter_name, parameter_value in parameters.get(
                    "parameters"
                ).items():
                    parameter_types[parameter_name] = str(
                        type(parameter_value).__name__
                    )
            print(parameter_types)

            # model content
            with open(f"{folder}model_petri.json", "r") as f:
                model_content = json.load(f)

            payload = json.dumps(
                {
                    "name": "Covid SIDARHTE",
                    "description": "Petri net model to predict covid movement patters in a community",
                    "content": json.dumps(model_content),
                    "framework": "Petri Net",
                    "parameters": parameter_types,
                }
            )
            headers = {"Content-Type": "application/json"}

            response = requests.request(
                "POST", url + "models", headers=headers, data=payload
            )
            model_json = response.json()
            model_id = model_json.get("id")
            print(f"model_id {model_id}")
            asset_to_project(project_id=1, asset_id=int(model_id), asset_type="model")

        except Exception as e:
            print(f"error opening {folder}document_doi.txt . - {e}")

        ## intermediates ##
        try:
            print("Upload intermediate mmt")
            with open(folder + "model_mmt_templates.json", "r") as f:
                mmt_template = json.load(f)

                payload = json.dumps(
                    {
                        "source": "mrepresentationa",
                        "type": "bilayer",
                        "content": json.dumps(mmt_template),
                    }
                )
            headers = {"Content-Type": "application/json"}

            response = requests.request(
                "POST", url + "intermediates", headers=headers, data=payload
            )
            intermediate_json = response.json()
            intermediate_id = intermediate_json.get("id")
            print(f"model_id {intermediate_id}")

            asset_to_project(
                project_id=1, asset_id=int(intermediate_id), asset_type="intermediate"
            )

        except Exception as e:
            print(e)

        try:
            print("Upload intermediate sbml")
            with open(folder + "model_sbml.xml", "r") as f:
                mmt_template = f.read()
                payload = json.dumps(
                    {
                        "source": "mrepresentationa",
                        "type": "sbml",
                        "content": mmt_template,
                    }
                )
            headers = {"Content-Type": "application/json"}

            response = requests.request(
                "POST", url + "intermediates", headers=headers, data=payload
            )
            intermediate_json = response.json()
            intermediate_id = intermediate_json.get("id")
            asset_to_project(
                project_id=1, asset_id=int(intermediate_id), asset_type="intermediate"
            )

        except Exception as e:
            print(e)

    ## now delete repo
    shutil.rmtree("experiments-main")
else:
    pass

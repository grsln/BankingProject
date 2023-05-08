import base64
import json
import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("send_allure")


def send_allure_reports():
    load_dotenv()
    project_id = os.getenv("PROJECT_ID")

    allure_results_directory = os.getenv("ALLURE_RESULTS_DIRECTORY")

    allure_server = os.getenv("ALLURE_SERVER")

    current_directory = Path(__file__).parent.parent
    results_directory = current_directory.joinpath(allure_results_directory)
    logger.info(f"RESULTS DIRECTORY PATH: {results_directory}")

    files = os.listdir(results_directory)

    logger.info("FILES:")
    results = []
    for file in files:
        result = {}

        file_path = results_directory.joinpath(file)
        logger.info(file_path)

        if os.path.isfile(file_path):
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                    if content.strip():
                        b64_content = base64.b64encode(content)
                        result["file_name"] = file
                        result["content_base64"] = b64_content.decode("UTF-8")
                        results.append(result)
                    else:
                        logger.info(f"Empty File skipped: {file_path}")
            finally:
                f.close()
        else:
            logger.info(f"Directory skipped: {file_path}")

    headers = {"Content-type": "application/json"}
    request_body = {"results": results}
    json_request_body = json.dumps(request_body)

    ssl_verification = False

    logger.info("------------------SEND-RESULTS------------------")
    response = requests.post(
        allure_server + "/allure-docker-service/send-results?project_id=" + project_id,
        headers=headers,
        data=json_request_body,
        verify=ssl_verification,
    )
    logger.info("STATUS CODE:")
    logger.info(response.status_code)
    logger.info("RESPONSE:")
    json_response_body = json.loads(response.content)
    json_prettier_response_body = json.dumps(
        json_response_body, indent=4, sort_keys=True
    )
    logger.info(json_prettier_response_body)

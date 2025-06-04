import shutil
import socket
import subprocess
import time
from io import StringIO

import allure
import pytest
import base64
import os

from loguru import logger

from driver_setup import get_driver


@pytest.fixture(scope='module')
def driver():
    # Start the Appium server
    appium_server = subprocess.Popen(['appium'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logger.info("Appium server started.")

    # Wait for the Appium server to be up and running
    for _ in range(30):  # Retry for up to 30 seconds
        try:
            with socket.create_connection(("localhost", 4723), timeout=1):
                logger.info("Appium server is up and running.")
                break
        except (ConnectionRefusedError, socket.timeout):
            time.sleep(1)
    else:
        logger.error("Appium server failed to start.")
        appium_server.terminate()
        appium_server.wait()
        raise RuntimeError("Appium server did not start.")

    try:
        driver = get_driver()
        yield driver
        driver.quit()
    finally:
        # Stop the Appium server
        appium_server.terminate()
        appium_server.wait()
        logger.info("Appium server stopped.")


@pytest.fixture(autouse=True)
def video(driver, request):
    # Start recording
    driver.start_recording_screen()
    yield
    # Stop recording
    video_raw = driver.stop_recording_screen()

    # Save video to current directory
    test_name = request.node.name
    video_path = f"artifacts/{test_name}.mp4"
    with open(video_path, "wb") as f:
        f.write(base64.b64decode(video_raw))

    # Attach video to Allure report
    with open(video_path, "rb") as f:
        allure.attach(f.read(), name=test_name, attachment_type=allure.attachment_type.MP4)


# Python
@pytest.fixture(autouse=True)
def logs(request):
    log_stream = StringIO()  # Create a stream to capture logs
    logger.add(log_stream, level="DEBUG")  # Redirect logs to the stream

    yield  # Yield control to the test

    # Retrieve all captured logs from the stream
    log_stream.seek(0)
    logs = log_stream.readlines()
    logger.remove()  # Remove the stream handler

    # Attach logs to Allure report
    log_content = "".join(logs)
    test_name = request.node.name
    allure.attach(log_content, name=test_name, attachment_type=allure.attachment_type.TEXT)


@pytest.fixture(scope='session', autouse=True)
def clean_allure_results():
    results_dir = "allure-results"
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
    os.makedirs(results_dir)


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """
    Hook to generate Allure report after all tests are finished.
    """
    results_dir = "allure-results"
    report_dir = "allure-report"

    if os.path.exists(results_dir):
        print("\nGenerating Allure report...")
        try:
            # Ensure the report directory exists
            os.makedirs(report_dir, exist_ok=True)

            subprocess.run(["allure", "generate", results_dir, "-o", report_dir, "--clean"], check=True)
            print(f"Allure report successfully generated at: {report_dir}")
            subprocess.Popen(["allure", "open", report_dir])
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate Allure report: {e}")
    else:
        print(f"No Allure results found in '{results_dir}'")


@pytest.fixture(autouse=True)
def last_screenshot(driver, request):
    yield  # Yield control to the test

    # Capture the screenshot after the test
    screenshot_path = f"artifacts/{request.node.name}_screenshot.png"
    driver.save_screenshot(screenshot_path)

    # Attach the screenshot to the Allure report
    with open(screenshot_path, "rb") as f:
        allure.attach(f.read(), name=f"{request.node.name}_screenshot", attachment_type=allure.attachment_type.PNG)


# Python
@pytest.fixture(scope='session', autouse=True)
def clean_artifacts():
    artifacts_dirs = [
        "artifacts",  # Directory for videos and screenshots
        "allure-results",  # Directory for Allure results
        "allure-report"  # Directory for Allure reports
    ]

    for dir_path in artifacts_dirs:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)  # Remove the directory if it exists
        os.makedirs(dir_path)  # Recreate the directory

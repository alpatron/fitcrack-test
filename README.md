# fitcrack-test

Automatic integration tests of [Fitcrack](https://github.com/nesfit/fitcrack). The tests test the system through the web front-end using [Selenium](https://www.selenium.dev/).

## Prerequisites 

* Python 3.11+
* Selenium [browser drivers](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/#3-the-path-environment-variable) located in PATH

## Setup and running 

Install `requirements.txt` with `pip install -r requirements.txt`.

Run `pytest --base-url [FITCRACK_URL] --driver [BROWSER] --credentials [USERNAME] [PASSWORD] to run all tests` to run all tests.

Replace `[FITCRACK_URL]` with the base URL where the instance of Fitcrack which should be tested is running; do not include a trailing slash (e.g. `https://fitcrack.foo`).

Replace `[BROWSER]` with the name of the web browser to be used for the test session (e.g. "Firefox", "chrome", "edge"). See [pytest-selenium docs](https://pytest-selenium.readthedocs.io/en/latest/user_guide.html#specifying-a-browser) for all browser options.

If the Fitcrack instance under test does not allow acces through the default username and password, add the `--credentials [USERNAME] [PASSWORD]` option with the username and password to be used by the tests.

You can edit `pytest.ini` to not have to include these options every time on the command line.

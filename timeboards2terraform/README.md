# Tooling

This directory contains tooling to turn DataDog resources into Terraform.

## Converting time boards with dd2tf.py

1. Make sure you've got the necessary dependencies (dotenv, Jinja2 and datadog) installed.

  * Install them manually
  ```bash
  pip install datadog Jinja2 python-dotenv
  ```
 * Alternatively, make user of `pipenv` and install in a virtualenv from the Pipfile.
1. Create a file called `.env` with valid values for the following two entries:
  ```
  DD_API_KEY=1234567890
  DD_APP_KEY=0987654321
  ```

1. It's then easy to run the script

  ```bash
  python ./dd2tf.py
  ```

  It should create a dump of the JSON for each time board in the account and a Terraform `.tf` file alongside of it in the `modules/dashboards/no_category` folder.
1. Copy the dashboards to the relevant locations in the `modules/dashboards` structure.

**NOTES:**

 * **The generated resource names might be invalid, you'll have to manually adjust them!**
 * Validate by running `terraform plan`. Because the graphs are a list, any changes by moving graphs around in the dashboard will reflect as a big number of changes when planning the Terraform run.

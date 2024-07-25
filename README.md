# Outlook Email Account Creator

This project automates the creation of Outlook email accounts using Selenium WebDriver. The script reads configuration settings from a `config.yaml` file, generates random user details, and logs the created accounts.

## Important

Update Google Chrome to the latest version to ensure good quality account creation and easier CAPTCHA solving. To update, navigate to `chrome://settings/help` and check for updates.

## Prerequisites

- Python 3.x
- Selenium WebDriver
- ChromeDriver
- A `config.yaml` file with the necessary configuration settings
- `names.txt` and `words5char.txt` files for generating random names and passwords

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/sujay1599/Outlook-Email-Creator.git
   cd Outlook-Email-Creator
   ```

2. **Install Required Packages**

   Install the necessary Python packages using pip:

   ```bash
   pip install selenium pyyaml
   ```

3. **Download ChromeDriver**

   Download the ChromeDriver executable and place it in the same directory as the script. Ensure the version of ChromeDriver matches your installed version of Google Chrome. [Download ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

4. **Run Configuration Script**

   Run the `config.py` script to generate the `config.yaml` file:

   ```bash
   python config.py
   ```

   The script will prompt you to input the necessary configuration settings and save them to a `config.yaml` file.

## Configuration File (`config.yaml`)

The configuration file (`config.yaml`) contains the settings needed for account creation:

```yaml
AUTO_CREATE: true
NUMBER_OF_ACCOUNTS: 5
FIRST_NAMES: ["John", "Jane"]
LAST_NAMES: ["Doe", "Smith"]
USER_PASSWORDS: ["password1", "password2"]
BIRTH_YEAR: 1990
BIRTH_MONTH: 1
BIRTH_DAY: 1
PROXIES: ["username:password@ip:port", "ip:port"]
```

## How It Works

1. **Load Configuration**: The script reads the `config.yaml` file to get the settings for account creation.
2. **Browser Setup**: It configures the Chrome browser with the specified options and proxies.
3. **Account Creation**: The script navigates to the Outlook signup page and fills out the form using the provided or randomly generated details.
4. **Logging**: Created account details are logged in the `data/accounts_log.csv` file.

## Usage

1. **Run the Main Script**

   Execute the main script using Python:

   ```bash
   python main.py
   ```

   The script will read the configuration settings, open a browser window, and begin creating Outlook email accounts. If `AUTO_CREATE` is set to `true`, it will generate random usernames and passwords. If `AUTO_CREATE` is set to `false`, it will use the names and passwords specified in the `config.yaml` file.

2. **Solve CAPTCHA**

   If a CAPTCHA is encountered during the account creation process, you will need to solve it manually. The script will pause and prompt you to press Enter after solving the CAPTCHA.

## Pitfalls

- **CAPTCHA Handling**: The script requires manual intervention to solve CAPTCHAs. Ensure you monitor the process and solve CAPTCHAs promptly to avoid timeouts.
- **Proxy Configuration**: Incorrect proxy settings can lead to errors. Double-check your proxy configuration in the `config.yaml` file.
- **Browser Compatibility**: Ensure your ChromeDriver version matches your installed version of Google Chrome to avoid compatibility issues.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

This project is inspired by and derived from the [microsoft-account-creator](https://github.com/silvestrodecaro/microsoft-account-creator) repository.
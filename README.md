# Flask Template

Basic flask template

## Installation and Running

1. Download the code from github

```bash
git clone git@github.com:rabramley/volca_sample_manager.git
```

2. Install the requirements

Go to the `flask_template` directory and type the command:

```bash
sudo apt install python3-dev libldap2-dev libsasl2-dev

pip install -r requirements.txt
```

3. Create the database using

Staying in the `flask_template` directory and type the command:

```bash
./manage.py version_control
./manage.py upgrade
```

4. Run the application

Staying in the `flask_template` directory and type the command:

```bash
./app.py
```

## Development

### Testing

To test the application, run the following command from the project folder:

```bash
pytest
```

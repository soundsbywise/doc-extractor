# Document Extraction Service

This repository contains the code for the Feathery Document Extraction Service.

Further details on this service can be found in the [Design Doc](https://plctrm.notion.site/Document-Extraction-Service-Design-Doc-4d6c86fb7c9844b683400aa4963468a6).

# Server

## System Requirements

These instructions assume you are on macOS or a Unix system.

It also assumes you have Python 3 (>= Python `3.9.6`) installed and running.

## Setup

### Quick Setup

Note: For your convenience, there is a setup script you can run in lieu of manually running the commands.

Please run this from the terminal in the repository root:

```
chmod +x server_setup.sh
./server_setup.sh
source venv/bin/activate
```

### Manual Setup

To get setup with the server, run the following instructions in your terminal.

_Note: The below snippets assume the repo root is your current directory._

1. Create a virtual environment:

   ```
   python3 -m venv {environment name, i.e. "venv"}
   ```

2. Activate your virtual environment

   ```
   source {environment name}/bin/activate
   ```

3. Install the dependencies from the `requirements.txt` file located in the `server/` directory:

   ```
   python3 -m pip install -r server/requirements.txt
   ```

   **Poppler**

   In addition to the Python requirements, to use the package `pdf2image`, you will need to install poppler.

   On macOS you can do this via homebrew by running `brew install poppler` from the terminal. More information is provided [here in the `pdf2image` README](https://github.com/Belval/pdf2image?tab=readme-ov-file#mac).

   Note: This might take a bit of time if homebrew wasn't updated recently.

### Environment Variables

**OpenAI API Key**

The `server` utilizes the OpenAI API which requires an API Key. You can get an API Key on the [API Keys page of OpenAI's website](https://platform.openai.com/api-keys).

Once retreived, place this key in the environment variable `OPENAI_API_KEY` on your system via the shell config (i.e. in ~/.zshrc, ~/.bashrc etc). _Note_: You will need to restart your terminal or source the profile after changing the config.

```
export OPENAI_API_KEY='<your-key>'
```

## Running the server locally

From you terminal, change directories to the `server/` directory:

```
cd server/
```

Then, run the following django command:

```
python3 manage.py runserver
```

The server should be running on port 8000 and you should be able to ping it via http://127.0.0.1:8000/ or http://localhost:8000.

# Client

The client application is an **example** NextJS application that makes use of the extractor service and a Feathery form.
It is meant to be a playground to show what kind of data is extracted by the service and how it might be displayed in a UX.

## System Requirements

These instructions assume you are running `node` version >= 21.5.0 and `npm` >= 10.2.4.

## Setup

Change directories into the `client/` directory and run the following command from your terminal:

```
npm install
```

This will install all of the dependencies.

## Running Locally

To run the NextJS application locally, from your terminal run the command:

```
npm run dev
```

The web application will be running at `http;//localhost:3000`.

**Note**: for the web app to work, the Django extractor service must also be running. See the **Server** section above for more details.

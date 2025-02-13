# Kate

[![check.yml](https://github.com/fmind/kate/actions/workflows/check.yml/badge.svg)](https://github.com/fmind/kate/actions/workflows/check.yml)
[![publish.yml](https://github.com/fmind/kate/actions/workflows/publish.yml/badge.svg)](https://github.com/fmind/kate/actions/workflows/publish.yml)
[![Documentation](https://img.shields.io/badge/documentation-available-brightgreen.svg)](https://fmind.github.io/kate/)
[![License](https://img.shields.io/github/license/fmind/kate)](https://github.com/fmind/kate/blob/main/LICENCE.txt)
[![Release](https://img.shields.io/github/v/release/fmind/kate)](https://github.com/fmind/kate/releases)

**Kate is a multimodal live assistant that can be used to discuss any website content.**

## Examples

**Kate Playlist**: https://www.youtube.com/playlist?list=PLPCnNL6Y2PbTzUxmsFICoQj0rx_PmVnk-

### Demo: Find Textbooks to Learn Web Programming

[![Kate Demo: Find Textbooks to Learn Web Programming - Multimodal Live Assistant](https://img.youtube.com/vi/fDf4KifJsrs/0.jpg)](https://www.youtube.com/watch?v=fDf4KifJsrs)

## Demo: Search Information about an Accounting Book

[![Kate Demo: Search Information about an Accounting Book - Multimodal Live Assistant](https://img.youtube.com/vi/nPvpDRi7L58/0.jpg)](https://www.youtube.com/watch?v=nPvpDRi7L58)

## Demo: Recommend Textbooks for Project Management

[![Kate Demo: Recommend Textbooks for Project Management - Multimodal Live Assistant](https://img.youtube.com/vi/mVU17Is7MsE/0.jpg)](https://www.youtube.com/watch?v=mVU17Is7MsE)

## Demo: Browse the Website FAQ

[![Kate Demo: Browse the Website FAQ - Multimodal Live Assistant](https://img.youtube.com/vi/EqPiIbgjP1w/0.jpg)](https://www.youtube.com/watch?v=EqPiIbgjP1w)

## Architecture: How it Works

[![Kate Architecture: How it Works - Multimodal Live Assistant](https://img.youtube.com/vi/_rwEV1aAvqc/0.jpg)](https://www.youtube.com/watch?v=_rwEV1aAvqc)

## Key Features

*   **AI-Powered Live Assistant:**  Kate acts as a helpful AI assistant, providing users with a natural language interface to search for and learn from websites.

*   **Multimodal Interaction:** Kate leverages [multimodal capabilities of Gemini 2.0](https://ai.google.dev/gemini-api/docs/multimodal-live), including audio transcription, text generation, and potentially visual elements (talking animation), to create an engaging and interactive user experience.

*   **Real-Time Communication Integration:**  Built on [pipecat](https://www.pipecat.ai/) framework, Kate seamlessly integrates with real-time communication platforms like Daily.co, allowing users to interact with the assistant within a live meeting or call.

*   **Website Search Tool:** Kate uses the [Vertex AI Search](https://cloud.google.com/enterprise-search?hl=en) to accurately search the website and provide users with precise answers to their queries.

*   **Customizable and Extensible:** The project is designed with modular components and uses environment variables for configuration, making it adaptable to different environments and use cases. New bots and tools can be created for new use cases.

*   **[Pipecat Framework](https://www.pipecat.ai/):** Utilizes the [pipecat framework](https://www.pipecat.ai/) to handle media and events.


## Dependencies

-   Python 3.12+
-   `invoke`
-   `uv`
-   `yarn` (for client-side dependencies)
-   Docker (for containerization)
-   Other dependencies are managed by `uv` and listed in `pyproject.toml`.

## Installation

```bash
git clone https://github.com/fmind/kate
```

```
uv sync --all-groups
```

## Development

```bash
inv runs.server
```

```bash
inv clients.dev
```

## Production

```bash
inv runs.server --mode=production
```

```bash
inv apps.expose
# ngrok start --config=ngrok.yml kate
```

## Tasks

The project uses `invoke` for task management. Here's an overview of the available tasks:

* Install tasks:
    * `inv installs.uv`: Install uv packages.
    * `inv installs.pre-commit`: Install pre-commit hooks on git.
    * `inv installs.all`: Run all install tasks.
* Server tasks:
    * `inv servers.run --mode=development`: Run the project server in development mode.
    * `inv servers.run --mode=production`: Run the project server in production mode.
    * `inv servers.all`: Run all server tasks.
* Spider tasks:
    * `inv spiders.otl`: Scrape Open Textbook Library dataset.
    * `inv spiders.all`: Run all spider tasks.
* Format tasks:
    * `inv formats.imports`: Format python imports with ruff.
    * `inv formats.sources`: Format python sources with ruff.
    * `inv formats.all`: Run all format tasks.
* Package tasks:
    * `inv packages.build`: Build the python package.
    * `inv packages.requirements`: Generate a requirements.txt.
    * `inv packages.all`: Run all package tasks.
* Client tasks:
    * `inv clients.install`: Install the project client.
    * `inv clients.dev`: Start the project client.
    * `inv clients.build`: Build the project client.
    * `inv clients.lint`: Lint the project client.
    * `inv clients.preview`: Preview the project client.
    * `inv clients.all`: Run all client tasks.
* Docs tasks:
    * `inv docs.serve --format=google --port=8088`: Serve the API docs with pdoc.
    * `inv docs.api --format=google --output_dir=docs/`: Generate the API docs with pdoc.
    * `inv docs.all`: Run all docs tasks.
* Checks tasks:
    * `inv checks.format`: Check the formats with ruff.
    * `inv checks.type`: Check the types with mypy.
    * `inv checks.code`: Check the codes with ruff.
    * `inv checks.test`: Check the tests with pytest.
    * `inv checks.security`: Check the security with bandit.
    * `inv checks.coverage`: Check the coverage with coverage.
    * `inv checks.all`: Run all check tasks.
* Container tasks:
    * `inv containers.compose`: Start up docker compose.
    * `inv containers.build --tag=latest`: Build the container image.
    * `inv containers.run --mode=production --port=8080 --tag=latest`: Run the container image.
    * `inv containers.all`: Run all container tasks.
* Clean tasks:
    * `inv cleans.mypy`: Clean the mypy tool.
    * `inv cleans.ruff`: Clean the ruff tool.
    * `inv cleans.pytest`: Clean the pytest tool.
    * `inv cleans.coverage`: Clean the coverage tool.
    * `inv cleans.dist`: Clean the dist folder.
    * `inv cleans.docs`: Clean the docs folder.
    * `inv cleans.cache`: Clean the cache folder.
    * `inv cleans.venv`: Clean the venv folder.
    * `inv cleans.uv`: Clean uv lock file.
    * `inv cleans.python`: Clean python caches and bytecodes.
    * `inv cleans.tools`: Run all tools tasks.
    * `inv cleans.folders`: Run all folders tasks.
    * `inv cleans.sources`: Run all sources tasks.
    * `inv cleans.all`: Run all tools and folders tasks.
    * `inv cleans.reset`: Run all tools, folders and sources tasks.
* App tasks:
    * `inv apps.expose`: Expose the application on the internet.
    * `inv apps.all`: Run all app tasks.

To execute a task, use the `inv` command followed by the task name (e.g., `inv checks.all`).

## Contributions

**We welcome contributions to enhance this project.**

Feel free to open issues or pull requests for any improvements, bug fixes, or feature requests.

## License

This project is licensed under the MIT License. See the ```LICENSE.txt``` file for details.

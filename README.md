# AI Threat Modeling action

[![Python package](https://github.com/xvnpw/ai-threat-modeling-action/actions/workflows/build.yaml/badge.svg)](https://github.com/xvnpw/ai-threat-modeling-action/actions/workflows/build.yaml)

🤖 You can use this GitHub Action to generate AI featured content for threat modeling and security review.

Supported features:
| Feature | Description |
| --- | --- |
| High Level Security and Privacy Requirements | Action will take project description and will use LLM to generate high level requirements regarding security and privacy |
| Threat Model of Architecture | Action will take architecture description and will use LLM to generate threat model for it |
| Security Acceptance Criteria for User Story | Action will take particular user story and generate security related acceptance criteria |

Table of content
===============
* [Example Outputs](#example-outputs)
  * [Feature: High Level Security and Privacy Requirements](#feature-high-level-security-and-privacy-requirements)
  * [Feature: Threat Model of Architecture](#feature-threat-model-of-architecture)
  * [Feature: Security Acceptance Criteria for User Story](#feature-security-acceptance-criteria-for-user-story)
* [Inputs](#inputs)
* [LLM Providers](#llm-providers)
* [Usage](#usage)
  * [High Level Security and Privacy Requirements](#high-level-security-and-privacy-requirements)
  * [Architecture Threat Model](#architecture-threat-model)
  * [Security Acceptance Criteria for User Story](#security-acceptance-criteria-for-user-story)
     * [Trigger on changes to directory](#trigger-on-changes-to-directory)
     * [Trigger on issue change](#trigger-on-issue-change)
  * [Push into Repository](#push-into-repository)
  * [Create Pull Request](#create-pull-request)
  * [Custom Prompts](#custom-prompts)
* [Roadmap](#-roadmap)
* [Tech Stack](#-tech-stack)
* [Fork](#fork)
* [Privacy](#privacy)
  * [OpenAI](#openai)
  * [OpenRouter](#openrouter)

## Example Outputs

### Feature: High Level Security and Privacy Requirements

| Model | Input | Output | 
| --- | --- | --- |
| **OpenAI GPT-3.5** | [PROJECT.md](https://github.com/xvnpw/ai-nutrition-pro-design-gpt3.5/blob/main/PROJECT.md) | [PROJECT_SECURITY.md](https://github.com/xvnpw/ai-nutrition-pro-design-gpt3.5/blob/main/PROJECT_SECURITY.md) or as [pull request](https://github.com/xvnpw/ai-nutrition-pro-design-gpt3.5/pull/2) |
| **Anthropic Claude 2** | [PROJECT.md](https://github.com/xvnpw/ai-nutrition-pro-design-claude2/blob/main/PROJECT.md) | [PROJECT_SECURITY.md](https://github.com/xvnpw/ai-nutrition-pro-design-claude2/blob/main/PROJECT_SECURITY.md) or as [pull request](https://github.com/xvnpw/ai-nutrition-pro-design-claude2/pull/1) |
| **OpenAI GPT-4** | [PROJECT.md](https://github.com/xvnpw/ai-nutrition-pro-design-gpt4/blob/main/PROJECT.md) | [PROJECT_SECURITY.md](https://github.com/xvnpw/ai-nutrition-pro-design-gpt4/blob/main/PROJECT_SECURITY.md) or as [pull request](https://github.com/xvnpw/ai-nutrition-pro-design-gpt4/pull/2) |

### Feature: Threat Model of Architecture

| Model | Input | Output | 
| --- | --- | --- |
| **OpenAI GPT-3.5** | [ARCHITECTURE.md](https://github.com/xvnpw/ai-nutrition-pro-design-gpt3.5/blob/main/ARCHITECTURE.md) | [ARCHITECTURE_SECURITY.md](https://github.com/xvnpw/ai-nutrition-pro-design-gpt3.5/blob/main/ARCHITECTURE_SECURITY.md) |
| **Anthropic Claude 2** | [ARCHITECTURE.md](https://github.com/xvnpw/ai-nutrition-pro-design-claude2/blob/main/ARCHITECTURE.md) | [ARCHITECTURE_SECURITY.md](https://github.com/xvnpw/ai-nutrition-pro-design-claude2/blob/main/ARCHITECTURE_SECURITY.md) |
| **OpenAI GPT-4** | [ARCHITECTURE.md](https://github.com/xvnpw/ai-nutrition-pro-design-gpt4/blob/main/ARCHITECTURE.md) | [ARCHITECTURE_SECURITY.md](https://github.com/xvnpw/ai-nutrition-pro-design-gpt4/blob/main/ARCHITECTURE_SECURITY.md) |

### Feature: Security Acceptance Criteria for User Story

| Model | Input | Output | 
| --- | --- | --- |
| **OpenAI GPT-3.5** | [0001_STORE_DIET_INTRODUCTIONS.md](https://github.com/xvnpw/ai-nutrition-pro-design-gpt3.5/blob/main/user-stories/0001_STORE_DIET_INTRODUCTIONS.md) or [issue](https://github.com/xvnpw/ai-nutrition-pro-design-gpt3.5/issues/1) | [0001_STORE_DIET_INTRODUCTIONS_SECURITY.md](https://github.com/xvnpw/ai-nutrition-pro-design-gpt3.5/blob/main/user-stories/0001_STORE_DIET_INTRODUCTIONS_SECURITY.md) or as [issue comment](https://github.com/xvnpw/ai-nutrition-pro-design-gpt3.5/issues/1) |
| **Anthropic Claude 2** | [0001_STORE_DIET_INTRODUCTIONS.md](https://github.com/xvnpw/ai-nutrition-pro-design-claude2/blob/main/user-stories/0001_STORE_DIET_INTRODUCTIONS.md) or [issue](https://github.com/xvnpw/ai-nutrition-pro-design-claude2/issues/2) | [0001_STORE_DIET_INTRODUCTIONS_SECURITY.md](https://github.com/xvnpw/ai-nutrition-pro-design-claude2/blob/main/user-stories/0001_STORE_DIET_INTRODUCTIONS_SECURITY.md) or as [issue comment](https://github.com/xvnpw/ai-nutrition-pro-design-claude2/issues/2) |
| **OpenAI GPT-4** | [0001_STORE_DIET_INTRODUCTIONS.md](https://github.com/xvnpw/ai-nutrition-pro-design-gpt4/blob/main/user-stories/0001_STORE_DIET_INTRODUCTIONS.md) or [issue](https://github.com/xvnpw/ai-nutrition-pro-design-gpt4/issues/1) | [0001_STORE_DIET_INTRODUCTIONS_SECURITY.md](https://github.com/xvnpw/ai-nutrition-pro-design-gpt4/blob/main/user-stories/0001_STORE_DIET_INTRODUCTIONS_SECURITY.md) or as [issue comment](https://github.com/xvnpw/ai-nutrition-pro-design-gpt4/issues/1) |

## Inputs

Add a step like this to your workflow:

```yaml
- uses: xvnpw/ai-threat-modeling-action@v1.2.6 # You can change this to use a specific version.
  with:
    # Type of feature, one of: project, architecture, user-story
    # Default: ''
    # Required
    type: 'project'

    # Provider name, one of: openai, openrouter
    # Default: 'openai'
    provider: 'openai'

    # Paths to input files formatted as json array
    # Default: ''
    input_files: '["PROJECT.md"]'

    # Path to output file
    # Default: ''
    output_file: 'PROJECT_SECURITY.md'

    # For USER STORY only! paths to architecture files formatted as json array
    # Default: ''
    input_architecture_files: '["ARCHITECTURE.md"]'

    # For USER STORY only! path to architecture threat model
    # Default: ''
    input_architecture_threat_model_file: 'ARCHITECTURE_SECURITY.md'

    # For USER STORY only! suffix that will be added to input file name to create output file
    # Default: '_SECURITY'
    user_story_output_suffix: '_SECURITY'

    # Type of OpenAI GPT model
    # Default: gpt-3.5-turbo
    # For openai models check: https://platform.openai.com/account/rate-limits
    # For openrouter models check: https://openrouter.ai/docs#models
    model: 'gpt-3.5-turbo-16k'

    # Sampling temperature for a model
    # Default: 0
    temperature: '0.3'

    # Verbose log messages
    # Default: false
    verbose: true

    # Debug log messages
    # Default: false
    debug: true

    # Prompt templates directory
    # Default: '/app/templates'
    # By default action will use prompt templates build-in docker image. You can specify your own without forking action.
    templates_dir: './templates'
  env:
    # OpenAI API key
    # Optional. Only if want to use openai provider
    # Get a key from https://platform.openai.com/account/api-keys
    # Add it to secrets in your repository settings
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

    # Open Router API key
    # Optional. Only if want to use openrouter provider
    # Get a key from https://openrouter.ai/keys
    # Add it to secrets in your repository settings
    OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
```

## LLM Providers

Currently supporting:
- [OpenAI](https://platform.openai.com/)
- [OpenRouter](https://openrouter.ai/)

## Usage

Action will generate `output_file` based on inputs. Using other actions you can:
- directly [push](#push-into-repository) into repository,
- create [pull request](#create-pull-request),
- or add comment to [issue](#trigger-on-issue-change).

### High Level Security and Privacy Requirements

If your input files are quite big you need to change `model` to one with bigger context, e.g. `gpt-3.5-turbo-16k`.

If you change input files, remember to change the trigger:
```yaml
on:
  push:
    branches:
      - main
    paths:
      - 'project-desc-1.md'
      - 'project-desc-2.md'
```

**Example (pull requests approach):**

```yaml
on:
  push:
    branches:
      - main
    paths:
      - 'PROJECT.md'

jobs:
  project_ai_devsecops_job:
    runs-on: ubuntu-latest

    permissions:
      # Give the default GITHUB_TOKEN write permission to commit and push the
      # added or changed files to the repository. Also permission to create/update
      # pull requests.
      contents: write
      pull-requests: write

    name: Run ai threat modeling action for project analysis
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3
      - name: Generate project security requirements
        uses: xvnpw/ai-threat-modeling-action@v1.2.6
        with:
          type: 'project'
          input_files: '["PROJECT.md"]'
          output_file: 'PROJECT_SECURITY.md'
          temperature: 0
          verbose: true
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      # Will use peter-evans/create-pull-request to create or update pull request
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          branch: create-pull-request/project
          title: (AI Generated) High Level Security and Privacy Requirements
          body: Automated pull request based on your changes to project. Please review it carefully.
          labels: 'security, ai'
```

### Architecture Threat Model

Check [High Level Security and Privacy Requirements](#high-level-security-and-privacy-requirements) for details about triggers and models.

**Example (direct push into repository):**

```yaml
on:
  push:
    branches:
      - main
    paths:
      - 'ARCHITECTURE.md'

jobs:
  architecture_ai_tm_job:
    runs-on: ubuntu-latest

    permissions:
      # Give the default GITHUB_TOKEN write permission to commit and push the
      # added or changed files to the repository.
      contents: write

    name: Will run ai threat modeling action for architecture analysis
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3
      - name: Generate architecture threat model
        uses: xvnpw/ai-threat-modeling-action@v1.2.6
        with:
          type: 'architecture'
          input_files: '["ARCHITECTURE.md"]'
          output_file: 'ARCHITECTURE_SECURITY.md'
          temperature: 0
          verbose: true
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      # Will use add-and-commit action to push output_file directly into repository
      - name: Commit changes
        uses: EndBug/add-and-commit@v9
        with:
          message: 'Project architecture threat model'
          add: 'ARCHITECTURE_SECURITY.md'
```

### Security Acceptance Criteria for User Story

Most useful usage is with [github issues](https://github.com/features/issues). But you can also generate output based on changes to particular directory (I did that in [research](https://github.com/xvnpw/ai-nutrition-pro-design-gpt3.5)).

User Stories feature requires two new parameters:
- `input_architecture_files` - json array of paths of input architecture files e.g. `["arch-1.md","arch-2.md"]`
- `input_architecture_threat_model_file` - path to architecture threat model e.g. `ARCHITECTURE_SECURITY.md`

and one optional:
- `user_story_output_suffix` - suffix that will be added to input file name to create output file, e.g. `_SECURITY`

#### Trigger on changes to directory

In case of user story, build is triggered on changes to particular directory. First, it needs to figure out which files were changed and process them individually.

As you can see, we don't use `input_files` parameter. This time we watch the whole directory for changes:

```yaml
on:
  push:
    branches:
      - main
    paths:
      - 'user-stories/*.md'
      - '!user-stories/*_SECURITY.md'
```

For your own directories, you need to adjust `paths` configuration. The same apply for committing changes with `add: 'user-stories/'`.

**Example (direct push into repository):**

```yaml
on:
  push:
    branches:
      - main
    paths:
      - 'user-stories/*.md'
      - '!user-stories/*_SECURITY.md'

jobs:
  user_story_ai_tm_job:
    runs-on: ubuntu-latest

    permissions:
      # Give the default GITHUB_TOKEN write permission to commit and push the
      # added or changed files to the repository.
      contents: write

    name: Will run ai threat modeling action for user story analysis
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3
      - name: Check which files were changed
        id: files_check
        uses: lots0logs/gh-action-get-changed-files@2.2.2
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      - name: Printing
        run: |
          echo "${{ steps.files_check.outputs.all }}"
      - name: Generate user story security acceptance criteria
        uses: xvnpw/ai-threat-modeling-action@v1.2.6
        with:
          type: 'user-story'
          input_files: "${{ steps.files_check.outputs.all }}"
          input_architecture_files: '["ARCHITECTURE.md"]'
          input_architecture_threat_model_file: "ARCHITECTURE_SECURITY.md"
          user_story_output_suffix: "_SECURITY"
          temperature: 0
          verbose: true
          model: "gpt-3.5-turbo-16k"
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      - name: Commit changes
        uses: EndBug/add-and-commit@v9
        with:
          message: 'User stories: security acceptance criteria'
          add: 'user-stories/'
```

#### Trigger on issue change

In this case we consider only stories with certain label:

```yaml
if: contains(github.event.issue.labels.*.name, 'ai-threat-modeling')
```

Comment is added (or updated) using [peter-evans/find-comment](https://github.com/peter-evans/find-comment) and [peter-evans/create-or-update-comment](https://github.com/peter-evans/create-or-update-comment) actions.

**Example (comment on issue):**

```yaml
name: Run ai threat modeling action for user story in issue analysis
on:
  issues:
    types:
      - labeled
      - edited

jobs:
  user_story_issue_ai_devsecops:
    name: Run ai threat modeling action for user story in issue analysis
    if: contains(github.event.issue.labels.*.name, 'ai-threat-modeling')
    runs-on: ubuntu-latest
    permissions:
      issues: write
      contents: write

    steps:
      - name: Checkout repo
        uses: actions/checkout@v3
      - uses: actions/github-script@v6
        id: set-result
        with:
          result-encoding: string
          retries: 3
          script: |
            const issue = await github.rest.issues.get({
              issue_number: ${{ github.event.issue.number }},
              owner: "${{ github.repository_owner }}",
              repo: "${{ github.event.repository.name }}",
            });
            const body = issue.data.body;
            const fs = require('fs');
            fs.writeFile('${{ github.workspace }}/issue_body.md', body, (err) => {
                if (err) throw err;
                console.log('Data written to file');
            });
            return JSON.stringify(body);
      - name: Generate user story security acceptance criteria
        uses: xvnpw/ai-threat-modeling-action@v1.2.6
        with:
          type: 'user-story'
          input_files: '["issue_body.md"]'
          input_architecture_files: '["ARCHITECTURE.md"]'
          input_architecture_threat_model_file: "ARCHITECTURE_SECURITY.md"
          temperature: 0
          verbose: true
          model: "gpt-3.5-turbo-16k"
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      - name: Find Comment
        uses: peter-evans/find-comment@v2
        id: fc
        with:
          issue-number: ${{ github.event.issue.number }}
          comment-author: 'github-actions[bot]'
          body-includes: (AI Generated) Security Related Acceptance Criteria
      - name: Add comment
        uses: peter-evans/create-or-update-comment@v3
        with:
          comment-id: ${{ steps.fc.outputs.comment-id }}
          issue-number: ${{ github.event.issue.number }}
          body-path: ${{ github.workspace }}/issue_body_SECURITY.md
          edit-mode: replace
```

### Push into Repository

With [Add & Commit](https://github.com/marketplace/actions/add-commit) you can get `output_file` easily committed into repository:

```yaml
      - name: Commit changes
        uses: EndBug/add-and-commit@v9
        with:
          message: 'Project architecture threat model'
          add: 'ARCHITECTURE_SECURITY.md'
```

If you change output file, remember to change commit file:
```yaml
      - name: Commit changes
        uses: EndBug/add-and-commit@v9
        with:
          message: 'Project security requirements'
          add: 'project-sec-reqs.md'
```

### Create Pull Request

With [Create Pull Request](https://github.com/marketplace/actions/create-pull-request) you can create new pull request with `output_file`:

```yaml
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          branch: create-pull-request/project
          title: (AI Generated) High Level Security and Privacy Requirements
          body: Automated pull request based on your changes to project. Please review it carefully.
          labels: 'security, ai'
```

In this mode, you also need to adjust permissions for workflow:

```yaml
    permissions:
      # Give the default GITHUB_TOKEN write permission to commit and push the
      # added or changed files to the repository.
      # It has also permission to pull requests
      contents: write
      pull-requests: write
```

Also [change settings](https://github.com/marketplace/actions/create-pull-request#workflow-permissions) for actions.

### Custom Prompts

You might want to tune prompts. To do so, you don't need to fork action, but provide templates directory into your target repository:

```bash
cd $HOME/<projects> # your directory with repositories
git clone git@github.com:xvnpw/ai-threat-modeling-action.git
cp -r ai-threat-modeling-action/templates <target-repo>/
cd <target-repo>/templates
# edit templates
```

In workflow file add:

```yaml
uses: xvnpw/ai-threat-modeling-action@v1.2.6
with:
  ...
  templates_dir: './templates'
```

`./templates` - is directory relative to `<target-repo>` root.

## 🎉 Roadmap

This project started as research of LLMs capabilities, but it improved over time beyond simple PoC. With version 1, it can be used to review documents in github using direct push, pr or issues. Further development will depend on usage and feature requests from community. 

## 🚀 Tech Stack

- Python
- LLM Tooling: [Langchain](https://github.com/hwchase17/langchain)
- LLM: [OpenAI GPT](https://openai.com/), [OpenRouter](https://openrouter.ai/)

## Fork

Fork this project. Edit files and release action:

```
git add .
git commit -m "My first action is ready"
git tag -a -m "My first action release" v1
git push --follow-tags
```

## Privacy

### OpenAI

This project uses OpenAI API. By default your data will not be used for learning, as per [API data usage policies](https://openai.com/policies/api-data-usage-policies):
> OpenAI will not use data submitted by customers via our API to train or improve our models, unless you explicitly decide to share your data with us for this purpose. You can opt-in to share data.

### OpenRouter

OpenRouter describe privacy and filtering in [settings](https://openrouter.ai/account) for each model.

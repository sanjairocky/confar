# How To Run

## Parse & aggregate configuration

```bash
confar parse <file>
```

## Parse & run the configuration

```bash
confar run <file>
```

## Web - UI to run the configuration (comming soon)

```bash
confar web
```

# Flow Configuration Documentation

This documentation explains the structure of a YAML file used for configuring flows. The YAML file includes various flow configurations under the flows key.

## Flows

The flows section defines different flow configurations, each identified by a unique name. Each flow consists of a list of steps that define the sequence of actions to be executed.

### Example:

```yaml
flows:
  echo:
    - name: shell exe
      shell: pwd
    # ...
  default:
    - name: calling flow
      call: echo
    # ...
  # ...
```

- flows (Dictionary): This section contains flow configurations, each with a unique name.
  - Flow Name (Dictionary Key): The name of the flow configuration.
    - name (String): The name of the step within the flow.
    - shell (String): A shell command to execute in this step.
    - call (String): Name of the sub-flow to call in this step.
    - if (Dictionary): A conditional block specifying whether to execute this step based on conditions.
    - then (List): A list of steps to execute if the condition is true.
    - else (List): A list of steps to execute if the condition is false.

## Default Flow

The default flow is a special flow that defines the steps to execute when no specific flow is specified. It is used as a fallback.

## Environment (env)

The env section defines environment variables that can be used within steps of the flows.

### Example

```yaml
env:
  - name: shell with env
    shell: echo {$.envd}
  - name: env adding
    env:
      envd: ${PWD}-{$.obj[test]}
  - name: shell with env
    shell: echo {$.envd}
```

- env (List): This section contains a list of environment variable configurations.
  - name (String): The name of the environment variable.
  - shell (String): A shell command that uses the environment variable.

## Conditionals (if)

The if section defines conditional statements that determine whether to execute certain steps based on conditions.

### Example:

```yaml
if:
  - name: conditional flow if
    if: $.ar and not len($.ar)
    then:
      - name: passed hello
        shell: echo {$.obj[test]}
```

- if (List): This section contains a list of conditional block configurations.
  - name (String): A name for the conditional block.
  - if (String): The condition to evaluate. It uses JSONPath expressions.
  - then (List): A list of steps to execute if the condition is true.
  - else (List): A list of steps to execute if the condition is false.

## Over All Example

```yaml
# Scenario 1: Basic Shell Commands
flows:
  echo:
    - name: shell exe
      shell: pwd
    - name: shell with env
      shell: echo {$.hello}

# Scenario 2: Conditional Flows
if:
  - name: conditional flow if
    if: $.ar and not len($.ar)
    then:
      - name: passed hello
        shell: echo {$.obj[test]}

  - name: conditional flow if .. else
    if: $.hello
    then:
      - name: passed if
        shell: echo "passed if"
    else:
      - name: passed if .. else
        shell: echo "passed if .. else"

  - name: conditional flow else .. if .. else
    if: $.hello
    then:
      - name: passed hello
        shell: echo "passed hello"
    else:
      - if: $.hello
        then:
          - name: passed if .. else
            shell: echo "passed if .. else"
        else:
          - name: passed hello
            shell: echo "passed hello"

# Scenario 3: Sub-Flows (including Default Flow)
flows:
  default:
    - name: calling flow
      call: echo
    - name: another step
      shell: echo "Another step in the default flow"

# Scenario 4: Environment Variables
env:
  - name: shell with env
    shell: echo {$.envd}
  - name: env adding
    env:
      envd: ${PWD}-{$.obj[test]}
  - name: shell with env
    shell: echo {$.envd}
```

This documentation provides an overview of the structure and purpose of the YAML configuration file used for defining flows and their associated actions. It can serve as a reference for users or developers working with these configurations.

# New York City Taxi and Limousine Commission (TLC) trip demo project

## How to run the demo

**⚠️ You need Python >= 3.8**

0. Create a virtual env, and activate
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
    
1. Install project and dependencies
    ```bash
    # 'EXTRA_INDEX_URL' will be provided.
    python -m pip install -r requirements.txt --extra-index-url=${EXTRA_INDEX_URL}
    python -m pip install -e .
    ```
    You may want to install these dependencies in a virtual environment, in which case you should enter this command first:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2. Initialize spice store (Needs to be done only once)
    ```
    spice store init
    ```

3. Run the demo
    ```bash
    python -m src.main
    ```

4. Check the UI
    ```bash
    spice ui
    ```

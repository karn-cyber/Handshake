#!/bin/bash
# Verifier entrypoint. Runs the output checks, emits a CTRF report, and always
# (re)writes the reward so it never trusts anything the agent may have left behind.
#
# pytest and pytest-json-ctrf are baked into the environment image
# (see environment/Dockerfile), so no network access is required here.

# Harbor reads the reward and the CTRF report from /logs/verifier.
mkdir -p /logs/verifier

pytest /tests/test_outputs.py -rA --ctrf /logs/verifier/ctrf.json
status=$?

if [ "$status" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi

exit 0

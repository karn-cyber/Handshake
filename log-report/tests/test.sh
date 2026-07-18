#!/bin/bash
# Verifier entrypoint. pytest and pytest-json-ctrf are baked into the single
# environment/Dockerfile, so this runs plain pytest with no verify-time installs.
# It emits a CTRF report and always (re)writes the reward, never trusting any
# reward file the agent may have left behind.

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

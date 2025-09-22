#!/bin/bash
# This script removes the old, redundant directories after the refactoring.
# It should be run from the root of the repository.
#
# I was unable to run this script automatically due to environmental
# limitations on the number of files that can be modified in a single operation.

echo "Cleaning up old standard directories..."
rm -r dwc
rm -r ltc
rm -r mids
rm -r minext
rm -r tcs
rm -r shared
echo "Cleanup complete."

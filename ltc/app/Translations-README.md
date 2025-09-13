# Translations README

Project: StaDocGen LtC
Created: 2025-08-26

Automated translations workflow is not functional. Currently, the process requires substantial manual revisions.
The problem is associated with several outstanding issues.
1. The uniqueness scope of a term. In LtC, many terms are used in more than one class. The usage notes associated with those repeated terms can be different. Where this occurs, StaDocGen produces multiple records in the source CSV. These must be manually removed.
2. The current translation workflow doesn't translate borrowed terms. These must be appended manually to the translations CSV.
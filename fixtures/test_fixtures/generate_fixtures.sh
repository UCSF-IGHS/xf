#!/usr/bin/env bash
#dumpdata --natural-foreign --exclude auth.permission --exclude contenttypes --indent 4 > uc_dashboards/fixtures/test_fixtures/testdata.json

#this doesn't work yet – content types throws a bug and auth.permission needs to be excluded for now
dumpdata contenttypes --indent 4 > uc_dashboards/fixtures/test_fixtures/contenttypes.json
dumpdata auth --exclude auth.permission --indent 4 > uc_dashboards/fixtures/test_fixtures/auth.json
dumpdata uc_dashboards --indent 4 > uc_dashboards/fixtures/test_fixtures/uc_dashboards.json

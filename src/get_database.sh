#!/bin/sh
rm database_buf.json
curl --get --include 'https://omgvamp-hearthstone-v1.p.mashape.com/cards' \
  -H 'X-Mashape-Key: fKjbakCDMymshCbUBwGgQLr7hlhEp1gWIYdjsn4iPqtgINyrl3' > database_buf.json

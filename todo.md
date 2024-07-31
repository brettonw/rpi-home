# TODO
- figure out how to use the driver name and version - should that be included in their report?
- figure out how to do a sensor or control history
- figure out how to do controls...
- put the logging level in the settings inside config.json
- use zeroconf to publish the presence of a new client
  - publish presence until a server reaches out to say hello, then stop
  - server browses for new publications once every few minutes?
  - if haven't been polled by a server in some time, republish
  - use server hello to publish mqtt credentials?

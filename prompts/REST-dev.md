---
description: Build basic REST services to interact with tables in InterSystems' IRIS database
argument-hint: "[extra constraints]"
---
You are working in the current project.

Goal:
Create basic REST services to interact with the tables  MLpipeline.PointSamples and MLpipeline.Predictions in InterSystems' IRIS database.
- services: GET, POST, DELETE

Requirements:
- all the commands to create a web application in IRIS terminal should be added to `dur/sandbox/webappconf.sh`, and executed by runing that file inside the container for reproducibility
- creation of a dispatch class that should be placed exactly in `REST/DispatchClass.cls`. For For guidance I provided the dispatch class that resulted from a tutorial that i followed, which you can find in the /REST_example folder. in `../REST_example/guidetext_example.md` is the guide instructions, and in `../REST_example/exampleDispatchClass.cls is` the resulting dispatch class for the web app created during the tutorial. however some steps require manual use of the Management Portal UI, which you might not be able to do, so you will have to figure out in the documentation how to achieve this through the IRIS terminal using the provided documentation.

Documentation requirements (read before and during edits):
- `isc-documentation/InterSystems IRIS for Health 2026.1/Development`
- Follow relevant markdown cross-references when needed.

Validation loop (required after each significant change):
```bash
PPROPOSE REASONABLE VALIDATION LOOP
```
- Iterate until validator exit code is `0`.
- Do not claim success unless exit code is `0`.

Authoring guidance:
- Prefer deterministic mappings from source fields.
- If fixture-specific literals are required (constants or fixed timestamps), add explicit DTL `<comment><annotation>...</annotation></comment>` near those `<assign>` actions explaining why.
- Avoid non-deterministic values (current time/random).

When done, provide:
1) dispatch class in `REST/DispatchClass.cls`
2) bash file with all IRIS-specific commands in `dur/sandbox/webappconf.sh` to create the web application.
2) documentation generated using IRIS as done in the `../REST_example/guidetext_example.md` tutorial
3) Markdown in `/REST` explaining in plain text your approach

Extra user constraints: $@

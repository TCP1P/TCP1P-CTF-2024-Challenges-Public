#!/bin/bash
/bin/su -s /bin/bash -c "uvicorn server:app --host 0.0.0.0 --port 8000" nobody

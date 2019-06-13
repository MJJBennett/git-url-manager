#!/bin/bash
if [ -d "~/programming/tools/bin/" ]; then
    chmod +x gitify.py
    cp gitify.py ~/programming/tools/bin/gitify
else
    echo "Manual install required, or run `mkdir -p ~/programming/tools/bin/` and rerun install." 
fi

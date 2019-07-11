echo "Waiting 60 seconds to start CI Test Server"
sleep 50s
echo "Starting CI Test Server"

pytest

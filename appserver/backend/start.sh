if [ -f $D3MCONFIG ]; then
	rm $D3MCONFIG
fi
echo "[Data]" >> $D3MCONFIG
echo "dataset_root = $D3MINPUTDIR" >> $D3MCONFIG
echo "out_dir_root = $D3MOUTPUTDIR" >> $D3MCONFIG
echo "[TA2]" >> $D3MCONFIG
echo "ta2_url = $TA2ADDR" >> $D3MCONFIG
echo "ta2_name = $TA2NAME" >> $D3MCONFIG
echo "mode = D3M" >> $D3MCONFIG


# Write Docker env variables to config file
dockerconfig="/app/docker_config.cfg"
echo "[frontend]" >> $dockerconfig
echo "HOST_URL=$FRONTEND_HOST_URL" >> $dockerconfig
echo "EXTERNAL_URL=$FRONTEND_URL" >> $dockerconfig
echo "[backend]" >> $dockerconfig
echo "HOST_URL=$BACKEND_HOST_URL" >> $dockerconfig
echo "EXTERNAL_URL=$BACKEND_URL" >> $dockerconfig
echo "[db]" >> $dockerconfig
echo "HOST_URL=$DB_HOST_URL" >> $dockerconfig
echo "[viz]" >> $dockerconfig
echo "HOST_URL=$VIZ_HOST_URL" >> $dockerconfig
echo "EXTERNAL_URL=$VIZ_URL" >> $dockerconfig

# Start the python server
python3 app.py

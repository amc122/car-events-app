source get_dataset.sh
docker build -t car-events-app:20220504 -f Dockerfile .
rm -rf tmp
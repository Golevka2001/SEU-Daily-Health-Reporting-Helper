WORKDIR="$( cd "$( dirname "$0"  )" && pwd  )"
docker run --rm -v ${WORKDIR}:/workspace/SEU-health-reporting-helper dhrh:0.1 python3 main.py
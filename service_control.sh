start() {
    docker compose -f vl_infrastructure/docker-compose.yml up --pull always -d
}

stop() {
    docker compose -f vl_infrastructure/docker-compose.yml down
    sleep 10
}

sync() {
    cd vl_infrastructure
    git pull
}

case "$1" in
    (start)
        start
        ;;
    (stop)
        stop
        ;;
    (sync)
        sync
        ;;
    (*)
        echo "Использование: $0 {start|stop}"
        exit 1
        ;;
esac

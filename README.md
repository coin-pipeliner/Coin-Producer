# Coin-Producer
- kafka-cluster와 연결 성공
- kafka-cluster 는 docker-compose로 구현했고 producer는 그냥 도커 컨테이너 단위로 실행시키게 했다. 이유는 producer는 원하는 개수만큼 나중에 동적으로 컨테이너를 생성해야하기 때문에??
- 그래서 docker-compose 와 개개인의 container의 네트워크 연결을 위해 custom network를 만들고 그안에 다 매핑시켰다.
### 현재까지의 가정
- topic name 과 받아오는 코인 종류는 BTC_KRW (나중에 인자값으로 받아오면 될듯하다)

## 실행방법  
1. 커스텀 네트워크 생성
```shell
docker network create coin-pipeliner
```

2. producer 이미지 빌드
```shell
 docker build . -t moggaa/coin-producer 
```

3. 카프카 클러스터 실행
```shell
docker-compose up --build -d 
```

4. 카프카 토픽 생성
```shell
docker-compose exec kafka1 kafka-topics --create --if-not-exists --zookeeper zk1:2181 --partitions 1 --replication-factor 1 --topic BTC_KRW
```

5. 프로듀서 컨테이너 실행 (마지막 인자값 받아올 데이터 개수)
```shell
docker run  --network coin-pipeliner --name producer -p 9001:9001 -t moggaa/coin-producer 10   
```


6. 테스트용 컨슈머 콘솔 실행
```shell
docker-compose exec kafka1 kafka-console-consumer --bootstrap-server kafka1:19091 kafka2:19092 kafka3:19093  --topic BTC_KRW  --from-beginning
```
 
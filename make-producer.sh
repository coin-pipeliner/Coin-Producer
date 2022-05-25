while read -r line || [ -n "$line" ]  ; do 
  docker build --build-arg arg=$(echo "$line" | tr -d '\r') . -t coin-producer-$(echo "$line" | tr -d '\r') 
  docker run -d coin-producer-$(echo "$line" | tr -d '\r')
done < coin.txt
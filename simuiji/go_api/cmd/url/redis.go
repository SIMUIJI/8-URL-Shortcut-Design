package url

import (
	"api/go_api/config"
	"context"
	"fmt"
)

func InsertRedis(key, value string) {
	// 키-값 설정
	rdb := config.Cache()
	ctx := context.Background()

	err := rdb.Set(ctx, key, value, 0).Err()
	if err != nil {
		panic(err)
	}
}

func GetRedisByKey(key string) string {
	// 값 가져오기
	rdb := config.Cache()
	ctx := context.Background()
	longUrl, err := rdb.Get(ctx, key).Result()
	if err != nil {
		fmt.Println(err)
	}
	return longUrl
}

package config

import (
	"fmt"
	"github.com/redis/go-redis/v9"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var database *gorm.DB
var insertDb *gorm.DB
var cache *redis.Client

var e error

func DatabaseInit() {
	host := "172.19.0.6"
	//host := "127.0.0.1"
	user := "snj"
	password := "snj"
	dbName := "snj_db"
	port := 5432

	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%d sslmode=disable TimeZone=Asia/Jakarta", host, user, password, dbName, port)
	database, e = gorm.Open(postgres.Open(dsn), &gorm.Config{})

	host = "172.19.0.6"
	dsn = fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%d sslmode=disable TimeZone=Asia/Jakarta", host, user, password, dbName, port)
	insertDb, e = gorm.Open(postgres.Open(dsn), &gorm.Config{})

	if e != nil {
		panic(e)
	}
}

func CacheInit() {
	cache = redis.NewClient(&redis.Options{
		Addr:     "172.19.0.7:6379", // Redis 서버 주소
		Password: "snj",             // 비밀번호가 없다면 빈 문자열
	})

}

func DB() *gorm.DB {
	return database
}

func IDB() *gorm.DB {
	return insertDb
}

func Cache() *redis.Client {
	return cache
}

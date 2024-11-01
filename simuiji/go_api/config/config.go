package config

import (
	"fmt"
	"github.com/redis/go-redis/v9"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"os"
)

var database *gorm.DB
var cache *redis.Client

var e error

func init() {
	DatabaseInit()
	CacheInit()
}

func DatabaseInit() {
	host := os.Getenv("DB_HOST")
	user := os.Getenv("DB_USER")
	password := os.Getenv("DB_PASSWORD")
	dbName := os.Getenv("DB_NAME")
	port := os.Getenv("DB_PORT")

	connectInfo := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%d sslmode=disable TimeZone=Asia/Jakarta", host, user, password, dbName, port)
	database, e = gorm.Open(postgres.Open(connectInfo), &gorm.Config{})

	if e != nil {
		panic(e)
	}
}

func CacheInit() {
	connectInfo := fmt.Sprintf("%s:%d", os.Getenv("REDIS_HOST"), os.Getenv("REDIS_PORT"))
	cache = redis.NewClient(&redis.Options{
		Addr:     connectInfo,                 // Redis 서버 주소
		Password: os.Getenv("REDIS_PASSWORD"), // 비밀번호가 없다면 빈 문자열
	})

}

func DB() *gorm.DB {
	return database
}

func Cache() *redis.Client {
	return cache
}

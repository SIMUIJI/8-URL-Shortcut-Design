package db

import (
	"api/go_api/config"
	"api/go_api/model"
	"context"
	"fmt"
	"github.com/labstack/echo/v4"
	"net/http"
	"time"
)

func CreateUrl(c echo.Context) error {
	b := new(model.Url)
	db := config.IDB()

	// Binding data
	if err := c.Bind(b); err != nil {
		data := map[string]interface{}{
			"message": err.Error(),
		}

		return c.JSON(http.StatusInternalServerError, data)
	}
	shortUrl := "test123"
	url := &model.Url{
		ShortUrl: shortUrl,
		LongUrl:  b.LongUrl,
		IsEnable: b.IsEnable,
		RegDate:  time.Now(),
	}

	if err := db.Create(&url).Error; err != nil {
		data := map[string]interface{}{
			"message": err.Error(),
		}

		return c.JSON(http.StatusInternalServerError, data)
	}

	// 키-값 설정
	rdb := config.Cache()
	ctx := context.Background()

	err := rdb.Set(ctx, b.LongUrl, b.ShortUrl, 0).Err()
	if err != nil {
		panic(err)
	}

	response := map[string]interface{}{
		"shortUrl": shortUrl,
	}

	return c.JSON(http.StatusOK, response)
}

func UpdateUrl(c echo.Context) error {
	id := c.Param("url_id")
	b := new(model.Url)
	db := config.DB()

	// Binding data
	if err := c.Bind(b); err != nil {
		data := map[string]interface{}{
			"message": err.Error(),
		}

		return c.JSON(http.StatusInternalServerError, data)
	}

	existing_url := new(model.Url)

	if err := db.First(&existing_url, id).Error; err != nil {
		data := map[string]interface{}{
			"message": err.Error(),
		}

		return c.JSON(http.StatusNotFound, data)
	}

	existing_url.ShortUrl = b.ShortUrl
	existing_url.LongUrl = b.LongUrl
	existing_url.IsEnable = b.IsEnable
	if err := db.Save(&existing_url).Error; err != nil {
		data := map[string]interface{}{
			"message": err.Error(),
		}

		return c.JSON(http.StatusInternalServerError, data)
	}
	// 키-값 설정
	rdb := config.Cache()
	ctx := context.Background()

	err := rdb.Set(ctx, b.LongUrl, b.ShortUrl, 0).Err()
	if err != nil {
		panic(err)
	}

	response := map[string]interface{}{
		"data": existing_url,
	}

	return c.JSON(http.StatusOK, response)
}

func GetUrl(c echo.Context) error {

	shortUrl := c.Param("short_url")
	// 키-값 설정
	rdb := config.Cache()
	ctx := context.Background()

	// 값 가져오기
	longUrl, err := rdb.Get(ctx, shortUrl).Result()
	if err != nil {
		fmt.Println(err)
	}
	if longUrl == "" {
		var url []*model.Url
		db := config.DB()
		if res := db.Where("short_url = ?", shortUrl).Find(&url); res.Error != nil {
			data := map[string]interface{}{
				"message": res.Error.Error(),
			}

			return c.JSON(http.StatusOK, data)
		}
		longUrl = url[0].LongUrl

		err = rdb.Set(ctx, shortUrl, longUrl, 0).Err()
		if err != nil {
			panic(err)
		}
	}
	return c.Redirect(http.StatusMovedPermanently, longUrl)
}

func DeleteUrl(c echo.Context) error {
	id := c.Param("url_id")
	db := config.DB()

	url := new(model.Url)

	err := db.Delete(&url, id).Error
	if err != nil {
		data := map[string]interface{}{
			"message": err.Error(),
		}

		return c.JSON(http.StatusInternalServerError, data)
	}

	response := map[string]interface{}{
		"message": "a book has been deleted",
	}
	return c.JSON(http.StatusOK, response)
}

package cmd

import (
	"api/go_api/db"
	"api/go_api/model"
	"github.com/labstack/echo/v4"
	"net/http"
)

func CreateUrl(c echo.Context) error {
	b := new(model.Url)
	if err := c.Bind(b); err != nil {
		data := map[string]interface{}{
			"message": err.Error(),
		}

		return c.JSON(http.StatusInternalServerError, data)
	}
	shortUrl, err := db.Create(b)
	if err != nil {
		data := map[string]interface{}{
			"message": err.Error(),
		}
		return c.JSON(http.StatusInternalServerError, data)
	}
	db.InsertRedis(b.ShortUrl, b.LongUrl)

	response := map[string]interface{}{
		"shortUrl": shortUrl,
	}

	return c.JSON(http.StatusOK, response)
}

func GetUrl(c echo.Context) error {
	var err error
	shortUrl := c.Param("short_url")
	longUrl := db.GetRedisByKey(shortUrl)

	if longUrl == "" {
		longUrl, err = db.Get(shortUrl)
		if err != nil {
			data := map[string]interface{}{
				"message": err,
			}
			return c.JSON(http.StatusOK, data)
		}
		db.InsertRedis(shortUrl, longUrl)
	}

	return c.Redirect(http.StatusMovedPermanently, longUrl)
}

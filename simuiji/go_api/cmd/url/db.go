package url

import (
	"api/go_api/config"
	"api/go_api/internal"
	"time"
)

func Create(data *Url) (string, error) {
	db := config.DB()
	shortUrl := internal.MakeShortUrl()
	url := &Url{
		ShortUrl: shortUrl,
		LongUrl:  data.LongUrl,
		IsEnable: data.IsEnable,
		RegDate:  time.Now(),
	}
	if err := db.Create(&url).Error; err != nil {
		return "", err
	}

	return shortUrl, nil
}

func Get(shortUrl string) (string, error) {
	var url []*Url
	db := config.DB()
	if res := db.Where("short_url = ?", shortUrl).Find(&url); res.Error != nil {
		return "", res.Error
	}
	return url[0].LongUrl, nil
}

//
//func DeleteUrl(c echo.Context) error {
//	id := c.Param("url_id")
//	db := config.DB()
//
//	url := new(model.Url)
//
//	err := db.Delete(&url, id).Error
//	if err != nil {
//		data := map[string]interface{}{
//			"message": err.Error(),
//		}
//
//		return c.JSON(http.StatusInternalServerError, data)
//	}
//
//	response := map[string]interface{}{
//		"message": "a book has been deleted",
//	}
//	return c.JSON(http.StatusOK, response)
//}
//
//
//func UpdateUrl(c echo.Context) error {
//	id := c.Param("url_id")
//	b := new(model.Url)
//	db := config.DB()
//
//	// Binding data
//	if err := c.Bind(b); err != nil {
//		data := map[string]interface{}{
//			"message": err.Error(),
//		}
//
//		return c.JSON(http.StatusInternalServerError, data)
//	}
//
//	existing_url := new(model.Url)
//
//	if err := db.First(&existing_url, id).Error; err != nil {
//		data := map[string]interface{}{
//			"message": err.Error(),
//		}
//
//		return c.JSON(http.StatusNotFound, data)
//	}
//
//	existing_url.ShortUrl = b.ShortUrl
//	existing_url.LongUrl = b.LongUrl
//	existing_url.IsEnable = b.IsEnable
//	if err := db.Save(&existing_url).Error; err != nil {
//		data := map[string]interface{}{
//			"message": err.Error(),
//		}
//
//		return c.JSON(http.StatusInternalServerError, data)
//	}
//	// 키-값 설정
//	rdb := config.Cache()
//	ctx := context.Background()
//
//	err := rdb.Set(ctx, b.LongUrl, b.ShortUrl, 0).Err()
//	if err != nil {
//		panic(err)
//	}
//
//	response := map[string]interface{}{
//		"data": existing_url,
//	}
//
//	return c.JSON(http.StatusOK, response)
//}

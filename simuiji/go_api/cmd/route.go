package cmd

import (
	"api/cmd/url"
	"github.com/labstack/echo/v4"
)

func UrlRoute(e *echo.Echo) {
	urlRoute := e.Group("/api/v1")
	urlRoute.POST("/shorten", url.CreateUrl)
	urlRoute.GET("/:short_url", url.GetUrl)
	//urlRoute.PUT("/:long_url", db.UpdateUrl)
	//urlRoute.DELETE("/:long_url", db.DeleteUrl)
}

package route

import (
	"api/go_api/cmd"
	"github.com/labstack/echo/v4"
)

func UrlRoute(e *echo.Echo) {
	urlRoute := e.Group("/api/v1")
	urlRoute.POST("/shorten", cmd.CreateUrl)
	urlRoute.GET("/:short_url", cmd.GetUrl)
	//urlRoute.PUT("/:long_url", db.UpdateUrl)
	//urlRoute.DELETE("/:long_url", db.DeleteUrl)
}
